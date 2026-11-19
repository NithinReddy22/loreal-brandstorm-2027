# Camera Acquisition Architecture: Native Android vs. Browser Fallback

**Document Version:** 2.3.0  
**System:** La Roche-Posay OptiChroma (v2.3)  
**Authors:** Principal Mobile Systems Engineer & Computer Vision Architect  
**Status:** Evaluated Camera Architecture Baseline

---

## 1. Architectural Strategy: Two-Tier Acquisition

A central finding of our technical audit is that **web browsers cannot guarantee low-level hardware camera control**. Claims that a Next.js web application can execute raw sensor capture across diverse consumer phones are technically unfounded.

OptiChroma implements a **two-tier capture architecture**:
1. **Tier 1 (Primary Capture Engine):** Native Android application utilizing the `Camera2` API for raw sensor (`RAW_SENSOR` / DNG) acquisition and hardware-locked exposure.
2. **Tier 2 (Consumer Viewing & Web Portal):** Progressive Web App (Next.js 14) for longitudinal visual review, patient records, pharmacy dashboards, and a best-effort WebRTC capture fallback with explicit limitation disclaimers.

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                                    TWO-TIER CAMERA ARCHITECTURE                                   |
+───────────────────────────────────────────────────+───────────────────────────────────────────────+
| TIER 1: NATIVE ANDROID ENGINE (Camera2 API)       | TIER 2: PROGRESSIVE WEB APP (WebRTC API)      |
+───────────────────────────────────────────────────+───────────────────────────────────────────────+
| • Format: 10-bit / 12-bit RAW_SENSOR (DNG).       | • Format: Rendered 8-bit sRGB (PNG / JPEG).   |
| • Exposure: Locked manual exposure time (t_exp).  | • Exposure: Best-effort applyConstraints().   |
| • Sensitivity: Locked ISO (typically ISO 100).    | • Sensitivity: Auto-gain controlled by OS/ISP.|
| • Focus: Locked manual lens focus distance.       | • Focus: Autofocus with reticle guide.        |
| • White Balance: Locked manual CCT gains.         | • White Balance: Auto or constrained.         |
| • Full access to un-demosaiced Bayer CFA pixels.  | • Post-ISP processed and tone-mapped image.   |
| • Role: Primary standardized capture mechanism.   | • Role: Viewing, records & fallback capture.  |
+───────────────────────────────────────────────────+───────────────────────────────────────────────+
```

---

## 2. What `RAW_SENSOR` Acquisition Avoids vs. Remaining Limitations

### 2.1 What `RAW_SENSOR` Acquisition Successfully Avoids
Bypassing the standard consumer Android Image Signal Processor (ISP) pipeline eliminates several severe confounders in medical skin photography:
1. **Proprietary Dynamic Tone Mapping (DTM):** Eliminates non-linear S-curves and local histogram equalization that brighten shadows and compress highlights based on scene context.
2. **Auto-White-Balance (AWB) Color Shifts:** Prevents continuous algorithmic hunting that alters skin chromaticity ($a^*, b^*$) between captures.
3. **Aggressive Edge Sharpening:** Bypasses unsharp masking filters that introduce synthetic halos around lesions, desquamation, and pores.
4. **Adaptive Noise Reduction:** Eliminates aggressive spatial/temporal smoothing filters that obliterate fine skin scaling and erythema gradients.
5. **Consumer "Beautification" Algorithms:** Completely prevents automatic skin-smoothing, blemish-removal, and synthetic saturation boosts.
6. **Lossy Compression & Chroma Subsampling:** Avoids 8-bit JPEG quantization and 4:2:0 chroma subsampling artifacts.

### 2.2 Remaining Sensor, Optical & Processing Limitations
Operating in `RAW_SENSOR` mode does NOT solve all measurement problems. Critical limitations that remain and must be accounted for:
1. **Sensor Quantum Efficiency ($QE(\lambda)$) Discrepancies:** Different image sensor models (e.g., Sony IMX series vs. Samsung ISOCELL vs. OmniVision) have distinct spectral transmittance curves across their Bayer color filter arrays. Two phones shooting RAW under identical lighting produce slightly different raw RGB digital numbers.
2. **Sensor Read Noise & Dark Current:** Thermal shot noise and temperature-dependent dark current pedestal remain in the raw sensor data.
3. **Hardware Black-Level Pedestal:** Raw Bayer pixels include an offset (e.g., 64, 256, or 512 DN) that must be identified from DNG metadata and subtracted before any linear processing.
4. **Software Demosaicing Interpolation:** Reconstructing full-resolution 3-channel RGB from 1-channel Bayer CFA requires interpolation (e.g. AHD or Malvar-He-Cutler), which can introduce subtle demosaicing color fringing near high-contrast edges.
5. **Lens Shading & Optical Falloff:** Natural cosine-fourth ($\cos^4\theta$) vignetting darkens image perimeters, requiring flat-field compensation or mechanical centering of the skin aperture.
6. **Temperature Drift:** Prolonged camera sensor usage causes sensor die heating, slightly altering dark noise and gain.
7. **PWA / JPEG Fallback Limitations:** When fallback WebRTC capture is used, tone mapping and gamma compression cannot be undone; analysis is restricted to qualitative, relative in-session documentation.

---

## 3. Tier 1: Native Android Camera2 Acquisition Pipeline

### 3.1 Hardware Capability Detection
Before initiating capture, the native Android service inspects `CameraCharacteristics`:
```java
CameraCharacteristics characteristics = cameraManager.getCameraCharacteristics(cameraId);

// 1. Check for RAW sensor capability
int[] capabilities = characteristics.get(CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES);
boolean hasRaw = false;
for (int cap : capabilities) {
    if (cap == CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES_RAW) {
        hasRaw = true;
        break;
    }
}

// 2. Check for manual sensor control (manual exposure, ISO, focus)
Integer syncMaxLatency = characteristics.get(CameraCharacteristics.SYNC_MAX_LATENCY);
boolean hasManualSensor = false;
for (int cap : capabilities) {
    if (cap == CameraCharacteristics.REQUEST_AVAILABLE_CAPABILITIES_MANUAL_SENSOR) {
        hasManualSensor = true;
        break;
    }
}
```

### 3.2 Locked Manual Capture Request Configuration
When `hasRaw` and `hasManualSensor` are present:
1. **Disable Auto-Exposure (AE):**
   ```java
   captureBuilder.set(CaptureRequest.CONTROL_AE_MODE, CaptureRequest.CONTROL_AE_MODE_OFF);
   captureBuilder.set(CaptureRequest.SENSOR_EXPOSURE_TIME, 20_000_000L); // 1/50 sec (20 ms)
   captureBuilder.set(CaptureRequest.SENSOR_SENSITIVITY, 100);          // ISO 100
   ```
2. **Disable Auto-Focus (AF) Hunting:**
   ```java
   captureBuilder.set(CaptureRequest.CONTROL_AF_MODE, CaptureRequest.CONTROL_AF_MODE_OFF);
   // Set fixed focus distance corresponding to 35mm working distance
   captureBuilder.set(CaptureRequest.LENS_FOCUS_DISTANCE, 28.5f); // diopters (1 / 0.035m)
   ```
3. **Disable Auto-White-Balance (AWB):**
   ```java
   captureBuilder.set(CaptureRequest.CONTROL_AWB_MODE, CaptureRequest.CONTROL_AWB_MODE_OFF);
   // Neutral 1:1 sensor gains
   captureBuilder.set(CaptureRequest.COLOR_CORRECTION_MODE, CaptureRequest.COLOR_CORRECTION_MODE_TRANSFORM_MATRIX);
   ```
4. **Acquire RAW Buffer:**
   * Output format: `ImageFormat.RAW_SENSOR`.
   * Written to disk as `.dng` using Android `DngCreator` with full metadata encapsulation (active sensor array, black level, white level, color space calibration matrices).

---

## 4. RAW Image Decoding & Processing Pipeline

DNG/RAW files must not be treated as standard 8-bit BGR images. The server/backend ingestion pipeline processes RAW sensor data deterministically:

```
[Raw DNG Input] ───> [1. Black-Level Subtraction & Linearization]
                            │ (Subtract sensor pedestal, scale to [0.0, 1.0])
                            ▼
                     [2. Demosaicing (Malvar-He-Cutler / Bilinear)]
                            │ (Interpolate 1-channel Bayer CFA to 3-channel Linear RGB)
                            ▼
                     [3. White Balance & Gain Application]
                            │ (Apply camera DNG daylight multipliers or in-frame grey patch)
                            ▼
                     [4. Color Space Conversion (Linear Camera RGB ──> sRGB)]
                            │ (Apply ColorMatrix1 / ForwardMatrix1 from DNG metadata)
                            ▼
                     [5. Linear 16-bit Image Ready for Quality Gate & Analysis]
```

### Python RAW Decoding Pipeline (Using `rawpy`):
```python
import rawpy
import numpy as np

def process_raw_dng(dng_path: str) -> np.ndarray:
    """
    Decodes raw DNG file linearly without proprietary tone curves or non-linear gamma.
    """
    with rawpy.imread(dng_path) as raw:
        # Extract linear, demosaiced 16-bit image
        # no_auto_bright=True, gamma=(1, 1) preserves physical photon proportionality
        rgb_linear = raw.postprocess(
            demosaic_algorithm=rawpy.DemosaicAlgorithm.AHD,
            half_size=False,
            four_color_rgb=False,
            use_camera_wb=True,
            use_auto_wb=False,
            no_auto_bright=True,
            output_color=rawpy.ColorSpace.sRGB,
            output_bps=16,
            gamma=(1, 1)  # Linear gamma
        )
    return rgb_linear
```

---

## 5. Tier 2: Browser Acquisition & PWA Fallback Strategy

For web-based capturing via WebRTC (`getUserMedia`), complete low-level control is impossible on most browsers. We implement a **fail-safe best-effort model**:

```javascript
// WebRTC Camera Constraints Configuration (PWA)
const constraints = {
    audio: false,
    video: {
        facingMode: { ideal: "environment" },
        width: { ideal: 1920 },
        height: { ideal: 1080 },
        // Advanced constraints: supported on Chromium Android, ignored on iOS Safari
        advanced: [
            { exposureMode: "manual", exposureTime: 20 },
            { whiteBalanceMode: "manual" },
            { focusMode: "manual" }
        ]
    }
};

async function initializeCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        const track = stream.getVideoTracks()[0];
        const capabilities = track.getCapabilities();
        
        console.log("Device Camera Capabilities:", capabilities);
        return stream;
    } catch (err) {
        console.warn("Manual camera constraints unsupported. Operating in Fallback Mode.");
    }
}
```

### Mandatory Fallback Disclaimer
When captures originate from browser WebRTC rather than native Camera2 RAW:
* The report is permanently watermarked:  
  **"WARNING: Captured via web browser fallback. Exposure and white balance were managed by consumer device ISP. Cross-device colorimetric comparability is unvalidated."**
* The in-frame 4-patch calibration target is still used to apply first-order exposure and neutral balance corrections, but no claim of device-independent standardization is made.

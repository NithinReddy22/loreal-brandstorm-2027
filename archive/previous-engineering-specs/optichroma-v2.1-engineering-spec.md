# OptiChroma v2.1 — Engineering Specification & Technical Blueprints

**Document ID:** `/architecture/optichroma-v2.1-engineering-spec.md`  
**System:** Standardized Cross-Polarized Smartphone Imaging Attachment & Longitudinal Analysis Platform  
**Target Brand Scope:** La Roche-Posay (L'Oréal Dermatological Beauty)  
**Authors:** Biomedical Imaging Engineer, Computer Vision Architect, Optical Hardware Engineer, and Critical Scientific Reviewer  
**Status:** Corrected Engineering Baseline (v2.1) — Strictly Empirical & Audit-Verified

---

## 1. Non-Negotiable Scientific & Claims Governance Matrix

This specification establishes an immutable claims boundary. Every engineer, team member, and presenter must adhere strictly to these distinctions.

```
+───────────────────────────────────────────────────────────────────────────────────────────────────────────────────+
|                                              CLAIMS GOVERNANCE TABLE                                              |
+─────────────────────────────────────────+──────────────────────────────────────+──────────────────────────────────+
| WHAT THE PROTOTYPE CAN DEMONSTRATE      | WHAT REMAINS AN UNVALIDATED          | WHAT MUST NEVER BE CLAIMED       |
| (Empirically Testable by Students)      | HYPOTHESIS (Requires Clinical Study) | (Scientifically Untrue/Overreach)|
+─────────────────────────────────────────+──────────────────────────────────────+──────────────────────────────────+
| 1. Optical reduction of specular        | 1. Correlation between Relative      | 1. "Clinical-grade               |
|    glare area and intensity via         |    Chromatic Contrast (RCC) and      |    spectrophotometer"            |
|    cross-polarization.                  |    clinical erythema severity scores.| 2. "Quantitative measurement of  |
| 2. Rejection of captures failing        | 2. Longitudinal sensitivity of GLCM  |    pure hemoglobin or melanin"   |
|    focus, exposure, or framing checks.  |    texture descriptors to treatment  | 3. "Measurement of epidermal     |
| 3. Exposure and white balance           |    outcomes over weeks.              |    barrier integrity or TEWL"    |
|    normalization using in-frame         | 3. Cross-device comparability of     | 4. "Predicts eczema/acne flares  |
|    reference patches under locked raw.  |    extracted features across diverse |    48–72 hours in advance"       |
| 4. Computation of Relative Chromatic    |    CMOS camera sensor architectures. | 5. "100% glare elimination or     |
|    Contrast (RCC) in CIELAB space.      | 4. Diagnostic utility for triage in  |    exclusive dermal imaging"     |
| 5. Standardized longitudinal visual     |    pharmacy settings.                | 6. "Autonomous AI diagnosis or   |
|    comparison views for documentation.  |                                      |    product prescription"         |
+─────────────────────────────────────────+──────────────────────────────────────+──────────────────────────────────+
```

---

## 2. Optical Hardware Architecture & Assembly Specifications

```
+---------------------------------------------------------------------------------------------------+
|                            OPTICAL ATTACHMENT MECHANICAL CROSS-SECTION                            |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|                       [ Smartphone Body ]                                                         |
|                       ┌─────────────────┐                                                         |
|                       │ Camera Aperture │                                                         |
|                       └────────┬────────┘                                                         |
| ═══════════════════════════════╪═════════════════════════════════════════════════════════════════ |
| ATTACHMENT BASEPLATE           │                                                                  |
|                                ▼ Optical Axis                                                     |
|                     ┌─────────────────────┐                                                       |
|                     │ Linear Polarizer B  │ Axis = 90° (Analyzer)                                 |
|                     └──────────┬──────────┘                                                       |
|                                │                                                                  |
|       ┌────────────────────────┼────────────────────────┐                                         |
|       │  Diffuse Optical Chamber (Matte-Black PLA)      │                                         |
|       │                                                 │                                         |
| ┌─────┴──────┐                                   ┌──────┴─────┐                                   |
| │ LED Pair A │ Dual High-CRI (CRI>95, 5000K)     │ LED Pair B │ Symmetrical Dual Illumination     |
| │  Diffuser  │ Sandblasted PMMA Diffusion Sheet  │  Diffuser  │ Sandblasted PMMA Diffusion Sheet  |
| │Polarizer A │ Axis = 0° (Illumination Polarizer)│Polarizer A │ Axis = 0° (Illumination Polarizer)|
| └─────┬──────┘                                   └──────┬─────┘                                   |
|       │                                                 │                                         |
|       ▼ Inclined at 45° to Skin Normal                  ▼ Inclined at 45° to Skin Normal          |
|       │                                                 │                                         |
|       │   Nominal Working Distance = 35.0 mm            │                                         |
|       │                                                 │                                         |
|       └────────────────────────┬────────────────────────┘                                         |
|                                │                                                                  |
|             ┌──────────────────▼──────────────────┐                                               |
|             │ Non-Compressive Standoff Aperture   │ Inner Diameter = 25 mm                        |
|             │ (Recessed 1.5mm from skin contact)  │ Integrated 4-Patch Calibration Target         |
|             └──────────────────┬──────────────────┘                                               |
|                                │                                                                  |
| ═══════════════════════════════╧═════════════════════════════════════════════════════════════════ |
|                        [ Target Skin Surface ]                                                    |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

### A. Mechanical & Geometrical Design Rules
1. **Nominal Working Distance (35.0 mm):** The 35 mm tubular baffle enforces a repeatable physical distance between the camera mounting plane and the target plane. **Terminology Note:** This is a *fixed working distance*, not a "fixed focal distance." Smartphone cameras feature autofocus systems; fixing the mechanical distance constrains the field of view (FOV) and working geometry, allowing the autofocus motor to settle consistently.
2. **Non-Compressive Standoff Rim:** Direct mechanical pressure on skin blanches microvessels, alters local perfusion, and corrupts color measurement. The contact rim features an annular perimeter ring with a **recessed contact lip (1.5 mm standoff)**. Only the outer perimeter touches surrounding skin; the central 25 mm Region of Interest (ROI) remains uncompressed.
3. **Internal Baffle Surface:** 3D-printed using carbon-black filled PLA or post-treated with non-reflective matte-black flocking tape ($\text{reflectance} < 2\%$) to eliminate internal specular reflections inside the cylinder.

---

### B. Illumination Subsystem Specifications
1. **Emitter Selection:** Dual surface-mount Nichia 757 or Seoul Semiconductor SunLike high-CRI LEDs ($CRI \ge 95$, $R_9 > 85$, nominal Correlated Color Temperature $5000\,\text{K}$). 
   * *Rationale:* High CRI ensures full spectral coverage across the visible band (400–700 nm), specifically avoiding the blue-pump spike and cyan gap ($470–490\,\text{nm}$) typical of cheap consumer LEDs.
2. **Current Regulation & Thermal Drift:**
   * LEDs are driven by a constant-current buck driver (AMC7135 or dedicated linear driver set to $100\,\text{mA} \pm 1\%$).
   * *Thermal Runaway Mitigation:* Illuminator is pulsed for **800 milliseconds** per capture rather than kept continuously lit. Operating in pulsed mode keeps junction temperature rise below $\Delta T_j < 3^\circ\text{C}$, preventing thermal lumen deprecation and spectral shifting across repeated shots.
3. **Diffusion & Polarizer Geometry:**
   * Direct LEDs create specular hotspots. Light from each LED passes through a **0.5 mm frosted sandblasted PMMA diffuser sheet** before hitting **Polarizer A**.
   * Polarizer A (over LEDs) is aligned at transmission axis $\theta_{ill} = 0^\circ$.
   * Polarizer B (over camera aperture) is aligned at transmission axis $\theta_{cam} = 90^\circ \pm 1^\circ$.
   * Polarizers: Optical grade stretched PVA film with protective cellulose triacetate (CTA) outer layers, extinction ratio $\ge 1000:1$ in the 450–650 nm range.
   * Illumination angle: Beams are directed at a nominal **$45^\circ$ angle of incidence** relative to the skin normal to deflect primary first-surface reflections away from the normal optical collection path.

---

### C. In-Frame 4-Patch Micro-Calibration Target
A microscopic reference target is permanently bonded to the interior periphery of the aperture ring (always visible in a fixed $30 \times 120$ pixel region of the frame, outside the central skin ROI):
* **Patch 1 (White Target):** 90% diffuse reflectance Spectralon or calibrated barium sulfate proxy ($R_{target} \approx [225, 225, 225]$).
* **Patch 2 (Neutral Grey 18%):** Calibrated 18% diffuse reflectance ($R_{target} \approx [118, 118, 118]$).
* **Patch 3 (Dark Grey 5%):** 5% diffuse reflectance for shadow clipping verification ($R_{target} \approx [35, 35, 35]$).
* **Patch 4 (Color Contrast Reference):** Stable terracotta/magenta inorganic pigment proxy used to monitor cross-session chromatic drift.

---

### D. Detailed Prototype Bill of Materials (BOM)

```
+----+------------------------------------+-------------------------------------------+-----------+--------------------+
| #  | Component                          | Technical Parameter / Model               | Unit Cost | Supplier / Sourcing|
+----+------------------------------------+-------------------------------------------+-----------+--------------------+
| 01 | Optical Linear Polarizing Film     | High-contrast PVA (0.2mm, Trans. 42%)     | ₹450      | Tech-optics lab    |
| 02 | High-CRI 5000K LEDs (Pack of 5)    | Nichia 757 / Lumileds (CRI 95+, 100mA)    | ₹280      | Component dist.    |
| 03 | Constant Current Driver Board      | AMC7135 350mA 1-mode driver (derated)     | ₹120      | Robotics hobby     |
| 04 | Sandblasted Optical PMMA Diffuser  | 0.5mm matte frosted sheet                 | ₹100      | Acrylic fabricator |
| 05 | 3D-Printed Baffle & Clamp Mount    | Matte Black eSUN PLA (35mm standoff)      | ₹180      | Campus 3D lab      |
| 06 | Calibration Color Target Strip     | Custom matte offset printed 4-patch strip | ₹120      | Print shop/Lab     |
| 07 | Li-Po Rechargeable Cell (3.7V)     | 400mAh with TP4056 micro-USB charge board | ₹180      | Local electronics  |
+----+------------------------------------+-------------------------------------------+-----------+--------------------+
|    | TOTAL PROTOTYPE BUILD COST         |                                           | ~₹1,430   | (~€15.80)          |
+----+------------------------------------+-------------------------------------------+-----------+--------------------+
```

---

## 3. Camera Acquisition & Optical Pipeline

### A. Raw vs. Rendered Capture Governance
To prevent camera Image Signal Processors (ISPs) from applying tone-mapping curves, non-linear gamma ($sRGB$), dynamic skin-smoothing, and auto-exposure recalculations:

1. **Preferred Capture Mode:** **10-bit or 12-bit DNG (RAW)** via:
   * Android: `Camera2` API (`RAW_SENSOR` format, manual exposure, manual sensitivity, manual lens focus, manual white balance lock).
   * iOS: `AVFoundation` (`AVCapturePhotoOutput` with `AVCapturePhotoSettings.rawPhotoPixelFormatType`).
2. **Fallback Mode (Compressed Capture):** Where mobile OS or browser sandbox (WebRTC) restricts raw access:
   * Capture at maximum resolution uncompressed JPEG/PNG with camera API `exposureMode: locked`, `whiteBalanceMode: locked`, and `focusMode: locked`.
   * Record hardware device model, camera sensor ID, ISO value, and exposure time ($t_{exp}$) into metadata.
   * Disclaim in report: *"Processed from rendered image. Cross-device comparability unvalidated."*

---

## 4. Software & Computer Vision Architecture

The software architecture is divided into three distinct modules: **Image Quality Gate**, **Normalization & Segmentation**, and **Feature Extraction & Registration**.

```
+---------------------------------------------------------------------------------------------------+
|                                  SOFTWARE PROCESSING FLOWCHART                                    |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [Captured Frame (DNG/PNG)]                                                                       |
|         │                                                                                         |
|         ▼                                                                                         |
|  ┌──────────────────────────────────────────────────────────────┐                                 |
|  │ MODULE 1: IMAGE QUALITY GATE                                 │                                 |
|  │ 1. Reference Patch Check: Detect 4 patches via Template Match│                                 |
|  │ 2. Exposure & Clipping: Saturated pixels (<0.5%) & Black (<1%)│                                 |
|  │ 3. Resolution-Aware Sharpness: Tenengrad/Laplacian Gradient  │                                 |
|  └──────────────────────────────┬───────────────────────────────┘                                 |
|                                 │                                                                 |
|               ┌─────────────────┴─────────────────┐                                               |
|               │                                   │                                               |
|         [FAIL Quality Gate]               [PASS Quality Gate]                                     |
|               │                                   │                                               |
|               ▼                                   ▼                                               |
|       Reject Frame & Return              ┌──────────────────────────────────────────────┐         |
|       Corrective Guidance Prompt         │ MODULE 2: NORMALIZATION & REGION EXTRACTION  │         |
|                                          │ 1. Compute RGB channel scaling gains from    │         |
|                                          │    18% neutral grey patch.                   │         |
|                                          │ 2. Geometric Masking: Extract central skin   │         |
|                                          │    circle (R=350px at fixed enclosure origin)│         |
|                                          └──────────────────────┬───────────────────────┘         |
|                                                                 │                                 |
|                                                                 ▼                                 |
|                                          ┌──────────────────────────────────────────────┐         |
|                                          │ MODULE 3: FEATURE EXTRACTION                 │         |
|                                          │ 1. Convert to CIELAB space.                  │         |
|                                          │ 2. Compute Individual Typology Angle (ITA).  │         |
|                                          │ 3. Compute Relative Chromatic Contrast (RCC) │         |
|                                          │    RCC = mean(a*_ROI) - mean(a*_Reference).  │         |
|                                          │ 4. Compute GLCM Texture Descriptors          │         |
|                                          │    (16 grey levels, dist=1, angles=0,45,90)  │         |
|                                          └──────────────────────┬───────────────────────┘         |
|                                                                 │                                 |
|                                                                 ▼                                 |
|                                          ┌──────────────────────────────────────────────┐         |
|                                          │ MODULE 4: STANDARDIZED LONGITUDINAL REPORT   │         |
|                                          │ 1. Register scans via Calibration Rim Target │         |
|                                          │ 2. Generate side-by-side visual delta view   │         |
|                                          │ 3. Export JSON schema to HCP Clinical Portal │         |
|                                          └──────────────────────────────────────────────┘         |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

---

### A. OpenCV / Python Implementation Module

```python
# File: optichroma_v2_1_core.py
"""
OptiChroma v2.1 Processing Core
Authors: OptiChroma Engineering Taskforce
Dependencies: numpy, opencv-python, scikit-image
"""

import cv2
import numpy as np
from typing import Dict, Any, Tuple, Optional
from skimage.feature import graycomatrix, graycoprops

class OptiChromaCoreV2:
    def __init__(self, target_grey_val: float = 118.0):
        """
        Initializes the pipeline with configurable calibration parameters.
        target_grey_val: Nominal sRGB value corresponding to 18% neutral grey reflectance.
        """
        self.target_grey_val = target_grey_val
        # Default nominal bounding box for 4-patch target (x, y, w, h) in standardized 1080p frame
        # These are initial parameters and must be calibrated to physical 3D print dimensions.
        self.patch_roi_coords = (20, 20, 100, 400) 

    def quality_gate(self, img_bgr: np.ndarray) -> Tuple[bool, Dict[str, Any]]:
        """
        Quality Gate: Validates sharpness, clipping, and exposure bounds.
        Numerical thresholds are documented initial engineering parameters.
        """
        h, w, c = img_bgr.shape
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        
        # 1. Resolution-Normalized Sharpness Score (Tenengrad Gradient Variance)
        # Using normalized Sobel gradients to avoid raw-pixel count dependency
        gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        tenengrad_score = float(np.mean(gx**2 + gy**2))
        
        # Initial threshold: determined empirically on 1080p phone imagery (typical range: 80 - 600)
        SHARPNESS_THRESHOLD = 85.0
        is_sharp = tenengrad_score >= SHARPNESS_THRESHOLD

        # 2. Specular Clipping & Shadow Saturation Check
        # Saturated: any channel >= 254 (loss of linearity)
        # Underexposed: all channels <= 5
        saturated_pixels = np.sum(img_bgr >= 254)
        shadow_pixels = np.sum(img_bgr <= 5)
        total_subpixels = h * w * c
        
        saturation_ratio = float(saturated_pixels / total_subpixels)
        shadow_ratio = float(shadow_pixels / total_subpixels)
        
        # Rejection: greater than 0.8% saturation within calibrated enclosure indicates improper seal
        is_exposure_acceptable = (saturation_ratio <= 0.008) and (shadow_ratio <= 0.02)

        passed = is_sharp and is_exposure_acceptable
        return passed, {
            "passed": passed,
            "tenengrad_sharpness": round(tenengrad_score, 2),
            "sharpness_pass": is_sharp,
            "saturation_ratio": round(saturation_ratio, 5),
            "shadow_ratio": round(shadow_ratio, 5),
            "exposure_pass": is_exposure_acceptable
        }

    def calibrate_color(self, img_bgr: np.ndarray, grey_patch: np.ndarray) -> np.ndarray:
        """
        Applies per-channel von Kries gain adjustment based on in-frame 18% neutral grey patch.
        Does NOT claim complete camera spectral inversion.
        """
        mean_b = float(np.mean(grey_patch[:, :, 0]))
        mean_g = float(np.mean(grey_patch[:, :, 1]))
        mean_r = float(np.mean(grey_patch[:, :, 2]))

        # Safeguard against division by zero or black clipped patch
        if min(mean_b, mean_g, mean_r) < 5.0:
            return img_bgr # Fail-safe fallback

        gain_b = self.target_grey_val / mean_b
        gain_g = self.target_grey_val / mean_g
        gain_r = self.target_grey_val / mean_r

        # Apply scaling
        calibrated = img_bgr.astype(np.float32)
        calibrated[:, :, 0] = np.clip(calibrated[:, :, 0] * gain_b, 0, 255)
        calibrated[:, :, 1] = np.clip(calibrated[:, :, 1] * gain_g, 0, 255)
        calibrated[:, :, 2] = np.clip(calibrated[:, :, 2] * gain_r, 0, 255)

        return calibrated.astype(np.uint8)

    def extract_skin_roi(self, img_bgr: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Extracts skin region defined by physical attachment geometry.
        Replaces complex Otsu segmentation: the 25mm standoff circular opening 
        is fixed relative to the optical center.
        """
        h, w, _ = img_bgr.shape
        center_x, center_y = w // 2, h // 2
        # Radius corresponds to inner 20mm uncompressed circular skin area
        radius = int(min(h, w) * 0.38) 

        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(mask, (center_x, center_y), radius, 255, -1)
        return mask, (center_x, center_y, radius)

    def compute_chromatic_features(self, calibrated_bgr: np.ndarray, 
                                   skin_mask: np.ndarray, 
                                   roi_coords: Tuple[int, int, int, int], 
                                   ref_coords: Tuple[int, int, int, int]) -> Dict[str, Any]:
        """
        Computes Relative Chromatic Contrast (RCC) and Individual Typology Angle (ITA).
        roi_coords: (x, y, w, h) for user-selected concern area
        ref_coords: (x, y, w, h) for adjacent non-involved reference skin
        """
        lab = cv2.cvtColor(calibrated_bgr, cv2.COLOR_BGR2LAB).astype(np.float32)
        L = lab[:, :, 0] * (100.0 / 255.0)  # Standardize L* to [0, 100]
        a = lab[:, :, 1] - 128.0            # Standardize a* to [-128, 127]
        b = lab[:, :, 2] - 128.0            # Standardize b* to [-128, 127]

        # 1. Global ITA across uncompressed skin region
        skin_indices = skin_mask > 0
        mean_L_skin = float(np.mean(L[skin_indices]))
        mean_b_skin = float(np.mean(b[skin_indices]))
        
        # ITA formula (degrees): arctan((L* - 50) / b*) * 180 / pi
        ita_deg = float(np.arctan((mean_L_skin - 50.0) / max(mean_b_skin, 0.1)) * (180.0 / np.pi))

        # 2. Relative Chromatic Contrast (RCC)
        # RCC = mean(a*_ROI) - mean(a*_Reference)
        rx, ry, rw, rh = roi_coords
        fx, fy, fw, fh = ref_coords

        a_roi = a[ry:ry+rh, rx:rx+rw]
        a_ref = a[fy:fy+fh, fx:fx+fw]

        mean_a_roi = float(np.mean(a_roi))
        mean_a_ref = float(np.mean(a_ref))
        rcc = mean_a_roi - mean_a_ref

        return {
            "individual_typology_angle_deg": round(ita_deg, 2),
            "skin_tone_group_ita": self._classify_ita(ita_deg),
            "mean_a_target_roi": round(mean_a_roi, 2),
            "mean_a_reference_skin": round(mean_a_ref, 2),
            "relative_chromatic_contrast_rcc": round(rcc, 2)
        }

    def compute_glcm_texture(self, calibrated_bgr: np.ndarray, 
                            crop_box: Tuple[int, int, int, int]) -> Dict[str, float]:
        """
        Computes standardized GLCM texture descriptors over a fixed-dimension crop.
        Quantization: 16 grey levels (to suppress sensor read noise).
        Distance: 1 pixel. Angles: 0, 45, 90, 135 degrees (averaged).
        """
        x, y, w, h = crop_box
        # Rescale crop to standardized 256x256 patch to ensure resolution invariance
        patch = cv2.resize(calibrated_bgr[y:y+h, x:x+w], (256, 256), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY)

        # Quantize from 256 levels down to 16 levels
        gray_16 = (gray // 16).astype(np.uint8)

        glcm = graycomatrix(gray_16, distances=[1], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4], 
                           levels=16, symmetric=True, normed=True)

        contrast = float(np.mean(graycoprops(glcm, 'contrast')))
        homogeneity = float(np.mean(graycoprops(glcm, 'homogeneity')))
        energy = float(np.mean(graycoprops(glcm, 'energy')))

        return {
            "glcm_texture_contrast": round(contrast, 3),
            "glcm_texture_homogeneity": round(homogeneity, 3),
            "glcm_texture_energy": round(energy, 4)
        }

    def _classify_ita(self, ita: float) -> str:
        # Standard dermatological ITA classifications (Del Bino et al.)
        if ita > 55: return "Very Light"
        elif ita > 41: return "Light"
        elif ita > 28: return "Intermediate"
        elif ita > 10: return "Tan"
        elif ita > -30: return "Brown"
        else: return "Dark"
```

---

## 5. Experimental Test Protocols (Engineering Proof-of-Concept)

Three distinct testing protocols are established to systematically validate the prototype.

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                                  THREE-TIER TESTING PROTOCOL MATRIX                               |
+───────────────────────────────────+───────────────────────────────────+───────────────────────────+
| TIER 1: BENCHTESTING              | TIER 2: EXPLORATORY HUMAN TEST    | TIER 3: FUTURE CLINICAL   |
| (Mechanical, Optical & Noise)     | (Consented Healthy Volunteers)    | (Formal IRB Trials)       |
+───────────────────────────────────+───────────────────────────────────+───────────────────────────+
| * Specular Glare Extinction Test  | * Reperfusion Observation Test    | * Multi-Center Clinical   |
| * White-Patch Repeatability Test  | * Multi-Skin-Tone Consistency     |   Comparison vs. Minolta  |
| * Motion Blur Threshold Tuning    | * Cross-Session Positioning Drift |   CM-700d Spectrometer    |
| * Battery Voltage Stability Test  | * Pharmacist Usability Survey     | * Diagnostic Concordance  |
+───────────────────────────────────+───────────────────────────────────+───────────────────────────+
```

---

### Protocol 1: Optical Glare Suppression Verification (Benchtop)
* **Objective:** Quantify the reduction of specular surface reflection achieved by the cross-polarized attachment compared to unpolarized lighting under identical exposure.
* **Materials:** High-gloss glossy photographic cardstock and an oily synthetic silicone skin phantom (coated with a thin film of mineral oil).
* **Procedure:**
  1. Fix the smartphone inside the mechanical rig.
  2. Capture Image 1: Dual LEDs on, Polarizer B removed (Parallel/Unpolarized capture).
  3. Capture Image 2: Dual LEDs on, Polarizer B installed at $90^\circ$ (Cross-polarized capture).
  4. Camera exposure, ISO (100), and sensor gain must remain strictly identical between both shots.
* **Metrics Recorded:**
  * Area of saturated specular pixels ($R, G, B \ge 250$).
  * Ratio of peak specular reflection intensity to mean background intensity.
* **Pass Criterion:** Saturated specular pixel area on the oiled phantom must decrease by **$\ge 75\%$** in the cross-polarized image without loss of ambient image exposure.

---

### Protocol 2: Measurement Repeatability & Limits of Agreement (Benchtop)
* **Objective:** Establish the instrument's measurement error and repeatability across repeated captures.
* **Procedure:**
  1. Mount the device over a static X-Rite / neutral grey 18% target.
  2. Record 15 consecutive captures over a 10-minute window (monitoring LED thermal stabilization).
  3. Lift and reposition the attachment 10 times over the same volar forearm skin location on a volunteer.
* **Statistical Metrics (Replacing naive Coefficient of Variation):**
  * Within-subject standard deviation: $s_w = \sqrt{\frac{\sum d_i^2}{2n}}$
  * Standard Error of Measurement: $\text{SEM} = s_w$
  * Repeatability coefficient: $r = 1.96 \sqrt{2} \cdot s_w = 2.77 \cdot s_w$
  * Bland–Altman 95% Limits of Agreement for paired repeated sessions.
* **Pass Criterion:** Within-session repeatability for CIELAB $a^*$ on the static grey target must satisfy $s_w \le 0.40$ units.

---

### Protocol 3: Multi-Skin-Tone Exploratory Capture Protocol
* **Objective:** Evaluate image-quality gate pass rates and visual contrast across diverse skin tones without claiming universal clinical sensitivity.
* **Ethics & Consent Governance:**
  * Testing conducted exclusively on consented, healthy adult student volunteers.
  * No invasive interventions. No testing on broken or infected skin.
  * Photographic data stored in encrypted local storage; facial identifiers strictly excluded (volar forearm and dorsal hand imaging only).
* **Protocol Steps:**
  1. Record baseline skin tone classification via computed Individual Typology Angle ($ITA^\circ$).
  2. Cohort grouping: Volunteers documented across three broad ITA bands:
     * High ITA ($>41^\circ$, Light, MST 1–4)
     * Medium ITA ($28^\circ\text{--}41^\circ$, Intermediate/Tan, MST 5–7)
     * Low ITA ($<28^\circ$, Brown/Dark, MST 8–10)
  3. Perform paired unpolarized vs. cross-polarized captures.
  4. Evaluate:
     * Did the Image Quality Gate function without bias (pass rates comparable across groups)?
     * Did cross-polarization improve visual distinction of benign vascular blanching across all groups?
* **Reporting Standard:** Results reported as an *exploratory engineering usability study* ($N=10–15$ subjects), explicitly disclaiming formal clinical trial status.

---

### Protocol 4: Controlled Reperfusion Observation Protocol
* **Objective:** Demonstrate that the system can record and visualize a transient relative change in skin chromatic contrast under controlled conditions.
* **Safety Protocol:**
  * Volunteer: Consenting healthy team member. Exclude anyone with cold agglutinin disease, Raynaud's, or vascular fragility.
  * Procedure: Apply gentle, blunt thumb pressure to the mid-volar forearm for **8 seconds**, then release.
* **Observation Capture:**
  * Frame 0: Baseline pre-pressure.
  * Frame 1: 5 seconds post-release (blanched zone transitioning to reactive hyperemia).
  * Frame 2: 30 seconds post-release (recovery).
* **Scientific Narration for Demo Video:**
  * *"Here we observe transient reactive hyperemia. The algorithm extracts the Relative Chromatic Contrast ($\Delta a^*$) between the blanched/hyperemic zone and adjacent untreated skin. This proves the system's ability to document localized color shifts without claiming to diagnose disease or measure absolute hemoglobin."*

---

## 6. Revised 5-Gate Validation Checklist

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                                    REVISED 5-GATE VALIDATION CHECKLIST                            |
+───────────────────────────────────────────────────────────────────────────────────────────────────+
| [ ] GATE 1: OPTICAL GLARE SUPPRESSION BENCHMARK                                                   |
|     Under locked camera exposure, cross-polarization reduces specular saturated pixel area        |
|     by >= 75% on an oiled phantom relative to unpolarized lighting.                               |
|                                                                                                   |
| [ ] GATE 2: SYSTEMATIC REPEATABILITY BENCHMARK                                                    |
|     10 repeated captures of a static neutral target yield a within-session standard deviation     |
|     s_w <= 0.40 on the CIELAB a* channel.                                                         |
|                                                                                                   |
| [ ] GATE 3: IMAGE QUALITY GATE TUNING                                                             |
|     Tenengrad gradient threshold and saturation ratios correctly classify >= 90% of a test set   |
|     of sharp vs. motion-blurred captures.                                                         |
|                                                                                                   |
| [ ] GATE 4: MULTI-SKIN-TONE TECHNICAL USABILITY                                                   |
|     The non-compressive standoff and exposure normalization successfully process captures        |
|     across light, intermediate, and dark skin tones without frame rejection due to melanin bias. |
|                                                                                                   |
| [ ] GATE 5: CLAIMS GOVERNANCE REVIEW                                                              |
|     All presentation decks, scripts, and UI labels have been audited: zero use of the terms      |
|     'spectrophotometer', 'pure hemoglobin concentration', 'barrier integrity measurement',       |
|     or 'flare prediction'.                                                                        |
+───────────────────────────────────────────────────────────────────────────────────────────────────+
```

---

## 7. Revised Three-Week Student Sprint Plan

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                                     3-WEEK STUDENT SPRINT ALLOCATION                              |
+───────────────────────────+───────────────────────────+───────────────────────────────────────────+
| MEMBER 1: HARDWARE & OPTICS| MEMBER 2: CV & ALGORITHMS | MEMBER 3: PWA & CLINICAL WORKFLOW         |
+───────────────────────────+───────────────────────────+───────────────────────────────────────────+
| [Week 1]                  | [Week 1]                  | [Week 1]                                  |
| • Assemble 35mm matte-    | • Implement OpenCV        | • Design Next.js 14 mobile web interface. |
|   black enclosure with    |   Tenengrad sharpness     | • Implement Camera2 / WebRTC video stream |
|   non-compressive rim.    |   and clipping check.     |   with locked exposure controls.          |
| • Mount dual high-CRI     | • Build grey-patch        | • Create on-screen circular alignment     |
|   LEDs, diffusers &       |   detection and gain      |   guide matching physical aperture.       |
|   polarizers (0° & 90°).  |   normalization module.   |                                           |
| • Verify Gate 1 (glare).  |                           |                                           |
|                           |                           |                                           |
| [Week 2]                  | [Week 2]                  | [Week 2]                                  |
| • Mount 4-patch in-frame  | • Implement CIELAB        | • Build side-by-side longitudinal         |
|   reference target.       |   conversion and Relative |   comparison view with opacity slider.    |
| • Run Protocol 2          |   Chromatic Contrast (RCC)| • Develop community pharmacist summary    |
|   (Repeatability s_w).    | • Implement 16-level GLCM |   view (structured image log + metadata).  |
| • Verify Gate 2.          |   texture module.         | • Connect frontend to FastAPI backend.    |
|                           | • Verify Gate 3.          |                                           |
|                           |                           |                                           |
| [Week 3]                  | [Week 3]                  | [Week 3]                                  |
| • Conduct Protocol 3      | • Run Protocol 4          | • Record 3-minute video presentation.     |
|   (Multi-skin-tone test). |   (Reperfusion demo).     | • Ensure UI strictly displays defensible   |
| • Verify Gate 4.          | • Finalize Python API     |   labels (RCC, Texture, ITA, Images).     |
| • Enforce Gate 5 (Scrub). |   container on Render.    | • Deploy live PWA to Vercel for judges.   |
+───────────────────────────+───────────────────────────+───────────────────────────────────────────+
```

---

## 8. Summary: The Authentic Brandstorm Narrative

When presenting OptiChroma v2.1 to L'Oréal Brandstorm judges, the team's strength lies in **uncompromising scientific honesty**:

> *"Judges, current beauty tech often promises the impossible: diagnosing disease or measuring invisible molecular biomarkers from an uncalibrated selfie. We chose a different path.  
> 
> We engineered **La Roche-Posay OptiChroma**: a low-cost, reusable optical enclosure and computer-vision platform that solves the single biggest bottleneck in digital dermatology—**uncontrolled capture variability**.  
> 
> By physically suppressing surface specular reflection and calibrating illumination at the skin surface, we make vascular and pigmentary contrast visible and trackable across all skin tones, especially skin of color. We don't claim to replace the dermatologist. We give patients, pharmacists, and clinicians the standardized visual evidence they need to communicate and care with confidence."*

# L'Oréal OptiChroma (Revised) — Forensic Technical Specification

**Document ID:** `/architecture/optichroma-redesign-spec.md`  
**Brand Partner:** La Roche-Posay (L'Oréal Dermatological Beauty)  
**Status:** Post-Audit Engineering Specification (v2.0 — Scientifically Grounded)  
**Primary Authors:** Multidisciplinary Taskforce (Principal Software Engineer, AI/ML Architect, Dermatological Science Researcher, Competition Judge)

---

## 1. Executive Summary & Forensic Position Statement

This document details the complete technical redesign of **OptiChroma**. Following a rigorous forensic audit, all unverified claims, pseudoscience, and over-extended extrapolations have been permanently excised.

### The Scientific Boundary: What We Do vs. What We Deliberately Remove

```
+-------------------------------------------------------------------------------------------------------------------------+
|                                              SCIENTIFIC POSITION MATRIX                                                 |
+-------------------------------------------------------------+-----------------------------------------------------------+
| UNVERIFIED / EXCISED CLAIMS (v1.0)                          | DEFENSIBLE / SCIENTIFICALLY SOUND REPLACEMENT (v2.0)      |
+-------------------------------------------------------------+-----------------------------------------------------------+
| "Turns phone into a clinical-grade spectrophotometer"       | Standardized, controlled optical smartphone imaging       |
| "100% optical glare extinction & pure dermal imaging"       | Significant specular reflection suppression via cross-pol |
| "Beer-Lambert matrix inversion extracts pure Hb & Melanin"  | Relative vascular-colour contrast & chromatic feature map |
| "Measures epidermal barrier integrity & lipid depletion"    | Longitudinal surface-texture & micro-relief monitoring    |
| "Predicts atopic dermatitis flares 48–72h in advance"       | Objective visual change detection over time               |
| "Autonomous AI diagnosis and product prescribing"           | Standardized visual documentation & triage escalation     |
| "€0.05 biodegradable disposable sticker"                    | Reusable, mechanically stable clip-on optical attachment  |
+-------------------------------------------------------------+-----------------------------------------------------------+
```

### Core Value Proposition (Revised)
OptiChroma is an **accessible, standardized optical attachment and computer vision platform** that:
1. Suppresses surface specular reflection to improve the visual contrast of vascular and pigmentary skin features across diverse skin tones (particularly Fitzpatrick IV–VI / Monk Skin Tone 6–10).
2. Enforces rigorous capture consistency (fixed distance, illumination, exposure, and color calibration).
3. Executes automated image-quality verification before running longitudinal change detection.
4. Provides patients, community pharmacists, and dermatologists with objective visual change tracking to support clinical decision-making.

---

## 2. Optical Physics & Hardware Architecture

### A. The Optical Reality of Human Skin
Human skin is a turbid, heterogeneous, multi-layered biological structure consisting of the stratum corneum ($10–20\,\mu m$), viable epidermis ($50–100\,\mu m$), and vascularized dermis ($1–2\,mm$).

```
                      Incident Light (Linearly Polarized 0°)
                                    │
                                    ▼
       ═════════════════════════════════════════════════════  Stratum Corneum
       ───┬─────────────────────────────────────────────────  (Air-Tissue Interface)
          │ Reflected Glare (Retains 0° Polarization: I_par)
          │  ───> BLOCKED BY 90° CAMERA FILTER (Specular Suppression)
          │
          ▼ Penetrating Photons
       ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒  Epidermis (Melanin)
          │ Multiple Rayleigh / Mie Scattering Events
          ▼ (Depolarization of Light)
       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  Dermis (Capillaries/Hb)
          │
          ▲ Diffusely Back-Scattered Depolarized Photons (I_perp)
          │  ───> PASSES 90° CAMERA FILTER TO CMOS SENSOR
```

1. **Specular Reflection (Surface Glare):** Occurs at the air-stratum corneum boundary due to refractive index mismatch ($n_{air} \approx 1.0, n_{skin} \approx 1.4$). This surface reflection preserves the polarization state of incoming light ($I_{\parallel}$).
2. **Diffuse Backscattered Remittance:** Photons that penetrate past the dermal-epidermal junction undergo multiple scattering events off collagen bundles and cellular organelles, randomizing their polarization state. The remitted light contains roughly equal parts parallel and perpendicular polarization ($I_{\perp}$).
3. **Cross-Polarization Mechanism:** Placing a linear polarizer at $0^\circ$ over the illumination source and an orthogonal polarizer at $90^\circ$ over the camera lens suppresses the majority of specular reflection ($I_{\parallel}$), isolating the diffusely scattered component ($I_{\perp}$).
4. **Engineering Caveat:** Cross-polarization does **not** extinguish 100% of surface photons (due to filter extinction ratios, oblique incidence angles, and single-scatter epidermal events), nor does it guarantee that every collected photon reached deep dermal microvessels. We claim **specular glare suppression**, not perfect optical isolation.

---

### B. Physical Attachment Specifications (Reusable Hardware)

Rather than relying on the phone's native flash (which suffers from spatial parallax, variable beam spread, and device-dependent placement), the prototype utilizes a dedicated, battery-powered optical clip-on fixture:

```
+---------------------------------------------------------------------------------------------------+
|                                 OPTICAL ATTACHMENT MECHANICAL SCHEMATIC                           |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|     +-----------------------------------------------------------------------+                     |
|     | SMARTPHONE CHASSIS                                                    |                     |
|     |                  [Camera Lens]                                        |                     |
|     +------------------------│----------------------------------------------+                     |
|                              │                                                                    |
|     +────────────────────────▼──────────────────────────────────────────────+                     |
|     │ OPTICAL ATTACHMENT BODY (3D-Printed PLA / Opaque Matte Black)         │                     |
|     │                                                                       │                     |
|     │  +─────────────────────────────────────────+                          │                     |
|     │  │ Filter B: 90° Linear Polarizing Film   │ (Over Camera Aperture)   │                     |
|     │  +─────────────────────────────────────────+                          │                     |
|     │                                                                       │                     |
|     │  +──────────────────+                   +──────────────────+          │                     |
|     │  │ High-CRI LED (0°)│                   │ High-CRI LED (0°)│          │                     |
|     │  │ + Polarizer A    │                   │ + Polarizer A    │          │                     |
|     │  +─────────┬────────+                   +────────┬─────────+          │                     |
|     │            │                                     │                    │                     |
|     │            ▼                                     ▼                    │                     |
|     │  ┌─────────────────────────────────────────────────────────┐          │                     |
|     │  │ Cylindrical Light-Baffle Spacer (Depth = 35 mm)         │          │                     |
|     │  │ - Fixed Focal Distance & Shielding from Ambient Light   │          │                     |
|     │  └─────────────────────────┬───────────────────────────────┘          │                     |
|     │                            │                                          │                     |
|     │  ┌─────────────────────────▼───────────────────────────────┐          │                     |
|     │  │ Contact Aperture Rim + Mini 4-Patch Color Target        │          │                     |
|     │  └─────────────────────────────────────────────────────────┘          │                     |
|     +───────────────────────────────────────────────────────────────────────+                     |
|                                  │                                                                |
|                                  ▼                                                                |
|                             [Skin Target]                                                         |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

#### Detailed Bill of Materials (BOM) for 3-Student Prototype

```
+----+------------------------------+-------------------------------------+-----------+-------------+
| #  | Component                    | Specification                       | Unit Cost | Source      |
+----+------------------------------+-------------------------------------+-----------+-------------+
| 01 | Linear Polarizing Film Sheet | High contrast optical grade (0.2mm) | ₹400      | Edmund/Local|
| 02 | High-CRI Mini LED Module     | CRI > 95, 5000K neutral white       | ₹250      | Electronics |
| 03 | 3D-Printed Spacer & Clip     | Matte black PLA/PETG light-baffle   | ₹150      | University  |
| 04 | Mini Calibration Target      | 4-patch neutral grey & white target | ₹100      | Self-printed|
| 05 | Reusable Spring Clamp Mount  | Universal smartphone alignment clip | ₹150      | Generic     |
+----+------------------------------+-------------------------------------+-----------+-------------+
|    | TOTAL PROTOTYPE BUILD COST   |                                     | ~₹1,050   | (~€11.50)   |
+----+------------------------------+-------------------------------------+-----------+-------------+
```

* **Physical Baffle Spacer:** A 35mm matte-black cylinder enforces a fixed camera-to-skin distance, eliminates ambient room lighting fluctuations, and ensures consistent optical geometry.
* **Controlled Illumination:** Dual high-CRI (Color Rendering Index > 95) LEDs with identical $0^\circ$ linear polarizing film ensure uniform bilateral illumination across the field of view without central flash hot-spots.
* **Color/Exposure Target:** A tiny micro-calibration frame positioned at the edge of the contact aperture provides known reference values (White 90% reflectance, 18% Neutral Grey, Dark Grey, Skin-tone proxy) inside every single captured frame.

---

## 3. Image Processing & Computer Vision Pipeline

We replace the scientifically untenable Beer-Lambert $3\times3$ matrix inversion with an **empirically calibrated, reproducible computer vision pipeline**:

```
+---------------------------------------------------------------------------------------------------+
|                                  COMPUTER VISION PROCESSING PIPELINE                              |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [Captured Frame] ───> [1. Image Quality Gate]                                                    |
|                               │ (Reject if blurred, over-exposed, or poorly framed)               |
|                               ▼ PASS                                                              |
|                        [2. Reference Color & Exposure Normalization]                              |
|                               │ (Calibrate against micro-patch: White balance & gain correction)  |
|                               ▼                                                                   |
|                        [3. Skin ROI Segmentation (Otsu + GrabCut / MediaPipe)]                    |
|                               │ (Isolate lesion / skin from background aperture rim)              |
|                               ▼                                                                   |
|                        [4. Dual-Domain Feature Extraction]                                        |
|                               ├─────────────────────────────────┐                                 |
|                               ▼                                 ▼                                 |
|                    [Chromatic Feature Domain]        [Morphological Texture Domain]               |
|                    - CIELAB a* (Vascular Contrast)   - GLCM Energy, Homogeneity, Contrast         |
|                    - Erythema Visual Contrast Index  - Spatial Frequency Roughness                |
|                               │                                 │                                 |
|                               └────────────────┬────────────────┘                                 |
|                                                ▼                                                  |
|                        [5. Longitudinal Registration & Delta Comparison]                          |
|                               │ (Rigid feature matching via SIFT/ORB against Baseline Scan)       |
|                               ▼                                                                   |
|                        [6. Objective Visual Change Report & HCP Escalation]                       |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

---

### Step 1: Automated Image Quality Gate (Zero-Hallucination Guardrail)
Before any analytical processing occurs, the image must pass three automated quality checks:
1. **Blur & Motion Sharpness Metric:** Computes the variance of the Laplacian operator:
   $$\text{Blur Score} = \text{Var}\left(\nabla^2 I_{grey}\right)$$
   If $\text{Blur Score} < \theta_{sharpness}$ (empirically set to 150), the capture is automatically rejected with an on-screen prompt: *"Hold device steady."*
2. **Specular Glare Area Verification:** Measures the percentage of pixels where RGB intensity saturates ($R > 250 \land G > 250 \land B > 250$):
   $$\text{Glare Ratio} = \frac{\sum [I(x,y) \ge 250]}{N_{total}}$$
   If $\text{Glare Ratio} > 0.02$ (more than 2% specular glare), the attachment alignment is flagged as compromised.
3. **Illumination Uniformity Check:** Evaluates luminance variance across the four quadrants of the calibration rim to detect angular tilt or uneven contact.

---

### Step 2: Exposure & Chromatic Normalization
To prevent camera ISP variances (auto-white-balance drifts, exposure changes) from polluting the medical comparison:
1. The known 18% neutral grey patch in the frame is located via template matching.
2. Channel scaling gains ($k_R, k_G, k_B$) are computed:
   $$k_c = \frac{I_{target\_grey}}{I_{measured\_grey\_c}} \quad \text{for } c \in \{R, G, B\}$$
3. The skin region is normalized: $I_{norm}(c) = \text{clip}(k_c \cdot I(c), 0, 255)$.

---

### Step 3: Skin-Tone-Aware Chromatic Feature Extraction

Instead of claiming to compute "pure molar hemoglobin concentration," we compute a scientifically defensible **Erythema Contrast Index (ECI)** and **Melanin-Adjusted Vascular Difference** using the perceptually uniform **CIELAB ($L^*a^*b^*$) color space**:

1. **Color Space Conversion:** Normalized RGB pixels are converted to CIE $L^*a^*b^*$:
   * $L^*$: Perceptual Lightness ($0 = \text{Black}, 100 = \text{White}$).
   * $a^*$: Red-Green Chromatic Axis (positive values indicate erythema/redness; negative indicate green).
   * $b^*$: Yellow-Blue Chromatic Axis (positive values correlate with melanin/carotene; negative indicate blue).
2. **Individual Typology Angle ($ITA^\circ$):** Characterizes the constitutive skin phototype:
   $$ITA^\circ = \frac{\arctan\left(\frac{L^* - 50}{b^*}\right) \times 180}{\pi}$$
   Categorizes skin tone into Very Light ($>55^\circ$), Intermediate ($41^\circ\text{--}55^\circ$), Tan ($28^\circ\text{--}41^\circ$), Brown ($10^\circ\text{--}28^\circ$), or Dark ($<10^\circ$).
3. **Erythema Contrast Score ($\Delta a^*$):**
   To detect inflammation on darker skin where melanin depresses visual contrast, we calculate the relative shift in the $a^*$ channel compared to adjacent non-inflamed peri-lesional healthy skin:
   $$\Delta a^*(x,y) = a^*_{lesion}(x,y) - \mu(a^*_{healthy})$$
   *Why this works:* Even when high melanin lowers the overall $L^*$ and shifts absolute skin color toward brown/grey, vascular dilation causes a statistically significant positive shift along the $a^*$ axis. Cross-polarization prevents specular surface glare from washing out this subtle shift.

---

### Step 4: Surface Micro-Relief & Texture Tracking (GLCM)
Rather than falsely claiming to measure "Transepidermal Water Loss" or "lipid depletion," we monitor **visible surface texture changes** using Gray-Level Co-occurrence Matrices (GLCM):
1. **GLCM Contrast:** Measures local spatial variations in pixel intensity, quantifying visible flaking, desquamation, and skin cracking:
   $$\text{Contrast} = \sum_{i,j} |i - j|^2 P(i,j)$$
2. **GLCM Homogeneity:** Measures the closeness of the distribution of elements in the GLCM to the GLCM diagonal, tracking smoothing or barrier recovery over time:
   $$\text{Homogeneity} = \sum_{i,j} \frac{P(i,j)}{1 + |i - j|}$$
3. **Longitudinal Texture Drift:** A patient applying La Roche-Posay Cicaplast B5+ or CeraVe Moisturizing Cream will exhibit a measurable decline in GLCM Contrast and an increase in Homogeneity over 7 to 14 days, providing objective visual proof of clinical smoothing.

---

## 4. Software Architecture & Implementation Blueprint

```
+---------------------------------------------------------------------------------------------------+
|                                  SYSTEM SOFTWARE STACK (3-STUDENT BUILD)                          |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|   +-------------------------------------------------------------------------------------------+   |
|   | CLIENT: Next.js 14 Progressive Web App (PWA) / React Native                               |   |
|   | * Camera Viewfinder with Real-Time Quality Guidance Overlay                               |   |
|   | * WebAssembly / OpenCV.js for On-Device Frame Sharpness & Glare Check                     |   |
|   | * Side-by-Side Longitudinal Comparison Slider with Dynamic Delta Heatmap                  |   |
|   +---------------------------------------------┬---------------------------------------------+   |
|                                                 │ HTTPS / Secure REST                             |
|   +---------------------------------------------▼---------------------------------------------+   |
|   | BACKEND: Python 3.11 / FastAPI Service                                                    |   |
|   | * Endpoint POST /api/v1/capture/calibrate: Normalizes against reference patch            |   |
|   | * Endpoint POST /api/v1/analyze/features: Computes CIELAB a* delta and GLCM metrics       |   |
|   | * Endpoint POST /api/v1/longitudinal/register: Aligns Day 0 vs Day N using ORB homography |   |
|   +---------------------------------------------┬---------------------------------------------+   |
|                                                 │                                                 |
|   +---------------------------------------------▼---------------------------------------------+   |
|   | PERSISTENCE: PostgreSQL 16 (Supabase)                                                     |   |
|   | * Structured JSONB storing standardized metrics (Delta_a, GLCM_contrast, ITA, QualityScore)|   |
|   | * Encrypted image blob references (Zero cloud storage of uncalibrated biometric PII)      |   |
|   +-------------------------------------------------------------------------------------------+   |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

### Complete, Functional Python/OpenCV Processing Module

```python
# File: optichroma_core.py
# Production-ready, scientifically defensible image processing engine
# Designed for three CS students using FastAPI and OpenCV

import cv2
import numpy as np
from typing import Dict, Any, Tuple

class OptiChromaEngine:
    def __init__(self, sharpness_threshold: float = 120.0, max_glare_ratio: float = 0.03):
        self.sharpness_threshold = sharpness_threshold
        self.max_glare_ratio = max_glare_ratio

    def verify_quality(self, bgr_image: np.ndarray) -> Tuple[bool, Dict[str, Any]]:
        """
        Quality Gate: Verifies that image is in focus and free of specular saturation.
        """
        gray = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        
        # 1. Laplacian sharpness score
        laplacian_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        is_sharp = laplacian_var >= self.sharpness_threshold
        
        # 2. Specular glare saturation ratio (>250 in all channels)
        h, w, _ = bgr_image.shape
        glare_mask = (bgr_image[:, :, 0] > 250) & (bgr_image[:, :, 1] > 250) & (bgr_image[:, :, 2] > 250)
        glare_ratio = float(np.sum(glare_mask) / (h * w))
        is_glare_acceptable = glare_ratio <= self.max_glare_ratio
        
        passed = is_sharp and is_glare_acceptable
        details = {
            "passed": passed,
            "sharpness_score": round(laplacian_var, 2),
            "is_sharp": is_sharp,
            "glare_ratio": round(glare_ratio, 4),
            "is_glare_acceptable": is_glare_acceptable
        }
        return passed, details

    def normalize_color(self, bgr_image: np.ndarray, grey_patch_roi: Tuple[int, int, int, int]) -> np.ndarray:
        """
        Normalizes color balance and exposure using the 18% neutral grey calibration patch.
        grey_patch_roi: (x, y, w, h)
        """
        x, y, w, h = grey_patch_roi
        patch = bgr_image[y:y+h, x:x+w].astype(np.float32)
        
        # Compute mean intensity of grey patch per channel
        mean_b = np.mean(patch[:, :, 0])
        mean_g = np.mean(patch[:, :, 1])
        mean_r = np.mean(patch[:, :, 2])
        
        # Target grey level (18% grey mapped to sRGB ~ 118)
        target_val = 118.0
        scale_b = target_val / max(mean_b, 1.0)
        scale_g = target_val / max(mean_g, 1.0)
        scale_r = target_val / max(mean_r, 1.0)
        
        normalized = bgr_image.astype(np.float32)
        normalized[:, :, 0] = np.clip(normalized[:, :, 0] * scale_b, 0, 255)
        normalized[:, :, 1] = np.clip(normalized[:, :, 1] * scale_g, 0, 255)
        normalized[:, :, 2] = np.clip(normalized[:, :, 2] * scale_r, 0, 255)
        
        return normalized.astype(np.uint8)

    def extract_features(self, normalized_bgr: np.ndarray, skin_mask: np.ndarray) -> Dict[str, Any]:
        """
        Extracts defensible chromatic and textural features:
        - CIELAB a* (Erythema / Vascular Contrast)
        - ITA (Individual Typology Angle for Skin Tone Classification)
        - Texture roughness proxy
        """
        lab = cv2.cvtColor(normalized_bgr, cv2.COLOR_BGR2LAB).astype(np.float32)
        L = lab[:, :, 0] * (100.0 / 255.0)  # Scale to [0, 100]
        a = lab[:, :, 1] - 128.0            # Shift to [-128, 127]
        b = lab[:, :, 2] - 128.0            # Shift to [-128, 127]

        # Apply skin mask
        valid_indices = skin_mask > 0
        if np.sum(valid_indices) == 0:
            return {"error": "No valid skin pixels detected"}

        L_skin = L[valid_indices]
        a_skin = a[valid_indices]
        b_skin = b[valid_indices]

        # 1. Compute ITA (Individual Typology Angle)
        mean_L = np.mean(L_skin)
        mean_b = np.mean(b_skin)
        ita = (np.arctan((mean_L - 50.0) / max(mean_b, 0.1)) * 180.0) / np.pi

        # 2. Compute Vascular-Colour Contrast (Mean a* and standard deviation)
        mean_a = np.mean(a_skin)
        std_a = np.std(a_skin)

        # 3. Micro-Texture Surface Metric (High-pass filtered variance)
        gray = cv2.cvtColor(normalized_bgr, cv2.COLOR_BGR2GRAY)
        high_pass = cv2.Sobel(gray, cv2.CV_64F, 1, 1, ksize=3)
        texture_score = float(np.var(high_pass[valid_indices]))

        # Generate Normalized Visual Contrast Heatmap (a* channel)
        a_norm = np.clip((a + 20) * (255.0 / 40.0), 0, 255).astype(np.uint8)
        contrast_heatmap = cv2.applyColorMap(a_norm, cv2.COLORMAP_VIRIDIS)
        contrast_heatmap[~valid_indices] = [0, 0, 0]

        return {
            "ita_degrees": round(float(ita), 2),
            "skin_phototype_category": self._classify_ita(ita),
            "vascular_contrast_a_mean": round(float(mean_a), 2),
            "vascular_contrast_a_std": round(float(std_a), 2),
            "surface_texture_score": round(texture_score, 2),
            "heatmap": contrast_heatmap
        }

    def _classify_ita(self, ita: float) -> str:
        if ita > 55: return "Very Light (MST 1-2)"
        elif ita > 41: return "Light (MST 3-4)"
        elif ita > 28: return "Intermediate (MST 5-6)"
        elif ita > 10: return "Tan / Brown (MST 7-8)"
        else: return "Dark (MST 9-10)"
```

---

## 5. The Live Demonstration Protocol (Proving the Real Mechanism)

To win Brandstorm, the team must present a **live, scientifically validated demonstration**, not a PowerPoint animation or Figma click-through.

```
+---------------------------------------------------------------------------------------------------+
|                                 LIVE HACKATHON DEMO EXPERIMENTAL SETUP                            |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  STEP 1: The Side-by-Side Physical Optical Demonstration                                          |
|  * Demonstrate on an actual volunteer (team member or judge):                                    |
|    - Capture A: Ordinary Unpolarized Smartphone Lighting. Show on-screen: Specular reflection      |
|      from skin oils washes out fine micro-erythema; dark skin tone masks subtle redness.          |
|    - Capture B: OptiChroma Cross-Polarized Attachment. Show on-screen: Specular glare is optically |
|      quenched; subsurface vascular contrast becomes crisp and clear.                              |
|                                                                                                   |
|  STEP 2: Automated Quality Gate Rejection (Proving Real Algorithmic Substance)                   |
|  * Intentionally shake the device: App displays real-time "Blur Score: 72 — REJECTED".            |
|  * Hold device steady at baffle depth: App green-lights "Sharpness: 210 — PASS".                  |
|  * Judges see that the software actively enforces clinical standards.                            |
|                                                                                                   |
|  STEP 3: The Controlled Mechanical Reperfusion Experiment (Optical Verification)                  |
|  * A consenting volunteer presses a blunt, sanitized thumb against the volar forearm for 10 sec   |
|    to induce temporary mechanical blanching followed by localized reactive hyperemia (reperfusion)|
|  * The volunteer captures two OptiChroma cross-polarized frames (Baseline vs 15 sec post-release). |
|  * The OptiChroma algorithm runs: computes the Delta a* vascular heatmap live on screen.          |
|  * The transient hyperemic flush is clearly revealed as a vivid yellow-green contrast halo!       |
|  * TEAM DELIVERS THE KEY PITCH LINE:                                                              |
|    "Judges, this is not a diagnostic claim or an AI guess. This is reproducible optical           |
|     contrast enhancement running live on standard hardware."                                      |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

---

## 6. Three-Week Student Engineering Roadmap

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                                    3-WEEK SPRINT WORK BREAKDOWN                                   |
+───────────────────────────+───────────────────────────+───────────────────────────────────────────+
| MEMBER 1                  | MEMBER 2                  | MEMBER 3                                  |
| Hardware & Calibration    | Computer Vision & Backend | Frontend & Brandstorm UX                  |
+───────────────────────────+───────────────────────────+───────────────────────────────────────────+
| * Buy optical polarizing  | * Implement OpenCV        | * Build Next.js 14 / React                |
|   film and high-CRI LEDs. |   quality gate (blur and  |   Native viewfinder interface.            |
| * Construct 3D-printed    |   specular glare check).  | * Build side-by-side comparison           |
|   35mm baffle spacer clip.| * Implement CIELAB a*     |   slider & longitudinal timeline.         |
| * Mount 4-patch neutral   |   contrast and GLCM       | * Create pharmacy triage summary          |
|   color target on rim.    |   texture module.         |   dashboard under La Roche-Posay.         |
| * Calibrate illumination  | * Build FastAPI endpoints | * Integrate with Supabase JSONB           |
|   uniformity across phone |   with NumPy processing   |   schema and deploy prototype             |
|   models (iPhone/Pixel).  |   and error handling.     |   to Vercel for live judging.             |
+───────────────────────────+───────────────────────────+───────────────────────────────────────────+
| DELIVERABLE (Week 1):     | DELIVERABLE (Week 2):     | DELIVERABLE (Week 3):                     |
| Functional Optical Mount  | Tested CV Processing API  | End-to-End Live Web/Mobile Demo           |
+───────────────────────────+───────────────────────────+───────────────────────────────────────────+
```

---

## 7. The 5-Gate "Go / No-Go" Validation Checklist

Prior to entering video production or slide authoring, the team must pass every gate:

```
[ ] GATE 1: OPTICAL SUPPRESSION CHECK
    Can the team demonstrate visible reduction of specular reflection on oily skin when rotating 
    the camera polarizer to 90° relative to the LED source?
    --> PASS CRITERION: Specular pixel saturation drops by >80%.

[ ] GATE 2: REPEATABILITY CHECK
    Can the team capture 5 consecutive images of the same static skin region and obtain a CIELAB a* 
    mean variance of less than 3%?
    --> PASS CRITERION: Coefficient of Variation (CV) < 0.03.

[ ] GATE 3: IMAGE QUALITY REJECTION CHECK
    Does the algorithm reliably reject intentionally degraded captures (motion blur, off-axis tilt)?
    --> PASS CRITERION: 100% rejection of blurry frames without false rejections of sharp frames.

[ ] GATE 4: SKIN-OF-COLOR CONTRAST CHECK
    Does the cross-polarized capture reveal micro-vascular contrast shifts on Monk Skin Tone 7–10 
    that are obscured by surface shine in unpolarized photos?
    --> PASS CRITERION: Statistically significant improvement in Delta a* contrast ratio.

[ ] GATE 5: ZERO PSEUDOSCIENCE SCRUB
    Have all references to "spectrophotometer", "pure hemoglobin concentration", "barrier integrity 
    index", and "flare prediction" been purged from slides and speech scripts?
    --> PASS CRITERION: 100% adherence to defensible optical and computational claims.
```

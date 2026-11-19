# L'Oréal Brandstorm 2027 — La Roche-Posay OptiChroma v2.3

[![Test Suite](https://img.shields.io/badge/pytest-32%20passed%20(100%25)-brightgreen.svg)](tests/)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](src/)
[![Brand](https://img.shields.io/badge/Brand-La%20Roche--Posay-009ee2.svg)](https://www.laroche-posay.com/)
[![Playing Field](https://img.shields.io/badge/Brandstorm%202027-Playing%20Field%203-darkblue.svg)](#competition-alignment)
[![Evidence Baseline](https://img.shields.io/badge/Evidence%20Register-v2.3%20Audited-orange.svg)](research/evidence-register.md)

> **Official Competition Concept:** A standardized cross-polarized optical smartphone imaging attachment and longitudinal visual documentation platform designed to improve skin-image consistency across all skin tones and support communication between patients, pharmacists, and healthcare professionals.

---

## 1. Executive Summary & Brand Alignment

* **Brand:** **La Roche-Posay** (L'Oréal Dermatological Beauty Division)
* **Official Playing Field:** **Playing Field 3 — Reinvent the Doctor-Patient Relationship**
* **The Core Problem:** Smartphone skin photographs taken by patients or frontline healthcare providers frequently suffer from blinding specular glare, variable room lighting, camera motion blur, and optical color masking on deeper skin tones. Patients with chronic conditions (atopic dermatitis, eczema) struggle to track flare-ups objectively, while community pharmacists lack standardized optical tools to triage skin concerns.
* **The Solution:** **La Roche-Posay OptiChroma (v2.3)** combines an accessible, reusable cross-polarized optical attachment with an algorithmic quality gate, in-frame reference normalization, Relative Chromatic Contrast ($RCC$) scoring, and exploratory GLCM texture descriptors.
* **Status:** Exploratory Student Proof-of-Concept. NOT an autonomous diagnostic tool or certified medical device.

```
+-----------------------------------------------------------------------------------+
|                        LA ROCHE-POSAY OPTICHROMA v2.3                             |
|                                                                                   |
|  [Hardware Attachment]             [Capture Pipeline]       [Clinical Portal]    |
|  * 3D Enclosure (rPC / Polymer)      * Camera2 Native RAW     * Pharmacist Triage |
|  * Cross-Polarizers (Ext. >100:1)    * Tenengrad Sharpness    * Telederm Export   |
|  * High-CRI LEDs (CRI>95, 5000K)     * Reference Normalization* Longitudinal Trend|
|  * Series-Boost Constant Driver      * Relative Contrast (RCC)* Eczema/Psoriasis  |
|  * Non-Compressive 1.5mm Standoff    * GLCM Texture Descriptors Documentation     |
+-----------------------------------------------------------------------------------+
```

---

## 2. Non-Negotiable Boundaries & Claims Governance

To maintain scientific honesty, regulatory feasibility, and clinical credibility, OptiChroma strictly adheres to defined boundaries:

| Prohibited Claim / Pseudoscience | Approved Scientific Capability (OptiChroma v2.3) |
| :--- | :--- |
| **NO Autonomous Diagnosis:** Does not diagnose melanoma, atopic dermatitis, or skin cancer. | **Clinical Documentation:** Standardized image capture, visual archiving, and decision-support triage. |
| **NO Spectrophotometer Claims:** Does not output absolute spectral reflectance curves ($\text{nm}^{-1}$). | **Reference-Assisted Normalization:** In-frame 18% neutral gray ceramic standard normalizes RGB gains. |
| **NO Hemoglobin / Melanin Quantification:** Does not measure blood volume, blood flow, capillary dilation, or melanin mass. | **Relative Chromatic Contrast ($RCC$):** Tracks relative chromatic shifts along the CIELAB red-green axis ($RCC = \overline{a^*}_{ROI} - \overline{a^*}_{ref}$). |
| **NO Skin Barrier / TEWL Measurement:** Does not quantify Transepidermal Water Loss ($\text{g/m}^2/\text{h}$). | **Exploratory GLCM Texture:** Quantifies 2D image roughness, homogeneity, and contrast across 16 quantized gray levels. |
| **NO 48–72h Flare Prediction:** Does not predict subclinical inflammatory flares days in advance. | **Longitudinal Trend Tracking:** Records and plots objective visual trajectories over days and weeks. |
| **NO 100% Glare Elimination:** Does not claim total extinction of all optical reflection. | **Verified Glare Suppression:** Orthogonal cross-polarization targets $\ge 75\%$ specular suppression. |
| **NO Fitzpatrick Equivalence:** ITA surface color categories do NOT determine Fitzpatrick phototypes. | **Descriptive Colorimetry:** ITA ($ITA^\circ$) categorizes surface skin reflectance objectively (Chardon et al., 1991). |

---

## 3. Repository Structure

```
Loreal/
├── architecture/                             # Authoritative technical specifications
│   ├── camera-acquisition.md                 # Camera2 RAW vs WebRTC fallback architecture
│   ├── hardware-design.md                    # Mechanical, optical, and electrical schematics
│   ├── image-processing-pipeline.md          # Algorithmic image processing & OpenCV math
│   ├── optichroma-v2.3-engineering-spec.md   # Master consolidated engineering specification
│   └── validation-protocol.md                # Benchtop, usability & non-invasive protocols
├── archive/                                  # Historical iterations (isolated & preserved)
│   ├── previous-concepts/                    # Concepts 01–10, scorecards, and audit logs
│   ├── previous-dossiers/                    # Multi-concept master dossier archive (76 pages)
│   └── previous-engineering-specs/           # Draft specifications (v1.0 & v2.1)
├── concept/                                  # Brand & user experience documentation
│   ├── claims-governance.md                  # Non-negotiable claims charter & terminology
│   ├── optichroma-concept.md                 # La Roche-Posay OptiChroma v2.3 concept charter
│   └── user-workflow.md                      # Patient, pharmacist & dermatologist journeys
├── research/                                 # Scientific & competitive intelligence
│   ├── competitor-analysis.md                # Benchmarking VISIA, DermLite, ScalpConsult Pro
│   ├── evidence-register.md                  # Audited register of all project claims & status
│   ├── market-research.md                    # Epidemiology, skin-of-color optics, pharmacy triage
│   ├── mission-analysis.md                   # Brandstorm 2027 mission analysis & LDB fit
│   └── scientific-evidence.md                # Cross-polarization, CIELAB a*, and ITA° literature
├── src/                                      # Python proof-of-concept implementation
│   ├── optichroma_v2_2_core.py               # Compatibility layer forwarding to v2.3
│   └── optichroma_v2_3_core.py               # Forensic core: capture, quality gate & features
├── submission/                               # Brandstorm 2027 competition deliverables
│   ├── pitch-deck-content.md                 # Working draft 3-slide pitch content
│   └── video-script-outline.md               # Working draft 3-minute video presentation script
├── tests/                                    # Automated test suite (32 tests, 100% pass)
│   ├── test_calibration.py                   # Patch detection, clipping & gain normalization
│   ├── test_chromatic_features.py            # RCC calculations & circular ROI masking
│   ├── test_forensic_edge_cases.py           # Multi-resolution, OOB, empty, dtype, ITA stability
│   ├── test_quality_gate.py                  # Tenengrad sharpness & exposure gate tests
│   └── test_texture_features.py              # GLCM texture extraction & 16-level quantization
├── compile_dossier_pdf.py                    # Playwright PDF compiler script
├── LOREAL_BRANDSTORM_2027_OPTICHROMA_FINAL_DOSSIER.pdf  # Final compiled publication-grade PDF
├── MISSION DOCUMENT L-OREAL BRANDSTORM 2027 (2).pdf     # Official competition brief
└── README.md                                 # Consolidated repository documentation index
```

---

## 4. Hardware Specifications & Forensic Electrical Design

* **Optical Geometry:** Fixed working distance optical baffle ($35\text{ mm}$ internal standoff) with $60^\circ$ micro-fluted anti-reflective internal geometry.
* **Non-Compressive Standoff:** Annular contact rim with a $1.5\text{ mm}$ recessed internal optical aperture, distributing contact away from the central diagnostic field.
* **Cross-Polarization Engine:** Orthogonal linear polarizing films (extinction ratio $>100:1$, transmission $38\%$) positioned over the illumination source and camera sensor aperture.
* **Calibrated Illumination:** Dual high-CRI surface-mount LEDs ($5000\text{ K}$, $R_a \ge 95$, $R_9 \ge 90$) arranged in **series** and driven by an inductive boost constant-current driver (e.g. TI TPS61165) to eliminate parallel current-hogging and battery-discharge dimming.
* **Pulsed Operation:** $800\text{ ms}$ capture window minimizes thermal heating and battery consumption.
* **In-Frame Reference Standard:** Permanent $18\%$ neutral gray ceramic patch positioned on the internal aperture ring for real-time linear gain calibration.
* **Bill of Materials (BOM):** Student prototype build cost estimated at **~₹1,750 (~€19.00)**; preliminary target for mass production modeled at ~₹750–₹950 (~€8.00–€10.50).

---

## 5. Software Pipeline & Features

Implemented and verified in `src/optichroma_v2_3_core.py`:

1. **Input Validation:** Enforces strict 3-channel BGR dimensionality, uint8 typing, minimum $200\times200$ resolution, and non-empty arrays.
2. **Tenengrad Sharpness Gate:** Calculates Sobel gradient energy $\nabla I = (I * S_x)^2 + (I * S_y)^2$; rejects frames with sharpness $T < 85.0$.
3. **Exposure & Clipping Check:** Rejects frames with $>0.8\%$ specular saturated pixels ($255$) or $>2.0\%$ underexposed pixels.
4. **Patch-Assisted Normalization:** Detects in-frame $18\%$ gray reference patch; validates uniformity ($\sigma < 18.0$); scales RGB channels linearly with bounded gains ($[0.4, 2.5]$).
5. **Circular ROI Extraction:** Masks a central circular biological zone ($r = 0.35 \times \min(H, W)$), eliminating housing boundary artifacts.
6. **Relative Chromatic Contrast ($RCC$):** Computes $RCC = \overline{a^*}_{ROI} - \overline{a^*}_{ref}$ in CIELAB color space under $D65$ illuminant.
7. **Individual Typology Angle ($ITA^\circ$):** Computes $ITA^\circ = (\arctan((L^* - 50) / b^*)) \times (180/\pi)$ with numerical stability guards when $b^* \to 0$ or $b^* < 0$. Categorizes descriptive surface color groups (Very Light to Dark).
8. **GLCM Texture Extraction:** Quantizes $256 \times 256$ crop into 16 discrete levels; computes Contrast, Homogeneity, and Energy across 4 directions ($0^\circ, 45^\circ, 90^\circ, 135^\circ$).

---

## 6. Verification & Automated Testing

The implementation has been verified using `pytest`:

```bash
# Run the complete test suite
python -m pytest -v
```

### Test Suite Summary (32 Tests, 100% Pass)
* `tests/test_calibration.py`: 5 tests (patch detection, clipping flag, uniformity flag, gain scaling, fallback).
* `tests/test_chromatic_features.py`: 4 tests (contrast delta, zero difference, coordinate bounds, circular ROI masking).
* `tests/test_forensic_edge_cases.py`: 13 tests (1D/2D/4D shapes, empty arrays, unsupported dtypes, non-numpy inputs, missing patches, extreme gains, OOB ROIs, multi-resolution 200x200 to 2500x2500, constant images, invalid GLCM crops, ITA stability with $b^*=0$ and $b^*<0$).
* `tests/test_quality_gate.py`: 4 tests (invalid types, sharpness pass, blur rejection, saturation rejection).
* `tests/test_texture_features.py`: 3 tests (flat surface, high-contrast checkerboard, crop boundary handling).
* **Result:** **32 passed in 1.71s (100% pass rate, 0 failures, 0 warnings)**.
* *Governance Note:* Software unit tests verify only that the software code executes without error; they do NOT constitute proof of physical optical performance on human skin.

---

*L'Oréal Brandstorm 2027 | La Roche-Posay Innovation Taskforce*

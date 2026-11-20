# L'Oréal Brandstorm 2027 — La Roche-Posay OptiChroma v2.4

[![Test Suite](https://img.shields.io/badge/pytest-59%20passed%20(100%25)-brightgreen.svg)](tests/)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](src/)
[![3D CAD](https://img.shields.io/badge/CAD-OpenSCAD%20%2F%20STL-purple.svg)](cad/)
[![Brand](https://img.shields.io/badge/Brand-La%20Roche--Posay-009ee2.svg)](https://www.laroche-posay.com/)
[![Playing Field](https://img.shields.io/badge/Brandstorm%202027-Playing%20Field%203-darkblue.svg)](#competition-alignment)
[![Evidence Baseline](https://img.shields.io/badge/Evidence%20Register-v2.4%20Audited-orange.svg)](research/evidence-register.md)
[![Status](https://img.shields.io/badge/Status-Frozen%20Student%20MVP-success.svg)](OPTICHROMA_v2_4_MVP_SPEC.md)

> **Official Competition Concept:** A standardized cross-polarized optical smartphone imaging attachment and longitudinal visual documentation platform designed to improve skin-image consistency across all skin tones and support communication between patients, pharmacists, and healthcare professionals.

---

## 1. Quickstart: Interactive Prototype Demonstration

OptiChroma features an interactive clinical demonstration application that executes the verified computer vision engine, runs real-time optical quality gating, renders longitudinal split comparisons, and generates standardized patient-to-clinician consultation summaries.

### Launch in 3 Simple Steps:

```bash
# 1. Clone the repository
git clone https://github.com/NithinReddy22/loreal-brandstorm-2027.git
cd loreal-brandstorm-2027

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the interactive prototype server
python app.py
```

Open your browser to: **`http://127.0.0.1:5000`**

### What You Can Demonstrate Live:
1. **Optical Capture & Live Quality Gate:** Test image sharpness (Tenengrad gradient energy $\ge 85.0$) and specular reflection suppression (saturation $\le 0.8\%$). Try preloaded sample presets (Day 0 Baseline, Day 7 Follow-Up, Glare Artifact, Defocus Blur, Phototype VI Dark Skin, Phototype I Fair Skin) or upload custom captures.
2. **Longitudinal Comparison Canvas:** One-click generation of the standardized side-by-side comparison canvas with an interactive **Differential Chromatic Heatmap** ($|\Delta a^*|$) highlighting localized erythema attenuation.
3. **Clinician Triage & Consultation Summary:** Pharmacist/dermatologist annotation panel, progression assessment, recapture request triggers, and one-click printable **Standardized Consultation Summary (PDF/Print)**.
4. **Research Telemetry Drawer:** Isolated academic audit module computing Relative Chromatic Contrast ($RCC$), Individual Typology Angle ($ITA^\circ$), and GLCM texture statistics.
5. **Explainable Edge AI Lesion Delineation:** One-click CIELAB color-saliency contour extraction measuring calibrated surface area in $\text{mm}^2$ and circularity without black-box hallucination.
6. **Parametric 3D CAD Enclosure:** Production-ready OpenSCAD model (`cad/optichroma_enclosure_v2_4.scad`) and pre-compiled 3D mesh (`cad/optichroma_enclosure_v2_4.stl`) with 1.5mm anti-blanching recess and universal spring clamp.

---

## 2. Executive Summary & Brand Alignment

* **Brand:** **La Roche-Posay** (L'Oréal Dermatological Beauty Division)
* **Official Playing Field:** **Playing Field 3 — Reinvent the Doctor-Patient Relationship**
* **The Core Problem:** Smartphone skin photographs taken by patients or frontline healthcare providers frequently suffer from blinding specular glare, variable room lighting, camera motion blur, and optical color masking on deeper skin tones. Patients with chronic conditions (atopic dermatitis, eczema) struggle to track flare-ups objectively, while community pharmacists lack standardized optical tools to triage skin concerns.
* **The Solution:** **La Roche-Posay OptiChroma (v2.4)** combines an accessible, reusable cross-polarized optical attachment with an algorithmic quality gate, in-frame reference normalization, Relative Chromatic Contrast ($RCC$) scoring, and exploratory GLCM texture descriptors.
* **Status:** Frozen Student Proof-of-Concept MVP. Strictly non-diagnostic documentation tool.

```
+-----------------------------------------------------------------------------------+
|                        LA ROCHE-POSAY OPTICHROMA v2.4                             |
|                                                                                   |
|  [Hardware Attachment]             [Capture Pipeline]       [Clinical Portal]    |
|  * 35mm Optical Enclosure (rPC)      * Tier 2 JPEG / Raw Spec * Pharmacist Triage |
|  * Cross-Polarizers (Ext. >100:1)    * Tenengrad Sharpness    * Telederm Export   |
|  * High-CRI LEDs (CRI>95, 5000K)     * In-Frame Normalization * Longitudinal Trend|
|  * TI TPS61165 Boost Driver          * Specular Glare Gate    * Patient Summary   |
|  * Non-Compressive 1.5mm Standoff    * Side-by-Side Canvas    * Differential Map  |
+-----------------------------------------------------------------------------------+
```

---

## 3. Non-Negotiable Boundaries & Claims Governance

To maintain scientific honesty, regulatory feasibility, and clinical credibility, OptiChroma strictly adheres to defined boundaries:

| Prohibited Claim / Pseudoscience | Approved Scientific Capability (OptiChroma v2.4) |
| :--- | :--- |
| **NO Autonomous Diagnosis:** Does not diagnose melanoma, atopic dermatitis, or skin cancer. | **Clinical Documentation:** Standardized image capture, visual archiving, and decision-support triage. |
| **NO Spectrophotometer Claims:** Does not output absolute spectral reflectance curves ($\text{nm}^{-1}$). | **Reference-Assisted Normalization:** In-frame 18% neutral gray ceramic standard normalizes RGB gains. |
| **NO Hemoglobin / Melanin Quantification:** Does not measure blood volume, blood flow, capillary dilation, or melanin mass. | **Relative Chromatic Contrast ($RCC$):** Tracks relative chromatic shifts along the CIELAB red-green axis ($RCC = \overline{a^*}_{ROI} - \overline{a^*}_{ref}$). |
| **NO Skin Barrier / TEWL Measurement:** Does not quantify Transepidermal Water Loss ($\text{g/m}^2/\text{h}$). | **Exploratory GLCM Texture:** Quantifies 2D image roughness, homogeneity, and contrast across 16 quantized gray levels. |
| **NO 48–72h Flare Prediction:** Does not predict subclinical inflammatory flares days in advance. | **Longitudinal Trend Tracking:** Records and plots objective visual trajectories over days and weeks. |
| **NO 100% Glare Elimination:** Does not claim total extinction of all optical reflection. | **Verified Glare Suppression:** Orthogonal cross-polarization targets $\ge 75\%$ specular suppression. |
| **NO Fitzpatrick Equivalence:** ITA surface color categories do NOT determine Fitzpatrick phototypes. | **Descriptive Colorimetry:** ITA ($ITA^\circ$) categorizes surface skin reflectance objectively (Chardon et al., 1991). |

---

## 4. Hardware Specifications & Forensic Electrical Design

* **Optical Geometry:** Fixed working distance optical baffle ($35\text{ mm}$ internal standoff) with $60^\circ$ micro-fluted anti-reflective internal geometry.
* **Non-Compressive Standoff:** Annular contact rim with a $1.5\text{ mm}$ recessed internal optical aperture, distributing contact away from the central diagnostic field.
* **Cross-Polarization Engine:** Orthogonal linear polarizing films (extinction ratio $>100:1$, transmission $38\%$) positioned over the illumination source and camera sensor aperture.
* **Calibrated Illumination:** Dual high-CRI surface-mount LEDs ($5000\text{ K}$, $R_a \ge 95$, $R_9 \ge 90$) arranged in **series** and driven by a Texas Instruments TPS61165 boost constant-current driver ($R_{sense} = 4.02\,\Omega$, $L = 22\,\mu\text{H}$, $50.0\text{ mA} \pm 3\%$) to eliminate parallel current-hogging and battery-discharge dimming.
* **In-Frame Reference Standard:** Permanent $18\%$ neutral gray ceramic patch positioned on the internal aperture ring for real-time linear gain calibration.
* **Bill of Materials (BOM):** Student prototype build cost estimated at **~₹1,750 (~€19.00)**; preliminary target for mass production modeled at ~₹750–₹950 (~€8.00–€10.50).

---

## 5. Software Architecture & Automated Testing

The implementation is verified using `pytest`:

```bash
# Run the complete test suite
python -m pytest -v
```

### Test Suite Summary (50 Tests, 100% Pass)
* `tests/test_calibration.py`: 5 tests (patch detection, clipping flag, uniformity flag, gain scaling, fallback).
* `tests/test_chromatic_features.py`: 4 tests (contrast delta, zero difference, coordinate bounds, circular ROI masking).
* `tests/test_forensic_edge_cases.py`: 13 tests (1D/2D/4D shapes, empty arrays, unsupported dtypes, non-numpy inputs, missing patches, extreme gains, OOB ROIs, multi-resolution 200x200 to 2500x2500, constant images, invalid GLCM crops, ITA stability with $b^*=0$ and $b^*<0$).
* `tests/test_quality_gate.py`: 4 tests (invalid types, sharpness pass, blur rejection, saturation rejection).
* `tests/test_texture_features.py`: 3 tests (flat surface, high-contrast checkerboard, crop boundary handling).
* `tests/test_mvp_workflow.py`: 10 tests (record lifecycle, metadata timestamps, baseline validation, follow-up sequence, comparison canvas, consultation reports, research isolation).
* `tests/test_web_app.py`: 11 tests (SPA loading, preset listing, quality gate pass/reject endpoints, sample case loading, comparison image stream, differential heatmap stream, clinician annotations, research telemetry endpoint).
* **Result:** **50 passed in 1.47s (100% pass rate, 0 failures, 0 warnings)**.

---

## 6. Repository Layout

```
Loreal/
├── app.py                                    # Interactive Prototype Web Application (Flask)
├── requirements.txt                          # Project dependency specifications
├── OPTICHROMA_v2_4_ENGINEERING_AUDIT.md       # Independent engineering audit of all functions
├── OPTICHROMA_v2_4_HARDWARE_CALCULATIONS.md  # TPS61165 boost driver math & component selection
├── OPTICHROMA_v2_4_MVP_SPEC.md               # Frozen Student MVP specification
├── OPTICHROMA_v2_4_VALIDATION_PLAN.md        # 3-arm benchtop optical validation protocol
├── architecture/                             # Authoritative technical specifications
├── concept/                                  # Brand & user experience documentation
├── research/                                 # Scientific & competitive intelligence
├── src/                                      # Python implementation
│   ├── optichroma_v2_4_mvp.py                # MVP workflow, records, comparison & report export
│   ├── optichroma_v2_3_core.py               # Forensic core engine: quality gate, RCC, ITA, GLCM
│   ├── generate_presets.py                   # Realistic synthetic skin phantom generator
│   └── web_ui/                               # Prototype Web UI templates, presets, and styles
├── submission/                               # Brandstorm 2027 competition deliverables
│   ├── pitch-deck-content.md                 # 3-slide pitch deck content
│   └── video-script-outline.md               # 3-minute video presentation script
├── tests/                                    # 50 automated unit and integration tests
├── compile_dossier_pdf.py                    # Playwright PDF compiler script
└── LOREAL_BRANDSTORM_2027_OPTICHROMA_FINAL_DOSSIER.pdf # 41-page compiled master dossier
```

---

*L'Oréal Brandstorm 2027 | La Roche-Posay Innovation Taskforce*

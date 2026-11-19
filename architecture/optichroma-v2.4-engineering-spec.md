# La Roche-Posay OptiChroma v2.4 — Master Systems Architecture & MVP Engineering Spec

**Document Version:** 2.4.0  
**Status:** **FROZEN STUDENT MVP BASELINE (Evaluated & Audited)**  
**Brand Scope:** La Roche-Posay (L'Oréal Dermatological Beauty)  
**Competition Target:** L'Oréal Brandstorm 2027 — Playing Field 3: Reinvent the Doctor-Patient Relationship  
**System Classification:** Non-diagnostic, standardized optical imaging accessory and longitudinal clinical documentation platform.

---

## 1. System Architecture & Frozen MVP Boundary

The OptiChroma v2.4 architecture enforces a clear boundary between the core buildable student MVP and experimental research features:

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                                    OPTICHROMA v2.4 SYSTEM ARCHITECTURE                            |
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                                                                                                   |
|  [ PHYSICAL HARDWARE ATTACHMENT ]                                                                 |
|  ├── 3D-Printed Mechanical Baffle (Fixed 35.0 mm Working Distance, Annular Recessed Standoff)     |
|  ├── Dual High-CRI White LEDs (Nichia 757, 5000K, CRI >= 95, in Series String at 50 mA)         |
|  ├── Proposed Boost Driver (TI TPS61165 Constant-Current Regulator, R_sense = 4.02 Ω)            |
|  ├── Cross-Polarizing Engine (0° Illumination Polarizer, 90° Orthogonal Camera Analyzer)          |
|  └── In-Frame 18% Neutral Gray Ceramic Reference Target                                           |
|                                                                                                   |
|                                         │ Optical Alignment                                       |
|                                         ▼                                                         |
|  [ TIER 1 CAPTURE: STANDARDIZED MOBILE ENGINE ] (Google Pixel 7 / Samsung Galaxy S23)             |
|  ├── Android Camera2 API: Locked Exposure (1/50 s), Locked ISO (100), Manual Focus (35 mm)        |
|  └── Bypasses OEM sharpening, Dynamic Tone Mapping (DTM), and beautification filters             |
|                                                                                                   |
|                                         │ Ingest BGR / RAW Frame                                  |
|                                         ▼                                                         |
|  [ CORE STUDENT MVP PIPELINE (src/optichroma_v2_4_mvp.py) ]                                       |
|  ├── 1. Input Array Validation (Format, dimensions, memory integrity)                             |
|  ├── 2. Tenengrad Gradient Sharpness Focus Gate (T >= 85.0)                                       |
|  ├── 3. Specular Saturation (<0.8%) & Underexposure (<2.0%) Gate                                  |
|  ├── 4. Bounded Reference Normalization (von Kries scaling against in-frame 18% gray patch)        |
|  ├── 5. Longitudinal Observation Record (Baseline + Follow-up session management)                 |
|  ├── 6. Interactive Side-by-Side Visual Canvas (Pixel-aligned comparison with date banners)        |
|  ├── 7. Patient Symptom Notes & Capture Metadata Ingestion                                       |
|  └── 8. Shareable Structured Consultation Summary (Exportable JSON / HTML for clinicians)        |
|                                                                                                   |
|                                         │ Experimental Telemetry (Isolated)                       |
|                                         ▼                                                         |
|  [ ISOLATED RESEARCH MODULE (OptiChromaResearchModule) ]                                          |
|  ├── Experimental Relative Chromatic Contrast: RCC = mean(a*_ROI) - mean(a*_ref)                  |
|  ├── Research Individual Typology Angle: ITA° surface colorimetry (Chardon et al., 1991)          |
|  └── Research GLCM Texture Descriptors: 16-level quantized Contrast, Homogeneity, Energy          |
|                                                                                                   |
+───────────────────────────────────────────────────────────────────────────────────────────────────+
```

---

## 2. Non-Negotiable Boundaries & Prohibited Capabilities

OptiChroma v2.4 strictly adheres to defined boundaries to maintain scientific honesty and clinical credibility:

1. **NOT an Autonomous Diagnostic Tool:** Does not diagnose melanoma, eczema, psoriasis, or any skin malignancy.
2. **NOT a Medical Spectrophotometer:** Does not output absolute spectral reflectance curves ($\text{nm}^{-1}$).
3. **NOT a Hemoglobin, Blood Flow, or Inflammation Meter:** $RCC$ is strictly an image-chromatic difference ($\Delta a^*$) along the red-green opponent axis. It is NOT an assay of blood volume, blood flow, capillary dilation, or vascular inflammation.
4. **NOT a Skin-Barrier or TEWL Instrument:** GLCM metrics are 2D pixel-pattern descriptors. They do NOT quantify Transepidermal Water Loss ($\text{g/m}^2/\text{h}$) or stratum corneum lipid integrity.
5. **NO Flare Prediction Guarantees:** Does not predict subclinical inflammatory flares days in advance.
6. **NO 100% Glare Elimination Claims:** Uses cross-polarization to achieve a targeted design goal of $>75\%$ specular reflection suppression on sebum-rich surfaces; residual oblique leakage is acknowledged.
7. **NO Fitzpatrick Phototype Claims:** $ITA^\circ$ is descriptive surface colorimetry, NOT a clinical Fitzpatrick phototype classification.

---

## 3. Physical Hardware Architecture & Verified Driver Selection

### 3.1 Mechanical Optical Enclosure
* **Fixed Working-Distance Enclosure:** $35.0 \pm 0.5\text{ mm}$ internal clearance between camera lens and skin plane.
  * *Critical Terminology Distinction:* This fixes the **working distance**, NOT the focal distance. Mobile cameras utilize voice-coil motor (VCM) autofocus; holding the physical distance constant constrains the field of view (FOV) and allows autofocus to lock sharply without hunting.
* **Non-Compressive Standoff:** Annular contact rim ($32\text{ mm}$ outer diameter) with the central optical aperture recessed by **$1.5\text{ mm}$**. All normal positioning pressure is displaced to the outer contact boundary, leaving the central $20\text{ mm}$ diagnostic field uncompressed to prevent microvascular capillary blanching.

### 3.2 Inductive Step-Up (Boost) Illumination Driver: TI TPS61165
Following a comparative evaluation against the Microchip MCP1643 (which failed due to its $5.0\text{V}$ output ceiling), the **Texas Instruments TPS61165** was selected:

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                                  TPS61165 PROPOSED BOOST DRIVER SCHEMATIC                         |
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                                                                                                   |
|     +3.0V to +4.2V (LiPo)                                                                         |
|     ───────┬───────────────────────┬──────────────────────────────┐                               |
|            │                       │                              │                               |
|          ┌─┴──┐                  ┌─┴──┐                         ┌─┴──┐ L1                         |
|          │ C1 │ 10uF             │ C2 │ 100nF                   │    │ 22uH (Murata LQH3NPN)      |
|          │    │ 16V X5R          │    │ 16V X7R                 └──┬─┘                            |
|          └─┬──┘                  └─┬──┘                            │                              |
|            │                       │                               ├──────────────┐               |
|            ▼ GND                   ▼ GND                           │              │               |
|                                                                  ┌─┴──┐         ┌─┴──┐ D1         |
|                                                                  │ SW │         │    │ B0520WS    |
|                          ┌───────────────────────────┐           │Pin1│         │    │ Schottky   |
|                          │      TI TPS61165          │           └─┬──┘         └──┬─┘            |
|                          │                           │             │               │              |
|          V_IN ───────────┤ VIN (Pin 6)               │             │               ├──────┐       |
|                          │                           │             │               │      │       |
|          Pulse Enable ───┤ CTRL (Pin 4)              │             │             ┌─┴──┐ ┌─┴──┐    |
|          (800 ms pulse)  │                           │             │             │ C3 │ │ C4 │    |
|                          │               FB (Pin 3)  ├─────────────┼────────┐    │2.2u│ │100n│    |
|                          │                           │             │        │    └─┬──┘ └─┬──┘    |
|                          │               GND (Pin 2) ├────────┐    │        │      │      │       |
|                          └───────────────────────────┘        │    │        │      ▼ GND  ▼ GND   |
|                                                               │    │        │                     |
|                                                               ▼    ▼        │  +6.2V Out          |
|                                                              GND  GND       │     │               |
|                                                                             │   ┌─┴────────────┐  |
|                                                                             │   │ LED1 (5000K) │  |
|                                                                             │   │ Nichia 757   │  |
|                                                                             │   └─┬────────────┘  |
|                                                                             │     │               |
|                                                                             │   ┌─┴────────────┐  |
|                                                                             │   │ LED2 (5000K) │  |
|                                                                             │   │ Nichia 757   │  |
|                                                                             │   └─┬────────────┘  |
|                                                                             │     │               |
|                                                                             └─────┼───────────────┤
|                                                                                   │               |
|                                                                                 ┌─┴──┐            |
|                                                                                 │ R1 │ R_sense    |
|                                                                                 │    │ 4.02 Ω 1%  |
|                                                                                 └─┬──┘            |
|                                                                                   │               |
|                                                                                   ▼ GND           |
+───────────────────────────────────────────────────────────────────────────────────────────────────+
```

* **Sense Resistor:** $R_{sense} = V_{FB} / I_{LED} = 0.200\text{V} / 0.050\text{A} = 4.00\,\Omega$ (Selected: $4.02\,\Omega$, 1%, 0805).
* **Inductor:** $22\,\mu\text{H}$ power inductor (Murata LQH3NPN220MM0L, $I_{sat} = 0.65\text{A}$).
* **Current Stability:** Series connection guarantees identical current through both LEDs, operating stably across the entire LiPo discharge curve ($4.2\text{V} \to 3.0\text{V}$).

---

## 4. Minimum Demonstrable Software Implementation

The complete student workflow is implemented in [`src/optichroma_v2_4_mvp.py`](file:///c:/Users/nithin.reddy/Desktop/Loreal/src/optichroma_v2_4_mvp.py):

* **`SkinObservationRecord`:** Manages patient pseudonym, anatomical location, verified baseline, and follow-up images.
* **`CaptureMetadata`:** Stores timestamp, device model, ISO, exposure time, acquisition mode (`TIER1_RAW` or `TIER2_JPEG`), and notes.
* **Quality Gate Verification:** Rejects blurred captures ($T < 85.0$) and saturated glare ($>0.8\%$).
* **Side-by-Side Comparison:** Generates unified comparison canvas with date banners and separator bar.
* **Consultation Report:** Outputs structured, non-diagnostic JSON summary with full metadata and disclaimers.
* **Isolated Research Module:** Provides access to experimental RCC, research ITA, and research GLCM.

---

## 5. Automated Unit Test Verification

The codebase is verified across 42 unit tests with a **100% pass rate**:

```
tests/test_calibration.py (5 tests): Patch detection, clipping, uniformity, gain scaling, fallback
tests/test_chromatic_features.py (4 tests): Contrast delta, zero contrast, bounds, circular ROI mask
tests/test_forensic_edge_cases.py (13 tests): 1D/2D/4D shapes, empty arrays, unsupported dtypes, non-numpy inputs,
    missing patches, extreme gains, OOB ROIs, multi-resolution (200x200 to 2500x2500), constant images,
    invalid GLCM crops, ITA numerical stability with b*=0 and b*<0
tests/test_mvp_workflow.py (10 tests): Record init, baseline rejection/acceptance, follow-up sequencing,
    patient notes, clinician annotations/recapture, side-by-side rendering, consultation report, research isolation
tests/test_quality_gate.py (4 tests): Invalid inputs, sharp pattern pass, blur reject, saturation reject
tests/test_texture_features.py (3 tests): Flat texture, high-contrast pattern, invalid crop box
============================== 42 passed in 1.63s ==============================
```

*Governance Note:* These 42 unit tests verify that the Python code executes as written on synthetic arrays; they do NOT constitute proof of physical optical performance on human skin.

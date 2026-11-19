# OptiChroma v2.4 — Student MVP Specification & Feature Freeze

**Document ID:** `OPTICHROMA_v2_4_MVP_SPEC.md`  
**System:** La Roche-Posay OptiChroma (v2.4 MVP Freeze)  
**Authors:** Systems Architecture & Clinical Software Taskforce  
**Status:** **FROZEN STUDENT MVP BASELINE**  
**Classification:** Non-Diagnostic Optical Capture & Visual Consultation Platform

---

## 1. Executive Summary & MVP Scope Freeze

To ensure that a team of three computer science students can build, test, and physically demonstrate a functional proof-of-concept, the **OptiChroma v2.4 MVP is frozen**.

All speculative features, diagnostic classifiers, and unbuilt integrations are excluded from the core product.

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                                    OPTICHROMA v2.4 MVP BOUNDARY                                   |
+───────────────────────────────────────────────────+───────────────────────────────────────────────+
| INCLUDED IN FROZEN MVP                            | EXCLUDED / ISOLATED TO RESEARCH               |
+───────────────────────────────────────────────────+───────────────────────────────────────────────+
| 1. Standardized 35mm physical capture enclosure.  | • Autonomous disease diagnosis.               |
| 2. Cross-polarized surface glare suppression.     | • Prescription or treatment recommendations.  |
| 3. Blur & exposure quality gate (Tenengrad).      | • Flare prediction (48–72h).                  |
| 4. In-frame reference-assisted exposure balance.  | • Absolute hemoglobin or melanin measurement. |
| 5. Longitudinal Baseline & Follow-up storage.     | • Skin barrier / TEWL quantification.         |
| 6. Interactive side-by-side comparison canvas.    | • Complex deep neural networks.               |
| 7. User symptom notes & timestamped metadata.     | • Unbuilt EHR/FHIR hospital server pipelines. |
| 8. Shareable consultation summary report.         | • RCC (Isolated as Experimental Feature).     |
| 9. Clinician review annotation & recapture flag.  | • ITA & GLCM (Isolated in Research Module).   |
+───────────────────────────────────────────────────+───────────────────────────────────────────────+
```

---

## 2. Two-Tier Camera Acquisition Architecture

OptiChroma establishes two distinct acquisition tiers, distinguishing calibrated raw sensor ingestion from consumer web fallbacks:

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                                   ACQUISITION TIER ARCHITECTURE                                   |
+───────────────────────────────────────────────────+───────────────────────────────────────────────+
| TIER 1: NATIVE ANDROID RAW/DNG (Standardized)     | TIER 2: RENDERED JPEG (Best-Effort Consumer)  |
+───────────────────────────────────────────────────+───────────────────────────────────────────────+
| Target Device: Google Pixel 7 / Samsung Galaxy S23| Any modern smartphone browser (Chrome/Safari) |
| Format: 10-bit / 12-bit RAW_SENSOR (DNG)          | Format: Compressed 8-bit sRGB (JPEG/PNG)      |
| Exposure: Manually locked at 1/50 s (20 ms)       | Exposure: Best-effort WebRTC constraints      |
| ISO Sensitivity: Manually locked at ISO 100       | ISO: Auto-adjusted by OS camera service       |
| Focus: Locked at fixed 35.0 mm working distance   | Focus: Autofocus with reticle positioning     |
| White Balance: Locked 1:1 sensor gains (5000K)    | White Balance: Dynamic OEM auto-white-balance |
| Bypasses: OEM sharpening, DTM, beauty filters     | Subject to: Proprietary tone curves & smoothing|
+───────────────────────────────────────────────────+───────────────────────────────────────────────+
```

### 2.1 Tier 1: Recommended Reference Hardware Configuration
For the initial physical MVP demonstration, universal smartphone compatibility is **NOT promised**. A single reference device configuration is standardized:
* **Recommended Hardware:** **Google Pixel 7** running Android 14 (or Samsung Galaxy S23).
  * Justification: Full hardware support for Camera2 `LEVEL_3` / `FULL` capabilities, robust DNG metadata exposure, reliable manual exposure locking, and documented sensor spectral characteristics.
* **Locked Capture Settings:**
  * Exposure Time: $1/50\text{ s}$ ($20,000,000\text{ ns}$) to freeze hand tremor while eliminating $50/60\text{ Hz}$ room flicker.
  * ISO Gain: Locked at native base sensitivity (ISO 100).
  * Lens Focus: Manual focus locked at diopter value matching $35.0\text{ mm}$ ($28.5\text{ diopters}$).
  * Illumination: Synchronized $800\text{ ms}$ pulse from dual series Nichia 757 LEDs ($5000\text{ K}$, CRI 95+).

### 2.2 Tier 1: Step-by-Step RAW Pipeline
1. **DNG Ingestion:** Read raw Bayer frame via `rawpy` or Android `DngCreator`.
2. **Black-Level Subtraction:** Extract sensor black-level pedestal ($DN_{black}$) from DNG metadata and subtract: $I_{linear} = \max(I_{raw} - DN_{black}, 0) / (DN_{white} - DN_{black})$.
3. **Linear Demosaicing:** Convert 1-channel Bayer CFA to 3-channel linear RGB using Adaptive Homogeneity-Directed (AHD) or Malvar-He-Cutler interpolation.
4. **Daylight White Balance:** Apply camera sensor white-balance multipliers calibrated for $5000\text{ K}$.
5. **Color Transformation:** Apply $3\times3$ Color Correction Matrix (`ColorMatrix1` from DNG metadata) to convert camera native RGB to standardized linear sRGB.
6. **Analysis Color Space Conversion:** Convert linear sRGB to CIELAB under $D_{65}$ standard illuminant.

### 2.3 Tier 2: Rendered JPEG Limitations & Disclaimers
When captures originate from standard browser WebRTC:
* **Limitations Documented:** Irreversible non-linear tone curves, dynamic contrast boosting, 8-bit quantization loss, and chroma subsampling are baked into the image.
* **Mandatory Watermark:** All reports generated via Tier 2 carry an explicit header:  
  *"TIER 2 CAPTURE — Rendered with consumer OEM tone curves. Suitable for visual comparison only. Device-independent colorimetry unvalidated."*

---

## 3. Patient–Clinician Minimum Demonstrable Workflow

Implemented and unit-tested in `src/optichroma_v2_4_mvp.py`:

```
[ STEP 1: INITIALIZE RECORD ]
Patient creates skin record with pseudonym & anatomical site (e.g. "Patient_AB12", "Left Forearm").
               │
               ▼
[ STEP 2: BASELINE CAPTURE ]
Patient clips OptiChroma attachment and captures baseline image under standardized illumination.
               │
               ▼
[ STEP 3: QUALITY GATE EVALUATION ]
System computes Tenengrad focus (T >= 85.0) and checks specular saturation (< 0.8%).
├── FAIL: Rejects capture with guidance ("Hold steady; ensure enclosure is flush").
└── PASS: Stores verified Baseline frame with ISO, exposure time, and timestamp metadata.
               │
               ▼
[ STEP 4: PATIENT SYMPTOM LOGGING ]
Patient adds contextual observation notes (e.g., "Mild itching, day 3 of new moisturizer").
               │
               ▼
[ STEP 5: FOLLOW-UP CAPTURE ]
7 days later, patient captures follow-up image under identical optical geometry. Quality gate verifies frame.
               │
               ▼
[ STEP 6: SIDE-BY-SIDE VISUAL CANVAS ]
App renders standardized comparison canvas (Baseline vs. Follow-up) with date banners and fixed scale.
               │
               ▼
[ STEP 7: SHAREABLE CONSULTATION REPORT ]
Generates structured JSON / HTML consultation summary with verified images, timestamps, and notes.
               │
               ▼
[ STEP 8: CLINICIAN REVIEW & ANNOTATION ]
Dermatologist or pharmacist reviews record; logs review comments or flags a recapture request.
```

---

## 4. Isolated Research Module (Excluded from MVP Product UI)

To protect clinical safety and maintain regulatory boundaries, experimental analytical features are strictly isolated from the consumer/clinical user interface into `OptiChromaResearchModule`:

1. **Experimental Relative Chromatic Contrast ($RCC$):**
   * Computes $RCC = \overline{a^*}_{ROI} - \overline{a^*}_{ref}$.
   * Displayed exclusively in the engineering research tab with the notice: *"Experimental image-chromatic metric. Not a measure of hemoglobin or inflammation."*
2. **Research Individual Typology Angle ($ITA^\circ$):**
   * Computes surface colorimetry angle from reference skin.
   * Tagged: *"Descriptive colorimetry only (Chardon et al., 1991). Does not determine Fitzpatrick phototype."*
3. **Research GLCM Texture Descriptors:**
   * Computes Contrast, Homogeneity, and Energy on standardized 16-level crops.
   * Tagged: *"Exploratory 2D pixel texture. Does not measure skin barrier lipids or TEWL."*

---

## 5. Technical Deliverables Summary

* **Core Python Engine:** [`src/optichroma_v2_4_mvp.py`](file:///c:/Users/nithin.reddy/Desktop/Loreal/src/optichroma_v2_4_mvp.py)
* **Automated Unit Tests:** [`tests/test_mvp_workflow.py`](file:///c:/Users/nithin.reddy/Desktop/Loreal/tests/test_mvp_workflow.py) (10 tests, 100% pass)
* **Engineering Audit:** [`OPTICHROMA_v2_4_ENGINEERING_AUDIT.md`](file:///c:/Users/nithin.reddy/Desktop/Loreal/OPTICHROMA_v2_4_ENGINEERING_AUDIT.md)
* **Electrical Calculations:** [`OPTICHROMA_v2_4_HARDWARE_CALCULATIONS.md`](file:///c:/Users/nithin.reddy/Desktop/Loreal/OPTICHROMA_v2_4_HARDWARE_CALCULATIONS.md)
* **Optical Validation Plan:** [`OPTICHROMA_v2_4_VALIDATION_PLAN.md`](file:///c:/Users/nithin.reddy/Desktop/Loreal/OPTICHROMA_v2_4_VALIDATION_PLAN.md)

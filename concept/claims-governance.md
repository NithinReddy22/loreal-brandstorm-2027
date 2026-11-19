# Claims Governance & Scientific Boundaries Framework

**Document Version:** 2.3.0  
**System:** La Roche-Posay OptiChroma (v2.3)  
**Audience:** Brandstorm Presenters, Engineering Team, Competition Judges  
**Status:** Mandatory Governance Baseline

---

## 1. The Core Scientific Boundary

In competitive innovation competitions, teams frequently succumb to "claim inflation"—making exaggerated biomedical assertions to impress non-technical jurors. 

In L'Oréal Brandstorm, **clinical dermatologists and senior research executives sit on the judging panel**. Exaggerated or unscientific claims lead to immediate loss of credibility and disqualification.

OptiChroma's core strength is **scientific integrity**. Every claim must be traceable to established optical physics, calibrated computer vision, or clearly labeled exploratory engineering parameters.

---

## 2. The Six Strictly Prohibited Claims

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                                    PROHIBITED SCIENTIFIC CLAIMS                                   |
+----+----------------------------------+-----------------------------------------------------------+
| #  | PROHIBITED PHRASE / CLAIM        | WHY IT IS SCIENTIFICALLY UNACCEPTABLE                     |
+----+----------------------------------+-----------------------------------------------------------+
| 01 | "Turns phone into a clinical-    | A phone camera possesses broad RGB Bayer spectral bands   |
|    | grade spectrophotometer"         | (~100nm FWHM), not narrow monochromatic measurement bands.|
+----+----------------------------------+-----------------------------------------------------------+
| 02 | "Measures pure hemoglobin, blood | Consumer RGB sensors cannot invert an uncalibrated matrix |
|    | flow, or inflammation"           | to separate overlapping chromophores deterministically.   |
+----+----------------------------------+-----------------------------------------------------------+
| 03 | "Measures epidermal barrier      | Barrier function and lipid depletion require TEWL         |
|    | integrity or lipid loss (TEWL)"  | evaporimetry or corneometry; image texture cannot assay it|
+----+----------------------------------+-----------------------------------------------------------+
| 04 | "Predicts eczema/acne flares     | Eczema flare cascades involve complex immunobiology;      |
|    | 48 to 72 hours in advance"       | OptiChroma tracks visible changes over time, not flares.  |
+----+----------------------------------+-----------------------------------------------------------+
| 05 | "100% specular glare extinction  | Optical cross-polarization significantly suppresses glare;|
|    | and exclusive dermal imaging"    | it does not extinguish 100% of surface photons.           |
+----+----------------------------------+-----------------------------------------------------------+
| 06 | "Autonomous AI diagnostic and    | OptiChroma is NOT a diagnostic medical device; it supports|
|    | automated prescription engine"   | clinical consultation and structured patient tracking.    |
+----+----------------------------------+-----------------------------------------------------------+
```

---

## 3. Approved & Defensible Capabilities

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                                  APPROVED & DEFENSIBLE CAPABILITIES                               |
+----+----------------------------------+-----------------------------------------------------------+
| #  | APPROVED PHRASE / CLAIM          | EMPIRICAL JUSTIFICATION & TESTING METHOD                  |
+----+----------------------------------+-----------------------------------------------------------+
| 01 | "Standardized optical smartphone | Enforces fixed working distance (35mm), uniform series    |
|    | capture enclosure"               | LED illumination, and in-frame color reference target.    |
+----+----------------------------------+-----------------------------------------------------------+
| 02 | "Cross-polarization surface      | Dual linear polarizers (0° and 90°) target >=75% glare    |
|    | specular glare suppression"      | suppression, subject to benchtop phantom verification.    |
+----+----------------------------------+-----------------------------------------------------------+
| 03 | "Automated image-quality gate    | Programmatically rejects motion-blurred captures using    |
|    | and capture rejection"           | Tenengrad gradient energy and checks specular clipping.   |
+----+----------------------------------+-----------------------------------------------------------+
| 04 | "Relative Chromatic Contrast     | Computes Delta a* between user ROI and reference skin in  |
|    | (RCC) in CIELAB color space"     | standardized CIELAB space as an objective color metric.   |
+----+----------------------------------+-----------------------------------------------------------+
| 05 | "Standardized longitudinal visual| Provides calibrated side-by-side comparison tools for     |
|    | documentation and care support"  | patients, pharmacists, and clinicians.                    |
+----+----------------------------------+-----------------------------------------------------------+
```

---

## 4. Approved Technical Glossary

* **Relative Chromatic Contrast (RCC):** Defined as $RCC = \overline{a^*}_{ROI} - \overline{a^*}_{reference}$. A relative image-color difference along the CIELAB red-green chromatic axis. **Never** call it a "Vascular Index", "Hemoglobin Score", or "Inflammation Meter."
* **Exploratory Individual Typology Angle (ITA):** Computed from normalized $L^*$ and $b^*$ coordinates to describe surface chromatic category (Chardon et al., 1991). **Never** equate ITA to Fitzpatrick skin phototypes (which reflect genetic UV erythema and tanning reactivity). It is NOT a clinical or diagnostic classification.
* **GLCM Image Texture Descriptors:** Contrast, Homogeneity, and Energy calculated from standardized $256\times256$ grayscale pixel co-occurrences. Always describe as mathematical image-texture descriptors, never as biological skin barrier or TEWL measurements.
* **Fixed Working-Distance Enclosure:** A physical light-baffle spacing the phone 35mm from the skin. Never call it a "fixed-focal-distance system," as camera autofocus systems operate dynamically.
* **Non-Compressive Standoff:** A 1.5mm recessed contact rim that distributes pressure away from the central skin aperture, reducing vascular blanching.
* **Reference-Assisted Normalization:** Linear channel gain scaling using an in-frame gray standard. Clearly distinguish this from camera-specific color correction matrices (CCM) or traceable colorimetric calibration.
* **Software Verification vs. Physical Evidence:** The 32 automated unit tests verify software execution on synthetic arrays; they do NOT prove physical optical performance on human skin.

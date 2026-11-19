# La Roche-Posay OptiChroma v2.3 — Laboratory Verification & Validation Protocol

**Document Version:** 2.3.0  
**Status:** Evaluated Laboratory Protocol (Forensic Edition)  
**Scope:** Benchtop Optical Verification, Algorithmic Quality Gates, and Non-Invasive Demonstrations  
**Safety & Ethics Governance:** Strictly Non-Invasive. No unsupervised clinical, hemodynamic, or ischemic cuff interventions.

---

## 1. Protocol Overview & Objectives

This protocol defines the experimental and benchtop testing procedures to evaluate the physical, optical, and computational performance of the **La Roche-Posay OptiChroma (v2.3)** proof-of-concept attachment.

The protocol separates theoretical targets from verified data across five objectives:
1. **Benchtop Glare Suppression:** Quantifying specular highlight reduction on artificial synthetic skin phantoms.
2. **Static Repeatability & Measurement Precision:** Evaluating instrument noise floor and repositioning consistency.
3. **Image Quality Gate Tuning:** Calibrating Tenengrad gradient thresholds against controlled optical defocus.
4. **Multi-Skin-Tone Exploratory Observations:** Characterizing optical signal behavior across diverse skin tones without equating ITA to Fitzpatrick types.
5. **Safe, Non-Invasive Optical Capture Demonstration:** Demonstrating relative chromatic contrast tracking on physical color targets and healthy superficial skin without medical interventions.

---

## 2. Protocol 1: Benchtop Glare Suppression Assessment

### 2.1 Objective
Empirically test the **proposed engineering target** of achieving $\ge 75\%$ reduction in saturated specular reflection area ($GSE \ge 75\%$) using orthogonal linear cross-polarization compared to unpolarized capture.

### 2.2 Apparatus & Materials
* **Substrate:** Bio-mimetic polyurethane/silicone skin phantoms of light and dark baseline tones.
* **Sebum Simulant:** Cosmetic-grade squalene or mineral oil applied at $2.0\text{ mg/cm}^2$ using a micropipette and spread uniformly.
* **Imaging Systems:** OptiChroma prototype (cross-polarized) versus an identical unpolarized enclosure (polarizers removed).
* **Camera Setup:** Smartphone running manual exposure lock (ISO 50, $1/50\text{ s}$, neutral balance).

### 2.3 Analysis & Engineering Target
* **Metric:** Saturated Pixel Fraction ($SPF = N_{sat} / N_{total} \times 100\%$, where $N_{sat}$ is count of pixels with any channel $\ge 254$).
* **Glare Suppression Efficiency:**
  $$GSE = \left( 1 - \frac{SPF_{polarized}}{SPF_{unpolarized}} \right) \times 100\%$$
* **Current Status:** **Proposed Engineering Target (Unverified)**. Literature values for cross-polarization indicate high specular rejection, but physical verification with the 3D prototype must be conducted and logged.

---

## 3. Protocol 2: Static Repeatability & Measurement Precision

### 3.1 Objective
Establish the measurement precision and instrument noise floor of Relative Chromatic Contrast ($RCC$) and Individual Typology Angle ($ITA^\circ$).

### 3.2 Test Conditions
* **Test Condition A (Static Stationary):** Attachment clamped rigidly over a static GretagMacbeth ColorChecker skin tone patch; 10 consecutive captures acquired over 5 minutes (tests optical/sensor noise and thermal stability).
* **Test Condition B (Manual Repositioning):** Attachment manually placed, captured, removed, and repositioned 10 times by an operator on a static test target.

### 3.3 Proposed Repeatability Targets
* **Within-Subject Standard Deviation ($s_w$):**
  $$s_w = \sqrt{\frac{1}{K(M-1)} \sum_{k=1}^K \sum_{m=1}^M (x_{km} - \bar{x}_k)^2}$$
* **Proposed Target Thresholds:**
  * Static Stationary Target: $s_w(RCC) \le 0.15$ CIELAB units.
  * Manual Repositioning Target: $s_w(RCC) \le 0.40$ CIELAB units.
* **Current Status:** **Proposed Engineering Target (Unverified)**. Derived as a desired instrument repeatability limit relative to the human perceptual Just Noticeable Difference ($\Delta a^* \approx 1.5\text{--}2.0$). Must be experimentally established with physical prototype captures.

---

## 4. Protocol 3: Image Quality Gate (IQG) Threshold Tuning

### 4.1 Objective
Calibrate the Tenengrad gradient threshold $T_{thresh}$ to reject operator motion blur and hand tremor on actual smartphone camera sensors.

### 4.2 Procedure
1. Mount the smartphone on an optical translation stage.
2. Acquire standardized captures of high-contrast test targets at optimal focus, and under controlled defocus steps ($\pm 0.5\text{ mm}$, $\pm 1.0\text{ mm}$, $\pm 1.5\text{ mm}$, $\pm 2.0\text{ mm}$).
3. Calculate the Tenengrad gradient energy:
   $$T = \frac{1}{N} \sum_{x,y} \left( (I * S_x)^2 + (I * S_y)^2 \right)$$
4. Plot gradient score vs. defocus distance to establish an empirically verified threshold for the specific smartphone camera model.
* **Current Status:** The software threshold ($T = 85.0$) is an initial heuristic default verified in code; empirical benchtop tuning per camera sensor is required.

---

## 5. Protocol 4: Multi-Skin-Tone Exploratory Observations

### 5.1 Objective
Characterize the optical signal-to-noise ratio and dynamic range of Relative Chromatic Contrast ($RCC$) across diverse skin tones under cross-polarization.

### 5.2 Scientific Governance & Terminology Safeguards
* **No Diagnostic or Fitzpatrick Equivalence:** Skin tone observations must use objective, image-derived surface colorimetry ($ITA^\circ$ angles) per Chardon et al. (1991).
* **Never Equate ITA to Fitzpatrick Types:** Fitzpatrick phototype depends on genetic UV erythema and tanning reactivity, which cannot be inferred from surface reflectance.
* **Transparent Optical Limitations:** On deeply pigmented skin ($ITA^\circ \le -30^\circ$), epidermal melanin acts as a neutral optical absorber, attenuating dermal reflectance. While cross-polarization removes surface glare equally across all skin tones, the chromatic contrast dynamic range ($\Delta a^*$) is physically compressed on darker skin. This physical constraint must be documented transparently rather than claiming fictitious optical parity.

---

## 6. Protocol 5: Safe, Non-Invasive Optical Capture Demonstration

### 6.1 Safety & Ethics Notice
* **Removal of Ischemic Occlusion:** The previously proposed 3-minute 180 mmHg forearm cuff-occlusion protocol has been **completely removed**. Students must NOT perform prolonged vascular or ischemic interventions on themselves or others without formal Institutional Review Board (IRB) or clinical ethics oversight.
* **Permitted Demonstration:** A simple, non-invasive optical imaging demonstration designed to confirm that OptiChroma can record and display relative image-chromatic differences under controlled optical conditions.

### 6.2 Demonstration Option A: Benchtop Multi-Illumination Target Test
1. Place a calibrated multi-patch skin-tone chart (ColorChecker) under three challenging ambient lighting environments:
   * Direct incandescent light (strong warm directional glare).
   * Overhead cool fluorescent light (diffuse flickering ambient).
   * Low ambient shadow (<50 lux).
2. Capture images with an unassisted smartphone versus the OptiChroma attachment.
3. Demonstrate that:
   * The optical baffle and cross-polarizers exclude ambient glare.
   * In-frame reference normalization stabilizes digital counts across varied ambient lighting.

### 6.3 Demonstration Option B: Non-Invasive Normal Skin Color Comparison
1. Healthy volunteer rests forearm on a flat surface in a temperature-controlled room.
2. OptiChroma captures a standardized image of the lighter inner forearm (volar) and a neighboring region (dorsal).
3. The software computes Relative Chromatic Contrast ($RCC$) and exploratory $ITA^\circ$ color categories.
4. **Deliverable:** Confirms the end-to-end functionality of the physical attachment, quality gate, reference normalization, and CIELAB feature extraction.
5. **Strict Boundary:** The demonstration is presented strictly as a proof of optical imaging stability and relative color calculation—NOT as a medical diagnosis or vascular assay.

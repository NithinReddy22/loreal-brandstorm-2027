# OptiChroma v2.4 — Benchtop Optical Validation Plan & Measurement Protocol

**Document ID:** `OPTICHROMA_v2_4_VALIDATION_PLAN.md`  
**System:** La Roche-Posay OptiChroma (v2.4 MVP Freeze)  
**Authors:** Optical Systems Engineering Taskforce  
**Status:** **PROPOSED BENCHTOP PROTOCOL (Pending physical execution)**  
**Classification:** Experimental Validation Plan & Data Collection Template

---

## 1. Objective & Scope

This protocol defines the exact experimental setup, apparatus, measurement metrics, and data collection procedures required to empirically validate the optical performance of the OptiChroma prototype.

The protocol provides an objective 3-arm comparative evaluation:
* **Arm A (Baseline Smartphone):** Bare consumer smartphone camera under typical ambient lighting, with standard camera flash/torch.
* **Arm B (OptiChroma Non-Polarized):** Smartphone mounted to the OptiChroma 35 mm optical baffle with dual 5000K LEDs, but with linear polarizing sheets removed (unpolarized).
* **Arm C (OptiChroma Cross-Polarized):** Full OptiChroma configuration with orthogonal linear polarizers ($0^\circ$ illumination, $90^\circ$ analyzer).

---

## 2. Experimental Apparatus & Controlled Parameters

### 2.1 Fixed Camera Hardware & Acquisition Settings
To eliminate inter-device variability, all arms must utilize a single reference smartphone mounted to a laboratory tripod:
* **Reference Smartphone:** Google Pixel 7 (Android 14) or Samsung Galaxy S23.
* **Camera API:** Android `Camera2` in manual lock mode (`CONTROL_AE_MODE_OFF`, `CONTROL_AF_MODE_OFF`, `CONTROL_AWB_MODE_OFF`).
* **Sensor Sensitivity (ISO):** Locked at ISO 100.
* **Exposure Time ($t_{exp}$):** Locked at $1/50\text{ s}$ ($20.0\text{ ms}$).
* **Focus Distance:** Locked manually at $35.0\text{ mm}$ working distance.
* **White Balance:** Locked at neutral 1:1 sensor multipliers ($5000\text{ K}$).

### 2.2 Physical Test Targets
1. **Target 1 — Matte Reference:** GretagMacbeth / Calibrite ColorChecker Classic (Patches 1–4: skin tone and neutral gray standards, specular gloss $< 2.0\text{ GU}$).
2. **Target 2 — Synthetic Dry Skin Phantom:** Polyurethane skin-mimicking model (Fitzpatrick II and V equivalents, Shore 20A durometer).
3. **Target 3 — Synthetic Oiled Skin Phantom (High Glare):** Identical polyurethane phantom coated with cosmetic-grade squalene (or pharmaceutical mineral oil) applied at exactly $2.0\text{ mg/cm}^2$ using a micropipette and spread with a lint-free roller to simulate heavy sebum shine.

### 2.3 Environmental Controls
* **Ambient Lighting 1 (Darkroom):** Optical laboratory with ambient illumination $< 0.5\text{ lux}$ (measures pure system performance).
* **Ambient Lighting 2 (Fluorescent Room Light):** Standard commercial overhead fluorescent lighting ($400\text{--}500\text{ lux}$, $4000\text{ K}$).

---

## 3. Evaluated Metrics & Mathematical Formulations

### 3.1 Metric 1: Saturated Highlight Pixel Fraction ($SPF$)
Quantifies the percentage of pixels within the central biological aperture that suffer from specular flash clipping:
$$N_{sat} = \sum_{x,y \in ROI} \mathbf{1}\left( \max(R(x,y), G(x,y), B(x,y)) \ge 254 \right)$$
$$SPF = \frac{N_{sat}}{N_{ROI}} \times 100\%$$
* **Proposed Target (Unverified):** Cross-polarization (Arm C) targets $\ge 75\%$ reduction in $SPF$ compared to non-polarized capture (Arm B) on Target 3.

### 3.2 Metric 2: Mean Image Intensity & Channel Dispersion
Evaluates the optical transmission loss introduced by the polarizing filters:
$$\mu_c = \frac{1}{N_{ROI}} \sum_{x,y \in ROI} I_c(x,y), \quad \sigma_c = \sqrt{\frac{1}{N_{ROI}} \sum_{x,y \in ROI} (I_c(x,y) - \mu_c)^2}, \quad c \in \{R, G, B\}$$

### 3.3 Metric 3: Spatial Illumination Uniformity ($U$)
Quantifies whether the dual 45° LED geometry illuminates the circular skin aperture evenly without hot spots:
$$U = \left( 1 - \frac{\sigma_{Y}}{\mu_{Y}} \right) \times 100\%$$
Where $Y$ is the luminance channel ($Y = 0.299R + 0.587G + 0.114B$) evaluated across the inner 80% of the circular aperture.
* **Proposed Target (Unverified):** $U \ge 85\%$ across the 20 mm field of view.

### 3.4 Metric 4: Image Sharpness (Tenengrad Gradient Energy $T$)
Evaluates whether polarizing sheets or PMMA diffusers introduce optical wavefront distortion or blur:
$$T = \frac{1}{N_{ROI}} \sum_{x,y \in ROI} \left( G_x(x,y)^2 + G_y(x,y)^2 \right)$$
Where $G_x, G_y$ are $3\times3$ Sobel gradient convolutions on grayscale luminance.

### 3.5 Metric 5: Static Repeatability ($s_w$) & Repositioning Variability
* **Run 1 (Static):** 10 consecutive captures without moving attachment or target.
* **Run 2 (Repositioning):** 10 captures where attachment is removed, lifted, and repositioned on the target by the operator.
$$s_w = \sqrt{\frac{1}{M - 1} \sum_{m=1}^{M} (RCC_m - \overline{RCC})^2}$$
* **Proposed Target (Unverified):** $s_w \le 0.40$ CIELAB units across 10 repositionings.

---

## 4. Benchtop Execution Procedure

1. **Darkroom Alignment:** Mount the reference phone and attachment onto the optical breadboard. Align camera lens with the aperture centerline.
2. **Arm A Execution (Ordinary Phone):**
   * Position bare phone 10 cm from target.
   * Turn on phone torch/flash. Capture 10 frames of Target 1, Target 2, and Target 3 under Ambient 1 and Ambient 2.
3. **Arm B Execution (OptiChroma Non-Polarized):**
   * Attach OptiChroma housing without polarizing films.
   * Engage dual 5000K LEDs at 50 mA. Capture 10 frames per target.
4. **Arm C Execution (OptiChroma Cross-Polarized):**
   * Insert $0^\circ$ linear polarizer on LEDs and $90^\circ$ analyzer on camera aperture.
   * Engage dual 5000K LEDs at 50 mA. Capture 10 frames per target.
5. **Data Processing:**
   * Feed raw captured images into the verification script. Compute $SPF$, $\mu$, $U$, $T$, and $s_w$.

---

## 5. Standardized Data Collection Template

*(To be filled during physical bench measurement. Do not invent entries.)*

```
+───────────────────────────────────────────────────────────────────────────────────────────────────────────+
|                                    OPTICAL BENCHTOP DATA COLLECTION SHEET                                 |
+───────────────────────────+───────────────────────+───────────────────────+───────────────────────────────+
| Test Parameter            | Arm A (Bare Phone)    | Arm B (Unpolarized)   | Arm C (Cross-Polarized)       |
+───────────────────────────+───────────────────────+───────────────────────+───────────────────────────────+
| Target 1: Matte Target    |                       |                       |                               |
| • Saturated Pixels (SPF %) | [    ] %              | [    ] %              | [    ] %                      |
| • Mean Luminance (Y)      | [    ] DN             | [    ] DN             | [    ] DN                     |
| • Uniformity (U %)        | [    ] %              | [    ] %              | [    ] %                      |
| • Tenengrad Sharpness (T) | [    ]                | [    ]                | [    ]                        |
+───────────────────────────+───────────────────────+───────────────────────+───────────────────────────────+
| Target 2: Dry Skin Model  |                       |                       |                               |
| • Saturated Pixels (SPF %) | [    ] %              | [    ] %              | [    ] %                      |
| • Mean Luminance (Y)      | [    ] DN             | [    ] DN             | [    ] DN                     |
| • Uniformity (U %)        | [    ] %              | [    ] %              | [    ] %                      |
| • Tenengrad Sharpness (T) | [    ]                | [    ]                | [    ]                        |
+───────────────────────────+───────────────────────+───────────────────────+───────────────────────────────+
| Target 3: Oiled Skin Model|                       |                       |                               |
| • Saturated Pixels (SPF %) | [    ] %              | [    ] %              | [    ] %                      |
| • Mean Luminance (Y)      | [    ] DN             | [    ] DN             | [    ] DN                     |
| • Uniformity (U %)        | [    ] %              | [    ] %              | [    ] %                      |
| • Tenengrad Sharpness (T) | [    ]                | [    ]                | [    ]                        |
| • Glare Reduction vs Arm B| N/A                   | 0.0 % (Baseline)      | Target >= 75% [ Actual:     ] |
+───────────────────────────+───────────────────────+───────────────────────+───────────────────────────────+
| Repeatability (10 shots)  |                       |                       |                               |
| • Static Repeatability sw | [    ] CIELAB         | [    ] CIELAB         | Target <= 0.15 [ Actual:    ] |
| • Repositioned sw         | [    ] CIELAB         | [    ] CIELAB         | Target <= 0.40 [ Actual:    ] |
+───────────────────────────+───────────────────────+───────────────────────+───────────────────────────────+
```

# Image Processing Pipeline & Mathematical Specification

**Document Version:** 2.3.0  
**System:** La Roche-Posay OptiChroma (v2.3)  
**Authors:** Computer Vision Architect & Mathematical Imaging Specialist  
**Status:** Evaluated Algorithmic Baseline (Forensic Edition)

---

## 1. Pipeline Overview

The OptiChroma image processing pipeline is designed for determinism, computational efficiency, and scientific defensibility. It runs on standard CPU hardware without requiring heavy deep neural networks:

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                                  IMAGE PROCESSING PIPELINE STAGES                                 |
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                                                                                                   |
|  [Input Frame (RAW Linear RGB or Calibrated BGR)]                                                 |
|         │                                                                                         |
|         ▼                                                                                         |
|  ┌──────────────────────────────────────────────────────────────┐                                 |
|  │ STAGE 1: IMAGE QUALITY GATE                                  │                                 |
|  │ • Tenengrad Gradient Sharpness Variance: Mean(Gx^2 + Gy^2)   │                                 |
|  │ • Specular Saturation Ratio: Count(Pixels >= 254) / Total    │                                 |
|  │ • Shadow Underexposure Ratio: Count(Pixels <= 5) / Total     │                                 |
|  └──────────────────────────────┬───────────────────────────────┘                                 |
|                                 │                                                                 |
|         ┌───────────────────────┴───────────────────────┐                                         |
|         │ FAIL                                          │ PASS                                    |
|         ▼                                               ▼                                         |
|  [Reject Capture & Prompt]               ┌──────────────────────────────────────────────┐         |
|                                          │ STAGE 2: REFERENCE-ASSISTED NORMALIZATION    │         |
|                                          │ • Validate in-frame 18% grey reference patch │         |
|                                          │ • Check patch uniformity (std dev < 18.0)    │         |
|                                          │ • Compute von Kries channel gains:           │         |
|                                          │   k_c = clip(Target_Grey / Mean_c, 0.4, 2.5) │         |
|                                          └──────────────────────┬───────────────────────┘         |
|                                                                 │                                 |
|                                                                 ▼                                 |
|                                          ┌──────────────────────────────────────────────┐         |
|                                          │ STAGE 3: PHYSICAL ROI MASKING                │         |
|                                          │ • Extract 25mm circular skin region centered │         |
|                                          │   at optical aperture origin (R = 0.35 * min)│         |
|                                          └──────────────────────┬───────────────────────┘         |
|                                                                 │                                 |
|                                                                 ▼                                 |
|                                          ┌──────────────────────────────────────────────┐         |
|                                          │ STAGE 4: CHROMATIC FEATURE EXTRACTION        │         |
|                                          │ • Convert to CIELAB space                    │         |
|                                          │ • Compute Exploratory ITA (Skin tone group)  │         |
|                                          │ • Compute Relative Chromatic Contrast:       │         |
|                                          │   RCC = Mean(a*_ROI) - Mean(a*_Reference)   │         |
|                                          └──────────────────────┬───────────────────────┘         |
|                                                                 │                                 |
|                                                                 ▼                                 |
|                                          ┌──────────────────────────────────────────────┐         |
|                                          │ STAGE 5: GLCM TEXTURE DESCRIPTORS            │         |
|                                          │ • Standardize crop to 256x256 patch          │         |
|                                          │ • Quantize to 16 gray levels                 │         |
|                                          │ • Compute Haralick Contrast, Homogeneity,    │         |
|                                          │   and Energy (d=1, 4 angles averaged)        │         |
|                                          └──────────────────────┬───────────────────────┘         |
|                                                                 │                                 |
|                                                                 ▼                                 |
|                                          ┌──────────────────────────────────────────────┐         |
|                                          │ STAGE 6: LONGITUDINAL REGISTRATION & EXPORT  │         |
|                                          │ • Reference target anchor alignment          │         |
|                                          │ • Render side-by-side comparison slider      │         |
|                                          │ • Export structured JSON record to clinic    │         |
|                                          └──────────────────────────────────────────────┘         |
|                                                                                                   |
+───────────────────────────────────────────────────────────────────────────────────────────────────+
```

---

## 2. Stage 1: Quality-Gate Mathematical Formulation

### A. Resolution-Normalized Tenengrad Focus Operator
Traditional Laplacian variance varies with raw image pixel resolution. OptiChroma uses a normalized Tenengrad gradient operator:
1. Convert image to 8-bit grayscale $I_{grey}$.
2. Compute spatial horizontal and vertical gradients using Sobel kernels:
   $$G_x = \text{Sobel}(I_{grey}, \text{dx}=1, \text{dy}=0, k=3)$$
   $$G_y = \text{Sobel}(I_{grey}, \text{dx}=0, \text{dy}=1, k=3)$$
3. Compute the Tenengrad gradient variance:
   $$T = \frac{1}{H \times W} \sum_{x=1}^{W} \sum_{y=1}^{H} \left( G_x(x,y)^2 + G_y(x,y)^2 \right)$$
4. *Initial Engineering Threshold:* $T \ge 85.0$ indicates acceptable sharpness for standardized mobile captures.

### B. Specular Saturation & Shadow Bounds
To detect light leaks, improper standoff contact, or flash glare saturation:
* Saturated pixels: Count of pixels where $\max(R,G,B) \ge 254$.
* Shadow pixels: Count of pixels where $\max(R,G,B) \le 5$.
* Acceptance bounds:
  $$\frac{\text{Count}(\text{Pixel Sat})}{H \times W} \le 0.008 \quad (\le 0.8\% \text{ saturation})$$
  $$\frac{\text{Count}(\text{Pixel Shadow})}{H \times W} \le 0.020 \quad (\le 2.0\% \text{ shadow})$$

---

## 3. Stage 2: Reference-Assisted Normalization

### A. Patch Validation Protocol
The in-frame 18% neutral grey patch is located via fixed aperture coordinates $(x_p, y_p, w_p, h_p)$. Before gains are calculated:
1. Compute mean intensity per channel: $\mu_B, \mu_G, \mu_R$.
2. Compute standard deviation per channel: $\sigma_B, \sigma_G, \sigma_R$.
3. Check uniformity: $\max(\sigma_B, \sigma_G, \sigma_R) \le 18.0$.
4. Check non-clipping: $10.0 < \min(\mu_B, \mu_G, \mu_R) \le \max(\mu_B, \mu_G, \mu_R) < 245.0$.

### B. Linear von Kries Channel Gain Application
If valid, channel scaling gains are applied:
$$k_c = \text{clip}\left(\frac{I_{\text{target\_grey}}}{\mu_c}, 0.4, 2.5\right) \quad \text{for } c \in \{B, G, R\}$$
$$I_{\text{norm}}(x,y,c) = \text{clip}\left(k_c \cdot I(x,y,c), 0, 255\right)$$
Where $I_{\text{target\_grey}} = 118.0$ (nominal sRGB value for 18% reflectance).

*Documented Limitation:* This provides reference-assisted exposure and neutral balance alignment. It does NOT provide camera-specific color correction matrices (CCM) or traceable colorimetric calibration.

---

## 4. Stage 3: Physical ROI Masking

The central circular aperture ($25\,\text{mm}$ inner diameter) is extracted using a fixed circular mask centered at $(W/2, H/2)$ with radius $R = 0.35 \times \min(H, W)$. This physically isolates the uncompressed central skin zone and excludes the peripheral standoff rim and reference patches.

---

## 5. Stage 4: Chromatic Feature Extraction

### A. CIELAB Color Conversion
Normalized BGR images are converted to CIE $L^*a^*b^*$ using the standardized D65 illuminant reference:
* $L^* = L_{\text{OpenCV}} \times \frac{100}{255} \in [0, 100]$
* $a^* = a_{\text{OpenCV}} - 128 \in [-128, 127]$
* $b^* = b_{\text{OpenCV}} - 128 \in [-128, 127]$

### B. Relative Chromatic Contrast (RCC)
The core chromatic metric is defined as:
$$RCC = \overline{a^*}_{\text{ROI}} - \overline{a^*}_{\text{reference}}$$
* *Strict Interpretation:* Quantifies relative redness contrast along the CIELAB red-green axis.
* *Scientific Governance:* RCC is strictly an image-chromatic metric. It is NOT an assay of hemoglobin concentration, blood flow, capillary dilation, or vascular inflammation.

### C. Numerically Stable Individual Typology Angle (ITA)
$$\Delta L^* = \overline{L^*}_{\text{ref}} - 50.0$$
$$\text{If } |\overline{b^*}_{\text{ref}}| < 10^{-4}: ITA^\circ = \begin{cases} +90.0^\circ & \Delta L^* > 0 \\ -90.0^\circ & \Delta L^* < 0 \\ 0.0^\circ & \Delta L^* = 0 \end{cases}$$
$$\text{Else: } ITA^\circ = \left( \arctan\left( \frac{\Delta L^*}{\overline{b^*}_{\text{ref}}} \right) \right) \times \frac{180^\circ}{\pi}$$

Classified into descriptive surface colorimetry categories (Chardon et al., 1991):
* Very Light: $> 55^\circ$
* Light: $41^\circ\text{--}55^\circ$
* Intermediate: $28^\circ\text{--}41^\circ$
* Tan: $10^\circ\text{--}28^\circ$
* Brown: $-30^\circ\text{--}10^\circ$
* Dark: $\le -30^\circ$

*Scientific Governance Safeguard:* ITA color categories describe surface color reflectance only. They do NOT determine Fitzpatrick skin phototype (which reflects genetic UV erythema and tanning reactivity) and do NOT provide a clinical or diagnostic classification.

---

## 6. Stage 5: Standardized GLCM Texture Descriptors

* Standardize central skin crop to $256 \times 256$ pixels.
* Quantize 8-bit grayscale to 16 discrete levels ($[0, 15]$) via integer division ($I // 16$).
* Compute Gray-Level Co-occurrence Matrix (GLCM) at distance $d = 1$ across 4 canonical directions: $\theta \in \{0^\circ, 45^\circ, 90^\circ, 135^\circ\}$.
* Average Haralick descriptors across all 4 directions:
  * **Contrast:** $\sum_{i,j} |i - j|^2 P(i,j)$ (local intensity variations).
  * **Homogeneity:** $\sum_{i,j} \frac{P(i,j)}{1 + |i - j|}$ (structural smoothness).
  * **Energy:** $\sum_{i,j} P(i,j)^2$ (textural order).
* *Documented Limitation:* GLCM descriptors describe 2D image pixel intensity co-occurrence only. They do NOT measure stratum corneum barrier thickness, lipid depletion, or Transepidermal Water Loss (TEWL).

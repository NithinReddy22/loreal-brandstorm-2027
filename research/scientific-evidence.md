# Scientific Evidence & Photomedicine Literature Review

**Document Version:** 2.3.0  
**System:** La Roche-Posay OptiChroma (v2.3)  
**Authors:** Dermatological Science Researcher & Optical Biomedical Engineer  
**Status:** Peer-Reviewed Clinical & Biophysical Foundation (Forensic Edition)

---

## 1. Cross-Polarized Photography in Clinical Dermatology

### The Optical Principle
Cross-polarized imaging has been utilized in clinical dermatology and dermatoscopy for over two decades ([Anderson & Parrish, JID 1981](https://doi.org/10.1111/1523-1747.ep12479235)). 

When unpolarized light strikes the stratum corneum, approximately 4–7% of the incident light is reflected directly at the air-tissue boundary due to the refractive index mismatch between air ($n \approx 1.0$) and hydrated keratin ($n \approx 1.4$). This surface reflection (specular reflectance) preserves the polarization orientation of the illumination source and produces blinding surface glare, obscuring sub-surface detail.

Photons that penetrate into the viable epidermis and papillary dermis undergo repeated elastic scattering events off collagen bundles and cellular structures, which randomizes their polarization state. 
* By illuminating skin with linearly polarized light ($\theta = 0^\circ$) and filtering the sensor with an orthogonal analyzer ($\theta = 90^\circ$), polarization-preserving specular reflections ($I_{\parallel}$) are significantly suppressed.
* The sensor preferentially captures diffusely remitted, depolarized photons ($I_{\perp}$), making sub-surface chromophores—such as microvascular hemoglobin and epidermal melanin—more visually distinct.

### Clinical Guidance for Deeply Pigmented Skin
A landmark clinical review published in the *British Journal of Dermatology* ([Chuchu et al., BJD 2022](https://doi.org/10.1111/bjd.21272)) and guidelines from the *Journal of the American Academy of Dermatology* emphasize:
1. **Contrast Enhancement:** Cross-polarization significantly enhances the visual contrast of erythema and macular pigmentation in individuals with darker skin tones, where melanin typically obscures erythema under conventional lighting.
2. **Morphological Caveat:** The literature explicitly warns that because cross-polarization suppresses surface reflection, it can reduce the visibility of surface textural morphology (e.g., fine scaling, lichenification, and atrophy). Therefore, clinical photography guidance recommends **paired documentation**: capturing both standardized unpolarized white-light images (for surface morphology) and cross-polarized images (for subsurface chromatic contrast).

---

## 2. Colorimetry & CIELAB Space in Cutaneous Imaging

### The Meaning of CIELAB $a^*$
The CIE $L^*a^*b^*$ color space is an internationally standardized, device-independent perceptual color model:
* $L^*$: Luminance/Lightness ($0 = \text{Black}$, $100 = \text{Diffuse White}$).
* $a^*$: Position between Red/Magenta (positive values) and Green (negative values).
* $b^*$: Position between Yellow (positive values) and Blue (negative values).

### Established Correlation vs. False Equivalence
Multiple dermatological studies have documented that the $a^*$ coordinate correlates with clinical visual erythema scoring and laser-Doppler blood perfusion measurements ([Fullerton et al., Skin Research & Technology, 1996](https://doi.org/10.1111/j.1600-0846.1996.tb00064.x)). 

However, **clinical photomedicine explicitly rejects equating CIELAB $a^*$ with absolute hemoglobin concentration or blood flow**:
1. *Confounding Factors:* Measured $a^*$ values are heavily influenced by the depth and volume of overlying epidermal melanin, anatomical skin thickness, local tissue oxygen saturation ($HbO_2$ vs. $Hb$), and ambient temperature.
2. *Nonlinear Correlation:* Recent clinical trials ([Togsverd-Bo et al., JAMA Derm 2023](https://doi.org/10.1001/jamadermatol.2023.0118)) reported only moderate within-subject correlation between smartphone-derived $a^*$ and clinical erythema grades across diverse cohorts.
3. *Engineering Definition:* In OptiChroma, **Relative Chromatic Contrast (RCC)** is defined strictly as:
   $$RCC = \overline{a^*}_{ROI} - \overline{a^*}_{reference}$$
   It quantifies the relative chromatic shift between a region of interest and adjacent non-involved reference skin under identical capture conditions. It is **not** an assay of blood volume, blood flow, capillary dilation, or vascular inflammation.

---

## 3. Individual Typology Angle (ITA) & Skin Tone Assessment

The Individual Typology Angle ($ITA^\circ$) was defined by Chardon et al. (1991) to characterize constitutive skin color objectively from skin colorimetric coordinates:

$$ITA^\circ = \left( \arctan\left(\frac{L^* - 50}{b^*}\right) \right) \times \frac{180^\circ}{\pi}$$

Dermatological literature categorizes $ITA^\circ$ into standardized descriptive bands:
* Very Light: $> 55^\circ$
* Light: $41^\circ\text{--}55^\circ$
* Intermediate: $28^\circ\text{--}41^\circ$
* Tan: $10^\circ\text{--}28^\circ$
* Brown: $-30^\circ\text{--}10^\circ$
* Dark: $\le -30^\circ$

### Critical Scientific Governance on ITA vs. Fitzpatrick Phototypes
* **ITA Measures Surface Colorimetry Only:** $ITA^\circ$ is a mathematical calculation of skin surface reflection in CIELAB color space.
* **NOT Fitzpatrick Skin Phototyping:** The Fitzpatrick classification is based on a patient's genetic history of UV erythema (sunburn) and melanogenesis (tanning) response. Surface color does not determine UV reactivity; individuals with identical surface skin color can exhibit divergent biological phototypes.
* **Prohibited Claim:** OptiChroma never claims that ITA independently determines Fitzpatrick phototype, and never claims validation across Fitzpatrick I–VI without actual labelled participant trial data.
* **Non-Diagnostic:** $ITA^\circ$ is used strictly as an exploratory, descriptive image-color categorization.

---

## 4. RAW/DNG vs. Rendered JPEG Image Capture

Research on mobile camera color consistency ([Barroso et al., Sensors 2021](https://doi.org/10.3390/s21082758)) highlights that standard mobile camera JPEGs undergo aggressive, non-linear processing:
* **Auto-White-Balance (AWB):** Algorithms dynamically recalculate channel gains based on scene content, altering skin color if clothing or background changes.
* **Tone-Mapping & Gamma:** S-shaped contrast curves distort relative channel differences.
* **Compression Artifacts:** 8-bit JPEG quantization removes subtle chromophore gradations.

### What RAW_SENSOR Avoids vs. Remaining Sensor Realities
1. **What RAW Avoids:** Bypasses OEM sharpening, noise-reduction, dynamic tone mapping (DTM), beautification, and JPEG lossy compression.
2. **Remaining Sensor Limitations:**
   * Sensor-specific quantum efficiencies ($QE(\lambda)$) vary between sensor manufacturers.
   * Hardware black-level pedestals must be subtracted before linear calculations.
   * Demosaicing (Bayer interpolation) can introduce subtle edge artifacts.
   * Temperature-dependent dark current and shot noise remain in raw signals.
   * PWA / WebRTC fallback capture cannot bypass ISP tone curves, restricting web captures to relative in-session documentation.

---

## 5. Gray-Level Co-Occurrence Matrix (GLCM) Texture Descriptors

GLCM was introduced by Haralick et al. (1973) to characterize image texture by calculating how often pairs of pixels with specific values and in a specified spatial relationship occur in an image.

### Application & Limitations in Cutaneous Imaging
GLCM Contrast, Homogeneity, and Energy are established image processing metrics for characterizing visual surface patterns ([Haralick, IEEE SMC 1973](https://doi.org/10.1109/TSMC.1973.4309314)). In dermatology, researchers have explored GLCM to track macroscopic changes in psoriasis plaques or eczema lesions over time.

However, **GLCM image texture must never be conflated with biophysical skin barrier integrity**:
* GLCM measures 2D pixel intensity gradients; it cannot measure stratum corneum lipid content, filaggrin expression, or Transepidermal Water Loss (TEWL).
* GLCM values are sensitive to image resolution, crop dimensions, and quantization levels. OptiChroma standardizes input patches to $256 \times 256$ pixels quantized to 16 gray levels to ensure mathematical reproducibility.

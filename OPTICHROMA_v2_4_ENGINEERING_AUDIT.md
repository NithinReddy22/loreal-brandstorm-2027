# OptiChroma v2.4 — Forensic Source Code & Engineering Audit

**Document ID:** `OPTICHROMA_v2_4_ENGINEERING_AUDIT.md`  
**System:** La Roche-Posay OptiChroma (v2.4 MVP Freeze)  
**Auditor:** Independent Technical Verification Taskforce  
**Status:** Implementation-Verified Forensic Audit  
**Classification:** Student Proof-of-Concept Software & Optical Stack

---

## 1. Public Function-by-Function Source Code Verification

This section reviews every public method implemented in `src/optichroma_v2_3_core.py` (and aliased in `src/optichroma_v2_2_core.py`).

### 1.1 `__init__`
* **Inputs & Expected Types:**
  * `target_grey_val`: `float` (default `118.0`)
  * `sharpness_threshold`: `float` (default `85.0`)
  * `max_saturation_ratio`: `float` (default `0.008`)
  * `max_shadow_ratio`: `float` (default `0.02`)
  * `min_gain`: `float` (default `0.4`)
  * `max_gain`: `float` (default `2.5`)
* **Outputs & Types:** `None`
* **Input Validation:** Casts each parameter to `float()`. Does not enforce positive bounds in constructor (e.g. negative thresholds are cast but not blocked at initialization).
* **Mathematical Operations:** Field assignment.
* **Error Handling:** Standard Python `TypeError` / `ValueError` if non-numeric types are passed.
* **Known Limitations:** Parameters are heuristic engineering defaults. They are not universal across all camera hardware and require empirical tuning per sensor model.

### 1.2 `validate_image_input`
* **Inputs & Expected Types:**
  * `img_bgr`: `Any` (expects `np.ndarray`)
* **Outputs & Types:**
  * `Tuple[bool, str]`: `(is_valid, message)`
* **Input Validation:**
  * Checks `img_bgr is None`
  * Checks `isinstance(img_bgr, np.ndarray)`
  * Checks `img_bgr.size == 0`
  * Checks `img_bgr.dtype == np.uint8`
  * Checks `len(img_bgr.shape) == 3`
  * Checks `img_bgr.shape[2] == 3`
  * Checks minimum dimensions: $H \ge 200$, $W \ge 200$
* **Mathematical Operations:** Size and shape inspections.
* **Error Handling:** Returns `(False, "descriptive error string")` without crashing.
* **Known Limitations:** Restricted exclusively to 3-channel 8-bit BGR images. Rejects linear 16-bit images, 1-channel raw Bayer arrays, and images below 200x200 pixels.

### 1.3 `quality_gate`
* **Inputs & Expected Types:**
  * `img_bgr`: `np.ndarray` (uint8 BGR)
* **Outputs & Types:**
  * `Tuple[bool, Dict[str, Any]]`: `(passed, telemetry_dict)`
* **Input Validation:** Calls `validate_image_input`. Returns `False, {"passed": False, "error": msg}` if invalid.
* **Mathematical Operations:**
  1. Grayscale conversion: $I_{grey} = 0.114 B + 0.587 G + 0.299 R$ (OpenCV `COLOR_BGR2GRAY`).
  2. Spatial gradients: $G_x = \text{Sobel}(I, k=3)$, $G_y = \text{Sobel}(I, k=3)$ with `CV_64F`.
  3. Tenengrad focus score: $T = \frac{1}{H \times W} \sum_{x,y} (G_x^2 + G_y^2)$.
  4. Saturation check: $N_{sat} = \sum \text{any}(I_{c} \ge 254)$, $\text{ratio}_{sat} = N_{sat} / (H \times W)$.
  5. Underexposure check: $N_{shadow} = \sum \text{all}(I_{c} \le 5)$, $\text{ratio}_{shadow} = N_{shadow} / (H \times W)$.
* **Error Handling:** Catches malformed inputs via validation; returns structured dictionary with individual pass/fail flags.
* **Known Limitations:** Tenengrad variance is sensitive to high-frequency sensor noise. Saturated pixel ratio counts surface specular highlights across the entire image rather than isolating the central skin aperture.

### 1.4 `detect_and_validate_reference_patch`
* **Inputs & Expected Types:**
  * `img_bgr`: `np.ndarray` (uint8 BGR)
  * `patch_coords`: `Tuple[int, int, int, int]` representing `(x, y, w, h)`
  * `max_std_dev`: `float` (default `18.0`)
* **Outputs & Types:**
  * `Tuple[bool, Dict[str, Any]]`: `(valid, telemetry_dict)`
* **Input Validation:**
  * Validates image format.
  * Validates `len(patch_coords) == 4`.
  * Validates bounds: $x \ge 0, y \ge 0, w \ge 10, h \ge 10, x+w \le W, y+h \le H$.
* **Mathematical Operations:**
  * Extracts sub-array `patch = img[y:y+h, x:x+w]`.
  * Computes channel means: $\mu_B, \mu_G, \mu_R$.
  * Computes channel standard deviations: $\sigma_B, \sigma_G, \sigma_R$.
  * Evaluates clipping: $\min(\mu) < 10.0$ or $\max(\mu) > 245.0$.
  * Evaluates uniformity: $\max(\sigma) \le \text{max\_std\_dev}$.
* **Error Handling:** Returns `(False, {"valid": False, "error": msg})` for out-of-bounds or malformed inputs.
* **Known Limitations:** Requires a-priori knowledge of patch coordinates $(x, y, w, h)$. Does not perform automatic fiducial detection.

### 1.5 `reference_assisted_normalize`
* **Inputs & Expected Types:**
  * `img_bgr`: `np.ndarray` (uint8 BGR)
  * `patch_coords`: `Tuple[int, int, int, int]`
* **Outputs & Types:**
  * `Tuple[np.ndarray, Dict[str, Any]]`: `(normalized_bgr, report_dict)`
* **Input Validation:** Relies on `detect_and_validate_reference_patch`.
* **Mathematical Operations:**
  * Computes linear scalar channel gains:
    $$g_c = \text{clip}\left(\frac{I_{\text{target}}}{\max(\mu_c, 1.0)}, g_{min}, g_{max}\right), \quad c \in \{B, G, R\}$$
  * Multiplies array: $I_{norm}(x,y,c) = \text{clip}(g_c \cdot I(x,y,c), 0, 255)$.
* **Error Handling:** If the patch is clipped, non-uniform, or out-of-bounds, returns `img_bgr.copy()` unchanged with `gains = (1.0, 1.0, 1.0)`.
* **Known Limitations:** **CRITICAL LIMITATION:** Multiplies gamma-encoded 8-bit values directly by scalar gains. In non-linear sRGB, this scales scene radiance by $g_c^{\gamma} \approx g_c^{2.2}$, distorting relative chromaticity across luminance levels.

### 1.6 `extract_physical_skin_roi`
* **Inputs & Expected Types:**
  * `img_bgr`: `np.ndarray` (uint8 BGR)
  * `radius_ratio`: `float` (default `0.35`)
* **Outputs & Types:**
  * `Tuple[Optional[np.ndarray], Tuple[int, int, int]]`: `(binary_mask, (center_x, center_y, radius))`
* **Input Validation:** Validates image format. Returns `None, (0, 0, 0)` on invalid input.
* **Mathematical Operations:**
  * $c_x = W // 2, c_y = H // 2, r = \text{int}(\min(H, W) \times \text{radius\_ratio})$.
  * Draws filled circle on zero array using `cv2.circle(mask, ..., 255, -1)`.
* **Error Handling:** Returns `None, (0, 0, 0)` if input validation fails.
* **Known Limitations:** Assumes the camera lens is perfectly centered over the physical aperture. If the universal clip is misaligned, the circular mask will capture part of the interior plastic baffle.

### 1.7 `calculate_relative_chromatic_contrast`
* **Inputs & Expected Types:**
  * `img_bgr`: `np.ndarray` (uint8 BGR)
  * `roi_box`: `Tuple[int, int, int, int]`
  * `ref_box`: `Tuple[int, int, int, int]`
* **Outputs & Types:**
  * `Dict[str, Any]`
* **Input Validation:**
  * Validates image format.
  * Checks `len(roi_box) == 4` and `len(ref_box) == 4`.
  * Verifies both boxes are within image bounds and have dimensions $> 0$.
* **Mathematical Operations:**
  * Converts BGR to CIE $L^*a^*b^*$ using `cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)`.
  * Unpacks channels: $L^* = L \times \frac{100}{255}$, $a^* = a - 128$, $b^* = b - 128$.
  * Computes $\overline{a^*}_{ROI}$ and $\overline{a^*}_{ref}$.
  * $RCC = \overline{a^*}_{ROI} - \overline{a^*}_{ref}$.
  * Computes $\text{ITA}^\circ = \arctan\left(\frac{\overline{L^*}_{ref} - 50}{\overline{b^*}_{ref}}\right) \times \frac{180}{\pi}$.
* **Error Handling:** Returns `{"error": "message"}` on invalid inputs or out-of-bounds coordinates.
* **Known Limitations:** RCC is an image-color delta along the $a^*$ axis, NOT a physiological measure of hemoglobin, blood flow, or inflammation. Does not check if ROI and reference overlap.

### 1.8 `calculate_glcm_texture`
* **Inputs & Expected Types:**
  * `img_bgr`: `np.ndarray` (uint8 BGR)
  * `crop_box`: `Tuple[int, int, int, int]`
  * `standard_res`: `int` (default `256`)
* **Outputs & Types:**
  * `Dict[str, Any]`
* **Input Validation:**
  * Validates image format.
  * Checks bounds and minimum crop dimension: $w \ge 16, h \ge 16$.
* **Mathematical Operations:**
  * Extracts sub-image: `img[y:y+h, x:x+w]`.
  * Resizes to `(standard_res, standard_res)` using `cv2.INTER_AREA`.
  * Converts to grayscale and quantizes: `gray_16 = gray // 16`.
  * Computes GLCM at distance $1$, angles $\{0, \pi/4, \pi/2, 3\pi/4\}$.
  * Averages Contrast, Homogeneity, and Energy.
* **Error Handling:** Returns `{"error": "message"}` for out-of-bounds or small crops.
* **Known Limitations:** Resizing small crops to $256 \times 256$ inflates pixel blocks, distorting spatial frequency. 16-level quantization collapses subtle skin variations.

---

## 2. Forensic Specific Checks (Questions 1 to 9)

### Check 1: Does the core accept BGR uint8 images only, or also RAW/DNG data?
* **Audit Finding:** The core accepts **BGR uint8 images ONLY**.
* **Evidence in Code:** Line 59 of `src/optichroma_v2_3_core.py` explicitly rejects any image where `img_bgr.dtype != np.uint8`, and line 61 rejects any array where `shape[2] != 3`. RAW Bayer data (typically 1-channel 10-bit or 12-bit `np.uint16`) is rejected immediately at input validation.
* **Status:** RAW/DNG processing is documented in architecture specifications but is **NOT implemented** in the executable core module.

### Check 2: Does the actual camera-acquisition implementation exist or is it merely documented?
* **Audit Finding:** The camera-acquisition implementation is **MERELY DOCUMENTED**.
* **Evidence in Workspace:** A search across the workspace for `.java`, `.kt`, `.js`, `.ts`, and `.tsx` files returned zero code files. The Camera2 API calls and WebRTC snippets in `architecture/camera-acquisition.md` are descriptive design specifications. No runnable Android service or web capture client currently exists in the codebase.

### Check 3: Does the CIELAB conversion assume sRGB input?
* **Audit Finding:** **YES, it strictly assumes standard sRGB.**
* **Evidence in Code:** Line 249 of `src/optichroma_v2_3_core.py` executes `cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)`. OpenCV's internal implementation implements the standard CIE $D_{65}$ sRGB-to-XYZ-to-Lab transform, which expects non-linear gamma-corrected sRGB pixels. Passing linear sensor data into this function produces incorrect, distorted CIELAB coordinates.

### Check 4: Does reference-patch normalization operate on linear or gamma-encoded values?
* **Audit Finding:** It operates on **GAMMA-ENCODED values** (A mathematical defect in physical colorimetry).
* **Evidence in Code:** In `reference_assisted_normalize` (lines 184–191), scalar gains $g_c = 118.0 / \mu_c$ are multiplied directly against the 8-bit non-linear BGR array: `norm_bgr = img_bgr * gain`.
* **Physical Consequence:** True von Kries chromatic adaptation must be performed in linear scene-radiance space. Scaling gamma-compressed values by $g_c$ scales the underlying linear radiance by $g_c^\gamma \approx g_c^{2.2}$, causing non-linear chromatic shifts across shadow, midtone, and highlight regions.

### Check 5: Does RCC use consistent ROI and reference regions?
* **Audit Finding:** **NO, region geometry is unconstrained.**
* **Evidence in Code:** `calculate_relative_chromatic_contrast` accepts arbitrary bounding boxes `roi_box` and `ref_box`. The code verifies that both boxes are inside the image, but does not verify:
  * That ROI and reference do not overlap.
  * That ROI and reference lie inside the central uncompressed aperture.
  * That the reference region represents healthy perilesional skin rather than the plastic housing or in-frame calibration strip.

### Check 6: Does GLCM resizing and quantization preserve meaningful spatial information?
* **Audit Finding:** **NO, spatial frequency is distorted by forced resizing.**
* **Evidence in Code:** `calculate_glcm_texture` forces any arbitrary crop box $(w, h)$ to $256 \times 256$ pixels.
* **Distortion Analysis:** If a user selects a $32 \times 32$ pixel lesion crop, upsampling to $256 \times 256$ creates artificial $8 \times 8$ pixel uniform blocks. Computing GLCM at pixel distance $d = 1$ measures the smoothness of the bicubic interpolation, artificially driving Homogeneity toward $1.0$ and Contrast toward $0.0$. Furthermore, uniform 16-level quantization (`gray // 16`) collapses low-contrast erythema (standard deviation $< 4$ DN) into a single gray bin.

### Check 7: Are Tenengrad thresholds resolution-dependent?
* **Audit Finding:** **YES, Tenengrad scores vary with image resolution and sensor noise.**
* **Evidence in Code:** Although `np.mean(gx**2 + gy**2)` averages over total pixels, optical point spread functions (PSF) and sensor read noise scale differently with megapixel count. A fixed threshold ($T = 85.0$) will produce divergent acceptance rates between a 2 MP web stream and a 48 MP smartphone capture of identical optical focus. Universal thresholds cannot be asserted without per-sensor calibration.

### Check 8: Do numerical operations handle NaN, infinity, empty arrays and zero-variance images?
* **Audit Finding:**
  * **Empty Arrays:** Handled safely by `validate_image_input` (`img_bgr.size == 0`).
  * **Zero-Variance / Constant Images:** Handled safely. Pure black/white/gray images yield Tenengrad score $0.0$, correctly failing the focus gate.
  * **NaN / Infinity:** Standard input uint8 arrays cannot contain IEEE 754 NaN or Inf. If a float array is passed, `validate_image_input` catches and rejects it (`dtype != np.uint8`).

### Check 9: Does ITA handle all combinations of positive, negative and near-zero $b^*$ correctly?
* **Conventional Dermatological Formula (Chardon et al., 1991):**
  $$\text{ITA}^\circ = \left( \arctan\left(\frac{L^* - 50}{b^*}\right) \right) \times \frac{180}{\pi}$$
* **Mathematical Quadrant Analysis:**
  * Standard $\arctan(x)$ outputs values in $\left(-90^\circ, +90^\circ\right)$.
  * When $b^* > 0$ (normal living human skin):
    * If $L^* > 50$, ratio $> 0 \implies \text{ITA} \in (0^\circ, +90^\circ)$.
    * If $L^* < 50$, ratio $< 0 \implies \text{ITA} \in (-90^\circ, 0^\circ)$.
    * If $L^* = 50$, ratio $= 0 \implies \text{ITA} = 0.0^\circ$.
  * When $b^* \to 0$:
    * In our implementation (`optichroma_v2_3_core.py`, lines 260–268), when $|b^*| < 10^{-4}$:
      * If $\Delta L^* > 0 \implies \text{ITA} = +90.0^\circ$.
      * If $\Delta L^* < 0 \implies \text{ITA} = -90.0^\circ$.
      * If $\Delta L^* = 0 \implies \text{ITA} = 0.0^\circ$.
  * When $b^* < 0$ (artificial blue casts or cool color targets):
    * Chardon's formula was derived strictly under the physiological condition $b^* > 0$.
    * If $b^* < 0$, $\Delta L^* > 0$ produces a negative ratio ($\text{ITA} < 0$), while $\Delta L^* < 0$ produces a positive ratio ($\text{ITA} > 0$).
    * Using `arctan2(L^* - 50, b^*)` would map cool tones into Quadrant II ($90^\circ\text{ to }180^\circ$), which falls completely outside the dermatological classification scale.
    * **Conclusion:** Retaining standard $\arctan(\Delta L^* / b^*)$ with the $b^* \to 0$ singularity guard is mathematically faithful to Chardon's definition.

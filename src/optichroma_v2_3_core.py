"""
OptiChroma Core Processing Module (v2.3 - Forensic Baseline & Proof-of-Concept)
================================================================================
System: Standardized Cross-Polarized Smartphone Imaging & Visual Documentation Platform
Brand Scope: La Roche-Posay (L'Oréal Dermatological Beauty)

STATUS:
Exploratory Student Proof-of-Concept. NOT a certified medical software device,
NOT a validated clinical diagnostic tool, and NOT production-grade software.

NON-NEGOTIABLE CLAIMS & SCIENTIFIC BOUNDARIES:
- NOT an autonomous diagnostic tool or medical spectrophotometer.
- Does NOT measure absolute hemoglobin, melanin, blood flow, inflammation, or TEWL.
- Relative Chromatic Contrast (RCC) is strictly a relative image-color difference (Delta a*)
  under specified acquisition conditions, NOT a physiological vascular assay.
- Individual Typology Angle (ITA) provides exploratory image-derived chromatic categories
  (Chardon et al., 1991), NOT Fitzpatrick skin phototypes or clinical classifications.
- In-frame patch normalization provides heuristic, reference-assisted exposure/balance
  normalization; it does NOT provide camera-specific color correction or traceable
  colorimetric calibration.
"""

from typing import Dict, Any, Tuple, Optional
import numpy as np
import cv2
from skimage.feature import graycomatrix, graycoprops


class OptiChromaCoreV2_3:
    """
    Student proof-of-concept processing and quality verification engine
    for the La Roche-Posay OptiChroma optical attachment.
    """

    def __init__(
        self,
        target_grey_val: float = 118.0,
        sharpness_threshold: float = 85.0,
        max_saturation_ratio: float = 0.008,
        max_shadow_ratio: float = 0.02,
        min_gain: float = 0.4,
        max_gain: float = 2.5
    ) -> None:
        """
        Initializes the proof-of-concept engine with initial engineering defaults.
        
        NOTE: These parameters are initial heuristic defaults requiring empirical
        benchtop calibration per smartphone sensor model.

        :param target_grey_val: Nominal 8-bit sRGB value for 18% neutral grey (~118.0 under sRGB transfer curve).
        :param sharpness_threshold: Proposed Tenengrad gradient threshold for focus acceptance.
        :param max_saturation_ratio: Maximum allowable fraction of saturated pixels (<0.8%).
        :param max_shadow_ratio: Maximum allowable fraction of clipped shadow pixels (<2.0%).
        :param min_gain: Minimum allowable linear channel gain during color normalization.
        :param max_gain: Maximum allowable linear channel gain during color normalization.
        """
        self.target_grey_val = float(target_grey_val)
        self.sharpness_threshold = float(sharpness_threshold)
        self.max_saturation_ratio = float(max_saturation_ratio)
        self.max_shadow_ratio = float(max_shadow_ratio)
        self.min_gain = float(min_gain)
        self.max_gain = float(max_gain)

    def validate_image_input(self, img_bgr: Any) -> Tuple[bool, str]:
        """
        Validates input data format, dimensions, channels, data type, and memory integrity.
        """
        if img_bgr is None:
            return False, "Input image is None."
        if not isinstance(img_bgr, np.ndarray):
            return False, f"Input must be a numpy.ndarray, got {type(img_bgr).__name__}."
        if img_bgr.size == 0:
            return False, "Input array is empty (size 0)."
        if img_bgr.dtype != np.uint8:
            return False, f"Input array must have dtype uint8, got {img_bgr.dtype}."
        if len(img_bgr.shape) != 3:
            return False, f"Input array must be 3-dimensional (H, W, C), got shape {img_bgr.shape}."
        if img_bgr.shape[2] != 3:
            return False, f"Input array must have exactly 3 color channels (BGR), got {img_bgr.shape[2]}."
        
        h, w, _ = img_bgr.shape
        if h < 200 or w < 200:
            return False, f"Image dimensions too small ({w}x{h}). Minimum required: 200x200."
        
        return True, "Valid"

    def quality_gate(self, img_bgr: np.ndarray) -> Tuple[bool, Dict[str, Any]]:
        """
        Image Quality Gate (Proof-of-Concept):
        Assesses focus sharpness via Tenengrad gradient and exposure bounds.
        Rejects captures that are blurred, specular-saturated, or severely underexposed.
        """
        is_valid, msg = self.validate_image_input(img_bgr)
        if not is_valid:
            return False, {"passed": False, "error": msg}

        h, w, _ = img_bgr.shape
        total_pixels = float(h * w)

        # 1. Tenengrad Gradient Energy Sharpness Metric
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        gradient_sq = gx**2 + gy**2
        tenengrad_score = float(np.mean(gradient_sq))
        is_sharp = tenengrad_score >= self.sharpness_threshold

        # 2. Specular Saturation & Shadow Clipping Assessment
        # Saturated: any color channel clipping at >= 254 (loss of highlight detail)
        saturated_pixels = np.any(img_bgr >= 254, axis=2)
        # Underexposed: all channels <= 5 (deep shadow / blocked aperture)
        shadow_pixels = np.all(img_bgr <= 5, axis=2)

        saturated_count = int(np.sum(saturated_pixels))
        shadow_count = int(np.sum(shadow_pixels))

        saturation_ratio = float(saturated_count / total_pixels)
        shadow_ratio = float(shadow_count / total_pixels)

        is_exposure_acceptable = (
            saturation_ratio <= self.max_saturation_ratio and
            shadow_ratio <= self.max_shadow_ratio
        )

        passed = is_sharp and is_exposure_acceptable
        return passed, {
            "passed": passed,
            "tenengrad_sharpness": round(tenengrad_score, 2),
            "sharpness_threshold": self.sharpness_threshold,
            "sharpness_pass": is_sharp,
            "saturation_ratio": round(saturation_ratio, 5),
            "saturation_threshold": self.max_saturation_ratio,
            "shadow_ratio": round(shadow_ratio, 5),
            "shadow_threshold": self.max_shadow_ratio,
            "exposure_pass": is_exposure_acceptable
        }

    def detect_and_validate_reference_patch(
        self,
        img_bgr: np.ndarray,
        patch_coords: Tuple[int, int, int, int],
        max_std_dev: float = 18.0
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Extracts and statistically validates an in-frame neutral reference patch.
        Ensures the patch is within bounds, uniform, and not clipped.

        :param img_bgr: Input BGR image.
        :param patch_coords: (x, y, w, h) bounding box of the reference patch.
        :param max_std_dev: Maximum standard deviation across pixels to verify patch uniformity.
        """
        is_valid, msg = self.validate_image_input(img_bgr)
        if not is_valid:
            return False, {"valid": False, "error": msg}

        if len(patch_coords) != 4:
            return False, {"valid": False, "error": f"Patch coords must be (x, y, w, h), got {patch_coords}."}

        x, y, w, h = patch_coords
        img_h, img_w, _ = img_bgr.shape

        if w < 10 or h < 10:
            return False, {"valid": False, "error": f"Patch dimensions too small ({w}x{h}). Minimum: 10x10."}
        if x < 0 or y < 0 or (x + w) > img_w or (y + h) > img_h:
            return False, {"valid": False, "error": f"Patch coordinates out of bounds: {patch_coords} for image {img_w}x{img_h}."}

        patch = img_bgr[y:y+h, x:x+w].astype(np.float32)
        mean_b = float(np.mean(patch[:, :, 0]))
        mean_g = float(np.mean(patch[:, :, 1]))
        mean_r = float(np.mean(patch[:, :, 2]))

        std_b = float(np.std(patch[:, :, 0]))
        std_g = float(np.std(patch[:, :, 1]))
        std_r = float(np.std(patch[:, :, 2]))
        max_std = max(std_b, std_g, std_r)

        # Check clipping against extreme saturation/underexposure
        is_clipped = (min(mean_b, mean_g, mean_r) < 10.0) or (max(mean_b, mean_g, mean_r) > 245.0)
        is_uniform = max_std <= max_std_dev

        valid = (not is_clipped) and is_uniform
        return valid, {
            "valid": valid,
            "mean_bgr": (round(mean_b, 2), round(mean_g, 2), round(mean_r, 2)),
            "std_bgr": (round(std_b, 2), round(std_g, 2), round(std_r, 2)),
            "is_clipped": is_clipped,
            "is_uniform": is_uniform,
            "patch_coords": patch_coords
        }

    def reference_assisted_normalize(
        self,
        img_bgr: np.ndarray,
        patch_coords: Tuple[int, int, int, int]
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Applies linear von Kries gain adjustment based on the measured in-frame neutral grey patch.
        
        DOCUMENTED LIMITATION:
        This operation aligns exposure and neutral white balance to a nominal target level.
        It does NOT:
        - Provide traceable colorimetric calibration or camera-specific color correction matrices.
        - Linearize non-linear camera tone curves (sRGB gamma or OEM tone mapping).
        - Correct sensor spectral quantum efficiency differences.
        """
        is_valid_patch, patch_data = self.detect_and_validate_reference_patch(img_bgr, patch_coords)
        if not is_valid_patch:
            # Fallback: return unchanged copy to prevent corrupted gains
            return img_bgr.copy(), {
                "normalized": False,
                "reason": patch_data.get("error", "Invalid, clipped, or non-uniform reference patch."),
                "applied_gains": (1.0, 1.0, 1.0)
            }

        mean_b, mean_g, mean_r = patch_data["mean_bgr"]
        
        gain_b = float(np.clip(self.target_grey_val / max(mean_b, 1.0), self.min_gain, self.max_gain))
        gain_g = float(np.clip(self.target_grey_val / max(mean_g, 1.0), self.min_gain, self.max_gain))
        gain_r = float(np.clip(self.target_grey_val / max(mean_r, 1.0), self.min_gain, self.max_gain))

        norm_bgr = img_bgr.astype(np.float32)
        norm_bgr[:, :, 0] = np.clip(norm_bgr[:, :, 0] * gain_b, 0, 255)
        norm_bgr[:, :, 1] = np.clip(norm_bgr[:, :, 1] * gain_g, 0, 255)
        norm_bgr[:, :, 2] = np.clip(norm_bgr[:, :, 2] * gain_r, 0, 255)

        return norm_bgr.astype(np.uint8), {
            "normalized": True,
            "applied_gains": (round(gain_b, 3), round(gain_g, 3), round(gain_r, 3)),
            "target_grey_val": self.target_grey_val,
            "method": "Linear reference-assisted normalization (von Kries scaling)"
        }

    def extract_physical_skin_roi(
        self,
        img_bgr: np.ndarray,
        radius_ratio: float = 0.35
    ) -> Tuple[Optional[np.ndarray], Tuple[int, int, int]]:
        """
        Extracts the physically defined circular skin ROI matching the 25mm contact aperture.
        Because working distance and attachment clamp are mechanically fixed, the target skin
        is centered in the frame.

        :param radius_ratio: Ratio of image minimum dimension for the circular aperture radius.
        :return: (binary_mask, (center_x, center_y, radius))
        """
        is_valid, msg = self.validate_image_input(img_bgr)
        if not is_valid:
            return None, (0, 0, 0)

        h, w, _ = img_bgr.shape
        center_x = w // 2
        center_y = h // 2
        radius = int(min(h, w) * radius_ratio)

        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(mask, (center_x, center_y), radius, 255, -1)
        return mask, (center_x, center_y, radius)

    def calculate_relative_chromatic_contrast(
        self,
        img_bgr: np.ndarray,
        roi_box: Tuple[int, int, int, int],
        ref_box: Tuple[int, int, int, int]
    ) -> Dict[str, Any]:
        """
        Calculates Relative Chromatic Contrast (RCC) in CIELAB color space:
            RCC = mean(a*_ROI) - mean(a*_reference)

        DOCUMENTED SCIENTIFIC LIMITATIONS:
        - RCC is strictly a relative image-color difference along the red-green chromatic axis.
        - It is NOT a direct measurement of hemoglobin, blood flow, inflammation, capillary dilation,
          or vascular activity.
        - ITA degrees are exploratory surface colorimetry metrics (Chardon et al., 1991),
          NOT Fitzpatrick phototypes and NOT diagnostic classifications.
        """
        is_valid, msg = self.validate_image_input(img_bgr)
        if not is_valid:
            return {"error": msg}

        img_h, img_w, _ = img_bgr.shape
        if len(roi_box) != 4 or len(ref_box) != 4:
            return {"error": "Bounding boxes must be 4-tuples (x, y, w, h)."}

        rx, ry, rw, rh = roi_box
        fx, fy, fw, fh = ref_box

        # Boundary and dimension checks
        if rw <= 0 or rh <= 0 or rx < 0 or ry < 0 or (rx + rw) > img_w or (ry + rh) > img_h:
            return {"error": f"Target ROI out of bounds or invalid size: {roi_box}"}
        if fw <= 0 or fh <= 0 or fx < 0 or fy < 0 or (fx + fw) > img_w or (fy + fh) > img_h:
            return {"error": f"Reference ROI out of bounds or invalid size: {ref_box}"}

        # Convert to CIE L*a*b* using standard OpenCV mapping:
        # L* in [0, 100], a* in [-128, 127], b* in [-128, 127]
        lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB).astype(np.float32)
        L_channel = lab[:, :, 0] * (100.0 / 255.0)
        a_channel = lab[:, :, 1] - 128.0
        b_channel = lab[:, :, 2] - 128.0

        a_roi = a_channel[ry:ry+rh, rx:rx+rw]
        a_ref = a_channel[fy:fy+fh, fx:fx+fw]

        mean_a_roi = float(np.mean(a_roi))
        mean_a_ref = float(np.mean(a_ref))
        rcc = mean_a_roi - mean_a_ref

        # Numerically stable Individual Typology Angle (ITA) on healthy reference skin
        mean_L_ref = float(np.mean(L_channel[fy:fy+fh, fx:fx+fw]))
        mean_b_ref = float(np.mean(b_channel[fy:fy+fh, fx:fx+fw]))
        
        delta_L = mean_L_ref - 50.0
        if abs(mean_b_ref) < 1e-4:
            # Handle b* near zero singularity smoothly
            if delta_L > 0:
                ita_deg = 90.0
            elif delta_L < 0:
                ita_deg = -90.0
            else:
                ita_deg = 0.0
        else:
            ita_deg = float(np.arctan(delta_L / mean_b_ref) * (180.0 / np.pi))

        return {
            "relative_chromatic_contrast_rcc": round(rcc, 3),
            "mean_a_target_roi": round(mean_a_roi, 3),
            "mean_a_reference": round(mean_a_ref, 3),
            "exploratory_ita_degrees": round(ita_deg, 2),
            "exploratory_ita_color_category": self._classify_ita_color_category(ita_deg),
            "scientific_note": "RCC is a relative image-chromatic difference, NOT a physiological vascular measurement."
        }

    def calculate_glcm_texture(
        self,
        img_bgr: np.ndarray,
        crop_box: Tuple[int, int, int, int],
        standard_res: int = 256
    ) -> Dict[str, Any]:
        """
        Calculates Gray-Level Co-occurrence Matrix (GLCM) exploratory texture descriptors.
        
        DOCUMENTED LIMITATION:
        GLCM descriptors describe image spatial grayscale intensity patterns.
        They do NOT measure stratum corneum barrier thickness, transepidermal water loss (TEWL),
        or lipid bilayer integrity.
        """
        is_valid, msg = self.validate_image_input(img_bgr)
        if not is_valid:
            return {"error": msg}

        if len(crop_box) != 4:
            return {"error": "Crop box must be (x, y, w, h)."}

        x, y, w, h = crop_box
        img_h, img_w, _ = img_bgr.shape
        if w < 16 or h < 16 or x < 0 or y < 0 or (x + w) > img_w or (y + h) > img_h:
            return {"error": f"Crop box out of bounds or too small (<16px): {crop_box}"}

        # 1. Standardize resolution to eliminate resolution-dependent GLCM bias
        sub_img = img_bgr[y:y+h, x:x+w]
        resized = cv2.resize(sub_img, (standard_res, standard_res), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

        # 2. Quantize to 16 gray levels (suppresses high-frequency sensor read noise)
        gray_16 = (gray // 16).astype(np.uint8)

        # 3. Compute GLCM at distance 1, 4 canonical symmetric directions (0, 45, 90, 135 deg)
        angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]
        glcm = graycomatrix(gray_16, distances=[1], angles=angles, levels=16, symmetric=True, normed=True)

        contrast = float(np.mean(graycoprops(glcm, 'contrast')))
        homogeneity = float(np.mean(graycoprops(glcm, 'homogeneity')))
        energy = float(np.mean(graycoprops(glcm, 'energy')))

        return {
            "texture_contrast": round(contrast, 4),
            "texture_homogeneity": round(homogeneity, 4),
            "texture_energy": round(energy, 5),
            "standardized_patch_size": f"{standard_res}x{standard_res}",
            "quantization_levels": 16,
            "scientific_note": "Exploratory image-texture descriptors only. NOT a measure of skin barrier or TEWL."
        }

    def _classify_ita_color_category(self, ita: float) -> str:
        """
        Exploratory image-derived chromatic category based on published ITA angle bands
        (Chardon et al., 1991).
        
        NOTE: These are surface chromatic descriptors, NOT Fitzpatrick skin phototypes.
        """
        if ita > 55: return "Very Light (ITA > 55 deg)"
        elif ita > 41: return "Light (41 deg < ITA <= 55 deg)"
        elif ita > 28: return "Intermediate (28 deg < ITA <= 41 deg)"
        elif ita > 10: return "Tan (10 deg < ITA <= 28 deg)"
        elif ita > -30: return "Brown (-30 deg < ITA <= 10 deg)"
        else: return "Dark (ITA <= -30 deg)"


# Backwards compatibility alias
OptiChromaCoreV2_2 = OptiChromaCoreV2_3

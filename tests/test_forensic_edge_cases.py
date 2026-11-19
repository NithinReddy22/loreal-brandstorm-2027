"""
Forensic Verification Test Suite for OptiChroma v2.3
===================================================
Rigorous verification of edge cases, mathematical stability, input validation,
boundary conditions, and scientific governance constraints.
"""

import pytest
import numpy as np
import cv2
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from optichroma_v2_3_core import OptiChromaCoreV2_3


@pytest.fixture
def engine():
    return OptiChromaCoreV2_3()


# ---------------------------------------------------------------------------
# 1. Invalid Image Dimensions & Shapes
# ---------------------------------------------------------------------------

def test_invalid_dimensions_1d_and_2d(engine):
    # 1D array
    arr_1d = np.zeros(300, dtype=np.uint8)
    valid, msg = engine.validate_image_input(arr_1d)
    assert not valid
    assert "3-dimensional" in msg

    # 2D array
    arr_2d = np.zeros((300, 300), dtype=np.uint8)
    valid, msg = engine.validate_image_input(arr_2d)
    assert not valid
    assert "3-dimensional" in msg


def test_invalid_dimensions_4d(engine):
    # 4D batch tensor
    arr_4d = np.zeros((1, 300, 300, 3), dtype=np.uint8)
    valid, msg = engine.validate_image_input(arr_4d)
    assert not valid
    assert "3-dimensional" in msg


def test_invalid_channel_count(engine):
    # 4-channel RGBA
    arr_rgba = np.zeros((300, 300, 4), dtype=np.uint8)
    valid, msg = engine.validate_image_input(arr_rgba)
    assert not valid
    assert "exactly 3 color channels" in msg

    # 1-channel with 3D shape (H, W, 1)
    arr_1ch = np.zeros((300, 300, 1), dtype=np.uint8)
    valid, msg = engine.validate_image_input(arr_1ch)
    assert not valid
    assert "exactly 3 color channels" in msg


def test_sub_minimum_dimensions(engine):
    # Below 200x200 minimum requirement
    small_1 = np.zeros((199, 300, 3), dtype=np.uint8)
    valid, msg = engine.validate_image_input(small_1)
    assert not valid
    assert "too small" in msg

    small_2 = np.zeros((300, 150, 3), dtype=np.uint8)
    valid, msg = engine.validate_image_input(small_2)
    assert not valid
    assert "too small" in msg


# ---------------------------------------------------------------------------
# 2. Empty Arrays
# ---------------------------------------------------------------------------

def test_empty_arrays(engine):
    # Zero-size 1D array
    empty_1 = np.array([], dtype=np.uint8)
    valid, msg = engine.validate_image_input(empty_1)
    assert not valid
    assert "empty" in msg or "size 0" in msg

    # Zero-dimension 3D array (0, 0, 3)
    empty_3d = np.zeros((0, 0, 3), dtype=np.uint8)
    valid, msg = engine.validate_image_input(empty_3d)
    assert not valid


# ---------------------------------------------------------------------------
# 3. Unsupported Data Types
# ---------------------------------------------------------------------------

def test_unsupported_dtypes(engine):
    for bad_dtype in [np.float32, np.float64, np.int32, np.int64, np.uint16, bool]:
        img = np.zeros((300, 300, 3), dtype=bad_dtype)
        valid, msg = engine.validate_image_input(img)
        assert not valid
        assert "must have dtype uint8" in msg


def test_non_numpy_types(engine):
    for bad_input in [None, "image_string", [1, 2, 3], {"img": 1}, 12345]:
        valid, msg = engine.validate_image_input(bad_input)
        assert not valid
        assert ("numpy.ndarray" in msg) or ("None" in msg)


# ---------------------------------------------------------------------------
# 4. Missing / Out-of-Bounds Calibration Patches
# ---------------------------------------------------------------------------

def test_missing_and_oob_patches(engine):
    img = np.full((400, 400, 3), 100, dtype=np.uint8)

    # Completely outside image
    valid, data = engine.detect_and_validate_reference_patch(img, (450, 450, 30, 30))
    assert not valid
    assert "out of bounds" in data["error"]

    # Negative coordinates
    valid, data = engine.detect_and_validate_reference_patch(img, (-10, 50, 30, 30))
    assert not valid
    assert "out of bounds" in data["error"]

    # Patch size smaller than 10x10 minimum
    valid, data = engine.detect_and_validate_reference_patch(img, (50, 50, 8, 8))
    assert not valid
    assert "too small" in data["error"]

    # Malformed tuple
    valid, data = engine.detect_and_validate_reference_patch(img, (50, 50, 30))
    assert not valid
    assert "must be (x, y, w, h)" in data["error"]


# ---------------------------------------------------------------------------
# 5. Clipped Calibration Patches
# ---------------------------------------------------------------------------

def test_clipped_calibration_patches(engine):
    img = np.full((400, 400, 3), 100, dtype=np.uint8)

    # Completely black patch (<10 DN)
    img[20:60, 20:60] = [5, 5, 5]
    valid, data = engine.detect_and_validate_reference_patch(img, (20, 20, 40, 40))
    assert not valid
    assert data["is_clipped"] is True

    # Saturated white patch (>245 DN)
    img[20:60, 20:60] = [250, 250, 250]
    valid, data = engine.detect_and_validate_reference_patch(img, (20, 20, 40, 40))
    assert not valid
    assert data["is_clipped"] is True


# ---------------------------------------------------------------------------
# 6. Extreme Normalization Gains
# ---------------------------------------------------------------------------

def test_extreme_normalization_gains_clamping(engine):
    img = np.full((400, 400, 3), 80, dtype=np.uint8)

    # Very dark patch (mean = 20) -> nominal gain = 118 / 20 = 5.9, should clamp to max_gain (2.5)
    img[20:60, 20:60] = [20, 20, 20]
    norm_img, report = engine.reference_assisted_normalize(img, (20, 20, 40, 40))
    assert report["normalized"] is True
    assert report["applied_gains"] == (2.5, 2.5, 2.5)

    # Very bright patch (mean = 240) -> nominal gain = 118 / 240 = 0.491 -> inside [0.4, 2.5]
    img[20:60, 20:60] = [240, 240, 240]
    norm_img, report = engine.reference_assisted_normalize(img, (20, 20, 40, 40))
    assert report["normalized"] is True
    assert 0.4 <= report["applied_gains"][0] <= 0.5


# ---------------------------------------------------------------------------
# 7. Empty or Out-of-Bounds ROIs in RCC
# ---------------------------------------------------------------------------

def test_rcc_empty_and_oob_rois(engine):
    img = np.full((400, 400, 3), 120, dtype=np.uint8)

    # Target ROI with zero dimension
    res = engine.calculate_relative_chromatic_contrast(img, (50, 50, 0, 50), (100, 100, 50, 50))
    assert "error" in res

    # Negative ROI width/height
    res = engine.calculate_relative_chromatic_contrast(img, (50, 50, -10, 50), (100, 100, 50, 50))
    assert "error" in res

    # Out of bounds ROI
    res = engine.calculate_relative_chromatic_contrast(img, (380, 380, 50, 50), (100, 100, 50, 50))
    assert "error" in res

    # Malformed tuple
    res = engine.calculate_relative_chromatic_contrast(img, (50, 50, 50), (100, 100, 50, 50))
    assert "error" in res


# ---------------------------------------------------------------------------
# 8. Multi-Resolution Robustness
# ---------------------------------------------------------------------------

def test_different_image_resolutions(engine):
    resolutions = [
        (200, 200),    # Minimum resolution
        (640, 480),    # Standard VGA
        (1280, 720),   # 720p HD
        (1920, 1080),  # 1080p Full HD
        (2500, 2500)   # High resolution square
    ]

    for w, h in resolutions:
        # Create image with a synthetic sharp high-contrast block and a reference patch
        img = np.full((h, w, 3), 100, dtype=np.uint8)
        # Sharp high-frequency texture in top corner
        for i in range(0, min(200, h), 10):
            for j in range(0, min(200, w), 10):
                if (i // 10 + j // 10) % 2 == 0:
                    img[i:i+10, j:j+10] = [180, 180, 180]
                else:
                    img[i:i+10, j:j+10] = [20, 20, 20]

        # In-frame reference patch at bottom corner
        pw, ph = 40, 40
        px, py = w - pw - 20, h - ph - 20
        img[py:py+ph, px:px+pw] = [110, 110, 110]

        # 1. Quality gate
        passed, q_res = engine.quality_gate(img)
        assert q_res["passed"] is True

        # 2. Patch detection
        valid_p, p_res = engine.detect_and_validate_reference_patch(img, (px, py, pw, ph))
        assert valid_p is True

        # 3. Circular ROI
        mask, (cx, cy, r) = engine.extract_physical_skin_roi(img)
        assert mask is not None
        assert mask.shape == (h, w)


# ---------------------------------------------------------------------------
# 9. Constant and Near-Constant Images
# ---------------------------------------------------------------------------

def test_constant_images_rejected_by_quality_gate(engine):
    # Pure black image
    black_img = np.zeros((300, 300, 3), dtype=np.uint8)
    passed, res = engine.quality_gate(black_img)
    assert not passed
    assert res["sharpness_pass"] is False
    assert res["exposure_pass"] is False  # Shadow clipping

    # Pure white image
    white_img = np.full((300, 300, 3), 255, dtype=np.uint8)
    passed, res = engine.quality_gate(white_img)
    assert not passed
    assert res["sharpness_pass"] is False
    assert res["exposure_pass"] is False  # Saturation clipping

    # Pure uniform gray image (128)
    gray_img = np.full((300, 300, 3), 128, dtype=np.uint8)
    passed, res = engine.quality_gate(gray_img)
    assert not passed
    assert res["sharpness_pass"] is False
    assert res["tenengrad_sharpness"] == 0.0


# ---------------------------------------------------------------------------
# 10. Invalid GLCM Crop Coordinates
# ---------------------------------------------------------------------------

def test_invalid_glcm_crop_coordinates(engine):
    img = np.full((300, 300, 3), 120, dtype=np.uint8)

    # Negative coordinates
    res = engine.calculate_glcm_texture(img, (-5, 20, 50, 50))
    assert "error" in res

    # Out of bounds width
    res = engine.calculate_glcm_texture(img, (200, 200, 120, 50))
    assert "error" in res

    # Dimensions too small (<16px)
    res = engine.calculate_glcm_texture(img, (50, 50, 12, 12))
    assert "error" in res

    # Non-square valid crop should succeed by resizing to standard_res
    res_rect = engine.calculate_glcm_texture(img, (50, 50, 100, 60))
    assert "texture_contrast" in res_rect


# ---------------------------------------------------------------------------
# 11. Numerical Stability & Terminology in ITA Calculations
# ---------------------------------------------------------------------------

def test_ita_numerical_stability(engine):
    img = np.full((300, 300, 3), 128, dtype=np.uint8)

    # Test 1: Neutral grey image where b* channel is 0 (mean_b_ref = 0)
    # L* = 128 * (100 / 255) = 50.196 -> delta_L = +0.196
    # With b* = 0, delta_L > 0 -> ita should be +90.0 deg without division by zero!
    res = engine.calculate_relative_chromatic_contrast(
        img,
        roi_box=(50, 50, 40, 40),
        ref_box=(150, 150, 40, 40)
    )
    assert "exploratory_ita_degrees" in res
    assert abs(res["exploratory_ita_degrees"] - 90.0) < 0.1
    # Check that category label is strictly descriptive color category, NOT Fitzpatrick
    assert "exploratory_ita_color_category" in res
    assert "Very Light" in res["exploratory_ita_color_category"]
    assert "Fitzpatrick" not in res["exploratory_ita_color_category"]


def test_ita_with_cool_negative_b_star(engine):
    # Create image with bluish tint where b* is negative
    # In BGR: high Blue, low Red/Green -> Lab b* is negative
    cool_img = np.zeros((300, 300, 3), dtype=np.uint8)
    cool_img[:, :] = [220, 100, 60]  # Blue=220, Green=100, Red=60

    res = engine.calculate_relative_chromatic_contrast(
        cool_img,
        roi_box=(50, 50, 40, 40),
        ref_box=(150, 150, 40, 40)
    )
    assert "exploratory_ita_degrees" in res
    # Should calculate without throwing an exception or clamping negative b* to +0.1
    assert isinstance(res["exploratory_ita_degrees"], float)

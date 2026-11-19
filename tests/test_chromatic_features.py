"""
Unit Tests for Relative Chromatic Contrast (RCC) and ITA Calculations
"""

import pytest
import numpy as np
import cv2
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from optichroma_v2_2_core import OptiChromaCoreV2_2

@pytest.fixture
def engine():
    return OptiChromaCoreV2_2()

def test_rcc_expected_contrast(engine):
    # Create baseline image
    img = np.full((400, 400, 3), 120, dtype=np.uint8)

    # Reference region (healthy skin proxy): neutral skin tone (e.g., [110, 130, 160] in BGR)
    img[200:260, 50:110] = [110, 130, 160]

    # Target ROI (hyperemic/redness shift): increase red channel
    img[200:260, 200:260] = [110, 130, 210]  # Higher Red in BGR

    res = engine.calculate_relative_chromatic_contrast(
        img,
        roi_box=(200, 200, 60, 60),
        ref_box=(50, 200, 60, 60)
    )

    assert "relative_chromatic_contrast_rcc" in res
    # Red shifted target must have positive RCC (greater a* in CIELAB)
    assert res["relative_chromatic_contrast_rcc"] > 0
    assert res["mean_a_target_roi"] > res["mean_a_reference"]

def test_rcc_zero_difference(engine):
    # Identical regions must yield zero RCC
    img = np.full((400, 400, 3), 130, dtype=np.uint8)
    res = engine.calculate_relative_chromatic_contrast(
        img,
        roi_box=(100, 100, 50, 50),
        ref_box=(200, 200, 50, 50)
    )
    assert abs(res["relative_chromatic_contrast_rcc"]) < 0.001

def test_rcc_out_of_bounds_handled(engine):
    img = np.full((400, 400, 3), 120, dtype=np.uint8)
    # ROI extends beyond 400x400
    res = engine.calculate_relative_chromatic_contrast(
        img,
        roi_box=(380, 380, 50, 50),
        ref_box=(50, 50, 40, 40)
    )
    assert "error" in res

def test_physical_skin_roi_mask(engine):
    img = np.zeros((400, 400, 3), dtype=np.uint8)
    mask, (cx, cy, r) = engine.extract_physical_skin_roi(img, radius_ratio=0.35)
    assert mask.shape == (400, 400)
    assert cx == 200 and cy == 200
    assert r == int(400 * 0.35)
    # Center pixel must be 255 (skin)
    assert mask[200, 200] == 255
    # Corner pixel must be 0 (outside)
    assert mask[10, 10] == 0

"""
Unit Tests for In-Frame Calibration and Normalization
"""

import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from optichroma_v2_2_core import OptiChromaCoreV2_2

@pytest.fixture
def engine():
    return OptiChromaCoreV2_2(target_grey_val=118.0)

def test_detect_and_validate_good_patch(engine):
    img = np.full((400, 400, 3), 100, dtype=np.uint8)
    # Define uniform grey patch at (20, 20, 50, 50) with value [100, 100, 100]
    img[20:70, 20:70] = [100, 100, 100]

    valid, data = engine.detect_and_validate_reference_patch(img, (20, 20, 50, 50))
    assert valid is True
    assert data["is_clipped"] is False
    assert data["is_uniform"] is True
    assert data["mean_bgr"] == (100.0, 100.0, 100.0)

def test_detect_clipped_patch(engine):
    img = np.full((400, 400, 3), 100, dtype=np.uint8)
    # Saturated white patch
    img[20:70, 20:70] = [255, 255, 255]

    valid, data = engine.detect_and_validate_reference_patch(img, (20, 20, 50, 50))
    assert valid is False
    assert data["is_clipped"] is True

def test_detect_non_uniform_patch(engine):
    img = np.full((400, 400, 3), 100, dtype=np.uint8)
    # Non-uniform patch with high variance
    img[20:70, 20:45] = [20, 20, 20]
    img[20:70, 45:70] = [200, 200, 200]

    valid, data = engine.detect_and_validate_reference_patch(img, (20, 20, 50, 50), max_std_dev=15.0)
    assert valid is False
    assert data["is_uniform"] is False

def test_normalization_gain_application(engine):
    img = np.full((400, 400, 3), 80, dtype=np.uint8)
    # Patch at mean value 90
    img[20:60, 20:60] = [90, 90, 90]

    norm_img, report = engine.reference_assisted_normalize(img, (20, 20, 40, 40))
    assert report["normalized"] is True
    expected_gain = 118.0 / 90.0
    # Mean of normalized patch should be close to 118
    norm_patch = norm_img[20:60, 20:60]
    assert np.allclose(np.mean(norm_patch), 118.0, atol=2.0)

def test_normalization_fallback_on_invalid_patch(engine):
    img = np.full((400, 400, 3), 80, dtype=np.uint8)
    # Out of bounds patch
    norm_img, report = engine.reference_assisted_normalize(img, (380, 380, 50, 50))
    assert report["normalized"] is False
    assert report["applied_gains"] == (1.0, 1.0, 1.0)
    # Image should remain unchanged
    assert np.array_equal(norm_img, img)

"""
Unit Tests for Image Quality Gate
"""

import pytest
import numpy as np
import cv2
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from optichroma_v2_2_core import OptiChromaCoreV2_2

@pytest.fixture
def engine():
    return OptiChromaCoreV2_2(sharpness_threshold=85.0)

def test_invalid_input_types(engine):
    # Test None input
    passed, res = engine.quality_gate(None)
    assert not passed
    assert "error" in res

    # Test wrong dtype
    float_img = np.zeros((300, 300, 3), dtype=np.float32)
    passed, res = engine.quality_gate(float_img)
    assert not passed

    # Test 2D image instead of 3D
    gray_img = np.zeros((300, 300), dtype=np.uint8)
    passed, res = engine.quality_gate(gray_img)
    assert not passed

    # Test image too small
    small_img = np.zeros((100, 100, 3), dtype=np.uint8)
    passed, res = engine.quality_gate(small_img)
    assert not passed

def test_sharp_image_passes(engine):
    # Synthetic sharp pattern (checkerboard)
    img = np.zeros((400, 400, 3), dtype=np.uint8)
    for i in range(0, 400, 20):
        for j in range(0, 400, 20):
            if (i // 20 + j // 20) % 2 == 0:
                img[i:i+20, j:j+20] = [120, 120, 120]
            else:
                img[i:i+20, j:j+20] = [60, 60, 60]

    passed, details = engine.quality_gate(img)
    assert details["sharpness_pass"] is True
    assert details["tenengrad_sharpness"] > 85.0

def test_blurred_image_rejected(engine):
    # Create smooth, blurred image
    img = np.full((400, 400, 3), 100, dtype=np.uint8)
    # Gaussian blur over flat field has near zero gradient variance
    blurred = cv2.GaussianBlur(img, (25, 25), 0)

    passed, details = engine.quality_gate(blurred)
    assert passed is False
    assert details["sharpness_pass"] is False
    assert details["tenengrad_sharpness"] < 85.0

def test_specular_saturation_rejected(engine):
    # Sharp image with excessive saturated specular glare (>0.8% saturated pixels)
    img = np.random.randint(50, 150, (400, 400, 3), dtype=np.uint8)
    # Inject large saturated patch (100x100 = 10,000 pixels / 160,000 = 6.25% saturation)
    img[150:250, 150:250] = [255, 255, 255]

    passed, details = engine.quality_gate(img)
    assert passed is False
    assert details["exposure_pass"] is False
    assert details["saturation_ratio"] > 0.008

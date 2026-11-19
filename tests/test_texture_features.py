"""
Unit Tests for GLCM Texture Feature Descriptors
"""

import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from optichroma_v2_2_core import OptiChromaCoreV2_2

@pytest.fixture
def engine():
    return OptiChromaCoreV2_2()

def test_glcm_flat_texture(engine):
    # Completely flat image: contrast should be 0, homogeneity should be 1.0
    flat_img = np.full((300, 300, 3), 128, dtype=np.uint8)
    res = engine.calculate_glcm_texture(flat_img, crop_box=(50, 50, 100, 100))

    assert "texture_contrast" in res
    assert res["texture_contrast"] == 0.0
    assert res["texture_homogeneity"] == 1.0
    assert res["texture_energy"] == 1.0

def test_glcm_high_contrast_texture(engine):
    # Pattern with rapid intensity shifts: high contrast, reduced homogeneity vs flat
    pattern = np.zeros((300, 300, 3), dtype=np.uint8)
    for i in range(0, 300, 2):
        for j in range(0, 300, 2):
            if (i // 2 + j // 2) % 2 == 0:
                pattern[i:i+2, j:j+2] = [240, 240, 240]
            else:
                pattern[i:i+2, j:j+2] = [10, 10, 10]

    res = engine.calculate_glcm_texture(pattern, crop_box=(50, 50, 100, 100))
    assert res["texture_contrast"] > 10.0
    # Homogeneity should be noticeably lower than 1.0 (flat image)
    assert res["texture_homogeneity"] < 0.8

def test_glcm_invalid_crop_box(engine):
    img = np.full((300, 300, 3), 100, dtype=np.uint8)
    # Crop box extends past width/height
    res = engine.calculate_glcm_texture(img, crop_box=(250, 250, 80, 80))
    assert "error" in res

    # Crop box too small (<16x16)
    res2 = engine.calculate_glcm_texture(img, crop_box=(50, 50, 10, 10))
    assert "error" in res2

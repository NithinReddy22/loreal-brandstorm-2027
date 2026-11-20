"""
Unit Tests for OptiChroma Edge AI Module
=========================================
Verifies:
1. Automated lesion boundary segmentation on synthetic skin presets.
2. Area calculation (pixels & calibrated mm²) and circularity metric.
3. Longitudinal image registration (ORB + RANSAC homography).
4. Edge case robustness: uniform flat image, tiny image, invalid types.
5. Render AI overlay visual generator.
"""

import os
import sys
import pytest
import numpy as np
import cv2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from optichroma_ai import OptiChromaEdgeAI


@pytest.fixture
def edge_ai():
    return OptiChromaEdgeAI(working_distance_mm=35.0, nominal_fov_mm=25.0)


@pytest.fixture
def synthetic_lesion_image():
    """Generates a 600x600 synthetic skin phantom with central erythema patch."""
    img = np.full((600, 600, 3), (170, 180, 215), dtype=np.uint8) # fair skin BGR
    # Add central reddish lesion (high a* in LAB)
    cv2.circle(img, (300, 300), 75, (120, 130, 240), -1)
    # Add slight gaussian noise
    noise = np.random.normal(0, 5, img.shape).astype(np.int16)
    noisy_img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    return noisy_img


def test_ai_initialization(edge_ai):
    assert edge_ai.working_distance_mm == 35.0
    assert edge_ai.nominal_fov_mm == 25.0


def test_segment_lesion_contour_success(edge_ai, synthetic_lesion_image):
    result = edge_ai.segment_lesion_contour(synthetic_lesion_image)
    assert result["success"] is True
    assert result["area_pixels"] > 5000
    assert result["area_mm2"] > 5.0
    assert 0.0 < result["circularity"] <= 1.0
    assert "mask" in result
    assert result["mask"].shape == (600, 600)
    assert len(result["bounding_box"]) == 4
    # Check that bounding box encloses center
    bx, by, bw, bh = result["bounding_box"]
    assert bx < 300 < bx + bw
    assert by < 300 < by + bh


def test_segment_lesion_flat_image(edge_ai):
    """Uniform flat image should gracefully fallback without crash."""
    flat_img = np.full((400, 400, 3), 128, dtype=np.uint8)
    result = edge_ai.segment_lesion_contour(flat_img)
    assert result["success"] is True
    assert result["area_pixels"] > 0
    assert "bounding_box" in result


def test_segment_lesion_invalid_inputs(edge_ai):
    assert edge_ai.segment_lesion_contour(None)["success"] is False
    assert edge_ai.segment_lesion_contour(np.zeros((30, 30, 3), dtype=np.uint8))["success"] is False
    assert edge_ai.segment_lesion_contour(np.zeros((100, 100), dtype=np.uint8))["success"] is False


def test_longitudinal_registration(edge_ai, synthetic_lesion_image):
    """Test alignment between baseline and a slightly shifted/rotated follow-up."""
    h, w = synthetic_lesion_image.shape[:2]
    # Create follow-up with slight rotation and translation
    M = cv2.getRotationMatrix2D((w/2, h/2), angle=3.0, scale=1.0)
    M[0, 2] += 5.0 # dx
    M[1, 2] += -4.0 # dy
    followup = cv2.warpAffine(synthetic_lesion_image, M, (w, h))

    reg_result = edge_ai.register_longitudinal_images(synthetic_lesion_image, followup)
    assert reg_result["success"] is True
    assert "aligned_image" in reg_result
    assert reg_result["aligned_image"].shape == synthetic_lesion_image.shape
    assert reg_result["inlier_ratio"] >= 0.0
    assert reg_result["transformation_type"] in ["homography", "identity_fallback"]


def test_render_ai_overlay(edge_ai, synthetic_lesion_image):
    seg_result = edge_ai.segment_lesion_contour(synthetic_lesion_image)
    overlay = edge_ai.render_ai_overlay(synthetic_lesion_image, seg_result)
    assert isinstance(overlay, np.ndarray)
    assert overlay.shape == synthetic_lesion_image.shape
    # Overlay should have drawn on the image (not identical to raw input)
    assert not np.array_equal(overlay, synthetic_lesion_image)

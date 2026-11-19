"""
Unit Tests for OptiChroma v2.4 MVP Workflow & Research Module
=============================================================
Verifies the minimum demonstrable patient-clinician documentation workflow
and ensures research features (RCC, ITA, GLCM) remain isolated.
"""

import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from optichroma_v2_4_mvp import (
    SkinObservationRecord,
    CaptureMetadata,
    OptiChromaResearchModule
)


@pytest.fixture
def sharp_image():
    """Generates a synthetic sharp checkerboard image that passes quality gate."""
    img = np.zeros((400, 400, 3), dtype=np.uint8)
    for i in range(0, 400, 20):
        for j in range(0, 400, 20):
            if (i // 20 + j // 20) % 2 == 0:
                img[i:i+20, j:j+20] = [140, 140, 140]
            else:
                img[i:i+20, j:j+20] = [40, 40, 40]
    return img


@pytest.fixture
def blurred_image():
    """Generates a smooth uniform image that fails the Tenengrad focus gate."""
    return np.full((400, 400, 3), 120, dtype=np.uint8)


# ---------------------------------------------------------------------------
# 1. Observation Record Initialization
# ---------------------------------------------------------------------------

def test_record_initialization():
    record = SkinObservationRecord(
        patient_pseudonym="Patient_AB12",
        anatomical_location="Left Inner Volar Forearm"
    )
    assert record.patient_pseudonym == "Patient_AB12"
    assert record.anatomical_location == "Left Inner Volar Forearm"
    assert record.baseline_image is None
    assert len(record.followup_images) == 0


def test_record_init_validation():
    with pytest.raises(ValueError):
        SkinObservationRecord("", "Forearm")
    with pytest.raises(ValueError):
        SkinObservationRecord("Patient_1", "")


# ---------------------------------------------------------------------------
# 2. Baseline & Follow-Up Acquisition with Quality Checks
# ---------------------------------------------------------------------------

def test_baseline_quality_rejection(blurred_image):
    record = SkinObservationRecord("Patient_AB12", "Inner Forearm")
    meta = CaptureMetadata(device_model="Google Pixel 7", acquisition_mode="TIER2_JPEG")
    
    # Blurry image should be rejected
    success, res = record.set_baseline(blurred_image, meta)
    assert success is False
    assert res["accepted"] is False
    assert "Image Quality Gate Rejected" in res["reason"]
    assert record.baseline_image is None


def test_baseline_success(sharp_image):
    record = SkinObservationRecord("Patient_AB12", "Inner Forearm")
    meta = CaptureMetadata(device_model="Google Pixel 7", acquisition_mode="TIER1_RAW", iso=100)
    
    success, res = record.set_baseline(sharp_image, meta)
    assert success is True
    assert res["accepted"] is True
    assert record.baseline_image is not None
    assert record.baseline_metadata["device_model"] == "Google Pixel 7"
    assert record.baseline_metadata["acquisition_mode"] == "TIER1_RAW"


def test_followup_before_baseline_rejected(sharp_image):
    record = SkinObservationRecord("Patient_AB12", "Inner Forearm")
    meta = CaptureMetadata(device_model="Google Pixel 7")
    
    success, res = record.add_followup(sharp_image, meta)
    assert success is False
    assert "Cannot add follow-up before baseline" in res["reason"]


def test_followup_success_sequence(sharp_image):
    record = SkinObservationRecord("Patient_AB12", "Inner Forearm")
    meta1 = CaptureMetadata(device_model="Google Pixel 7", notes="Day 0 Baseline")
    meta2 = CaptureMetadata(device_model="Google Pixel 7", notes="Day 7 Follow-up")
    
    # Establish baseline
    record.set_baseline(sharp_image, meta1)
    
    # Add follow-up
    success, res = record.add_followup(sharp_image, meta2)
    assert success is True
    assert res["stage"] == "followup"
    assert len(record.followup_images) == 1


# ---------------------------------------------------------------------------
# 3. Patient Notes & Clinician Annotations
# ---------------------------------------------------------------------------

def test_patient_and_clinician_annotations():
    record = SkinObservationRecord("Patient_AB12", "Inner Forearm")
    
    # Patient note
    p_note = record.add_patient_note("Mild dryness and flaking observed after showering.")
    assert "dryness" in p_note["note"]
    assert len(record.patient_notes) == 1
    
    # Clinician annotation
    c_annot = record.add_clinician_annotation(
        clinician_id="Dr_Smith_Derm",
        comment="Image quality verified. Continue prescribed supportive moisturizer.",
        request_recapture=False
    )
    assert c_annot["clinician_id"] == "Dr_Smith_Derm"
    assert c_annot["request_recapture"] is False
    assert len(record.clinician_annotations) == 1

    # Clinician recapture request
    c_recapture = record.add_clinician_annotation(
        clinician_id="Dr_Smith_Derm",
        comment="Follow-up capture lighting was uneven. Please recapture flush against skin.",
        request_recapture=True
    )
    assert c_recapture["request_recapture"] is True
    assert len(record.clinician_annotations) == 2


# ---------------------------------------------------------------------------
# 4. Side-by-Side Comparison Canvas
# ---------------------------------------------------------------------------

def test_render_side_by_side_comparison(sharp_image):
    record = SkinObservationRecord("Patient_AB12", "Inner Forearm")
    meta1 = CaptureMetadata(device_model="Google Pixel 7")
    meta2 = CaptureMetadata(device_model="Google Pixel 7")
    
    # When no images exist, returns None
    assert record.render_side_by_side_comparison() is None
    
    record.set_baseline(sharp_image, meta1)
    # When no follow-up exists, returns None
    assert record.render_side_by_side_comparison() is None
    
    record.add_followup(sharp_image, meta2)
    canvas = record.render_side_by_side_comparison(followup_index=0, target_height=300)
    
    assert canvas is not None
    assert isinstance(canvas, np.ndarray)
    # Check that canvas has height = 300 + 35 (banner) = 335
    assert canvas.shape[0] == 335
    # Width should be 2 * 300 + 4 (separator) = 604
    assert canvas.shape[1] == 604
    assert canvas.shape[2] == 3


# ---------------------------------------------------------------------------
# 5. Shareable Consultation Report
# ---------------------------------------------------------------------------

def test_generate_consultation_report(sharp_image):
    record = SkinObservationRecord("Patient_AB12", "Inner Forearm")
    meta = CaptureMetadata(device_model="Google Pixel 7")
    record.set_baseline(sharp_image, meta)
    record.add_patient_note("Test patient symptom note.")
    record.add_clinician_annotation("Pharm_Desk_1", "Patient counseled on barrier cream.")
    
    report = record.generate_consultation_report()
    assert report["record_id"] == record.record_id
    assert report["patient_pseudonym"] == "Patient_AB12"
    assert report["has_baseline"] is True
    assert len(report["patient_notes"]) == 1
    assert len(report["clinician_annotations"]) == 1
    assert "governance_disclaimer" in report
    assert "does NOT provide an autonomous diagnosis" in report["governance_disclaimer"]


# ---------------------------------------------------------------------------
# 6. Isolated Research Module (RCC, ITA, GLCM)
# ---------------------------------------------------------------------------

def test_research_module_isolation(sharp_image):
    research = OptiChromaResearchModule()
    
    # 1. Experimental RCC
    rcc_res = research.compute_experimental_rcc(
        sharp_image,
        roi_box=(50, 50, 40, 40),
        ref_box=(150, 150, 40, 40)
    )
    assert "relative_chromatic_contrast_rcc" in rcc_res
    
    # 2. Research ITA
    ita_res = research.compute_research_ita(sharp_image, ref_box=(100, 100, 40, 40))
    assert "exploratory_ita_degrees" in ita_res
    assert "NOT Fitzpatrick phototype" in ita_res["note"]
    
    # 3. Research GLCM
    glcm_res = research.compute_research_glcm(sharp_image, crop_box=(100, 100, 50, 50))
    assert "texture_contrast" in glcm_res
    assert "texture_homogeneity" in glcm_res

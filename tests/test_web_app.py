"""
Web Application Endpoint Verification Tests
===========================================
Ensures that the interactive prototype Flask application serves all views
and REST endpoints accurately according to the v2.4 MVP baseline.
"""

import sys
import os
import json
import pytest

# Add root and src to path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
if os.path.join(ROOT_DIR, "src") not in sys.path:
    sys.path.insert(0, os.path.join(ROOT_DIR, "src"))

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_route(client):
    """Verifies that the main Single Page Application loads successfully."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"LA ROCHE-POSAY" in response.data
    assert b"OPTICHROMA" in response.data


def test_get_presets(client):
    """Verifies that presets list returns valid metadata."""
    response = client.get("/api/presets")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "presets" in data
    assert len(data["presets"]) >= 6
    preset_ids = [p["id"] for p in data["presets"]]
    assert "baseline_day0.png" in preset_ids
    assert "followup_day7.png" in preset_ids
    assert "followup_day28.png" in preset_ids
    assert "artifact_glare_unpolarized.png" in preset_ids


def test_quality_gate_endpoint_valid_baseline(client):
    """Verifies that quality gate endpoint returns PASS for baseline preset."""
    payload = {"image": "/static/presets/baseline_day0.png"}
    response = client.post("/api/quality-gate", json=payload)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["passed"] is True
    assert data["sharpness_pass"] is True
    assert data["exposure_pass"] is True
    assert data["tenengrad_sharpness"] >= 85.0


def test_quality_gate_endpoint_glare_rejection(client):
    """Verifies that quality gate endpoint returns REJECT for glare artifact."""
    payload = {"image": "/static/presets/artifact_glare_unpolarized.png"}
    response = client.post("/api/quality-gate", json=payload)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["passed"] is False
    assert data["saturation_ratio"] > data["saturation_threshold"]


def test_quality_gate_endpoint_blur_rejection(client):
    """Verifies that quality gate endpoint returns REJECT for blur artifact."""
    payload = {"image": "/static/presets/artifact_blur_defocus.png"}
    response = client.post("/api/quality-gate", json=payload)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["passed"] is False
    assert data["sharpness_pass"] is False
    assert data["tenengrad_sharpness"] < data["sharpness_threshold"]


def test_load_sample_case_and_comparison(client):
    """Verifies full loading of sample case and subsequent comparison generation."""
    # Load sample case
    load_resp = client.post("/api/record/load-sample-case")
    assert load_resp.status_code == 200
    load_data = json.loads(load_resp.data)
    assert load_data["success"] is True

    # Check side-by-side comparison image response
    comp_resp = client.get("/api/record/comparison")
    assert comp_resp.status_code == 200
    assert comp_resp.mimetype == "image/jpeg"
    assert len(comp_resp.data) > 1000

    # Check differential heatmap image response
    heat_resp = client.get("/api/record/difference-heatmap")
    assert heat_resp.status_code == 200
    assert heat_resp.mimetype == "image/jpeg"
    assert len(heat_resp.data) > 1000


def test_consultation_report_and_annotation(client):
    """Verifies adding a clinician annotation and retrieving the full report."""
    ann_payload = {
        "clinician_id": "TEST_DERM_99",
        "comment": "Erythema has attenuated noticeably over 7 days.",
        "request_recapture": False
    }
    ann_resp = client.post("/api/record/annotate", json=ann_payload)
    assert ann_resp.status_code == 200
    ann_data = json.loads(ann_resp.data)
    assert ann_data["success"] is True
    assert ann_data["annotation"]["clinician_id"] == "TEST_DERM_99"

    # Fetch report
    rep_resp = client.get("/api/record/report")
    assert rep_resp.status_code == 200
    rep_data = json.loads(rep_resp.data)
    assert rep_data["report_type"] == "La Roche-Posay OptiChroma Visual Documentation Record"
    assert "governance_disclaimer" in rep_data
    assert len(rep_data["clinician_annotations"]) >= 1


def test_research_analysis_endpoint(client):
    """Verifies isolated research analysis endpoint (RCC, ITA, GLCM)."""
    payload = {"image": "/static/presets/baseline_day0.png"}
    res = client.post("/api/research/analyze", json=payload)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert "rcc" in data
    assert "ita" in data
    assert "glcm" in data
    assert "exploratory_ita_degrees" in data["ita"]
    assert "texture_contrast" in data["glcm"]
    assert "texture_homogeneity" in data["glcm"]
    assert "texture_energy" in data["glcm"]


def test_healing_trajectory_endpoint(client):
    """Verifies cliffhanger feature: Chromatic Healing Trajectory (CHT) calculation."""
    # Ensure sample case is loaded
    client.post("/api/record/load-sample-case")
    
    # Request trajectory
    traj_resp = client.get("/api/record/trajectory")
    assert traj_resp.status_code == 200
    data = json.loads(traj_resp.data)
    assert data["has_trajectory"] is True
    assert data["sessions_count"] >= 2
    assert "days" in data
    assert "rcc_values" in data
    assert "net_reduction_pct" in data
    assert "clinical_trend" in data
    # Verified reduction from Day 0 flare to Day 28 resolution
    assert data["net_reduction_pct"] > 50.0

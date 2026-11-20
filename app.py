"""
La Roche-Posay OptiChroma — Interactive Prototype Web Application
==================================================================
L'Oréal Brandstorm 2027 | Playing Field 3: Reinvent the Doctor-Patient Relationship
Classification: Non-Diagnostic Visual Documentation MVP (v2.4 Baseline Freeze)

Single-command launch:
    python app.py
Access via browser:
    http://127.0.0.1:5000
"""

import os
import sys
import base64
import io
from typing import Optional, Tuple, Dict, Any

# Ensure 'src' is in python import path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CURRENT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
import cv2

from optichroma_v2_4_mvp import SkinObservationRecord, CaptureMetadata, OptiChromaResearchModule
from optichroma_v2_3_core import OptiChromaCoreV2_3

# Initialize Flask application with explicit template and static directories
app = Flask(
    __name__,
    template_folder=os.path.join(SRC_DIR, "web_ui", "templates"),
    static_folder=os.path.join(SRC_DIR, "web_ui", "static")
)

# Global active consultation session (in-memory demonstration record)
active_record = SkinObservationRecord(
    patient_pseudonym="ANON-PT-4091",
    anatomical_location="Right Volar Forearm"
)
core_engine = OptiChromaCoreV2_3()
research_module = OptiChromaResearchModule()


def decode_image_payload(payload: str) -> Optional[np.ndarray]:
    """Decodes image from either a relative static path, file path, or base64 data URI."""
    if not payload:
        return None

    # Handle preset or static file path
    if payload.startswith("/static/"):
        rel_path = payload[len("/static/"):]
        full_path = os.path.join(SRC_DIR, "web_ui", "static", rel_path)
        if os.path.exists(full_path):
            return cv2.imread(full_path)
    elif os.path.exists(payload):
        return cv2.imread(payload)

    # Handle base64 data URI
    if "," in payload:
        payload = payload.split(",", 1)[1]

    try:
        raw_bytes = base64.b64decode(payload)
        arr = np.frombuffer(raw_bytes, dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print(f"Error decoding image: {e}")
        return None


@app.route("/")
def index():
    """Serves the main single-page application."""
    return render_template("index.html")


@app.route("/api/presets", methods=["GET"])
def get_presets():
    """Returns available sample presets."""
    presets = [
        {
            "id": "baseline_day0.png",
            "title": "Baseline Day 0 (Cross-Polarized)",
            "expected_verdict": "PASS",
            "description": "Cross-polarized capture of an erythematous lesion on Day 0 with 18% neutral gray calibration target."
        },
        {
            "id": "followup_day7.png",
            "title": "Follow-Up Day 7 (Soothing Progression)",
            "expected_verdict": "PASS",
            "description": "Standardized Day 7 follow-up showing reduced erythema after topical barrier soothing regimen."
        },
        {
            "id": "artifact_glare_unpolarized.png",
            "title": "Artifact: Unpolarized Glare",
            "expected_verdict": "REJECT",
            "description": "Simulated unpolarized flash capture exhibiting blinding specular reflection clipping."
        },
        {
            "id": "artifact_blur_defocus.png",
            "title": "Artifact: Defocus Blur",
            "expected_verdict": "REJECT",
            "description": "Out-of-focus capture failing the Tenengrad gradient energy threshold."
        },
        {
            "id": "phototype_vi_baseline.png",
            "title": "Inclusivity: Phototype VI (Dark Skin)",
            "expected_verdict": "PASS",
            "description": "Cross-polarized capture on high-melanin skin demonstrating glare-free vascular contrast."
        },
        {
            "id": "phototype_i_baseline.png",
            "title": "Inclusivity: Phototype I (Fair Skin)",
            "expected_verdict": "PASS",
            "description": "Standardized capture on fair skin phototype I with balanced exposure."
        }
    ]
    return jsonify({"presets": presets})


@app.route("/api/quality-gate", methods=["POST"])
def evaluate_quality_gate():
    """Evaluates optical sharpness, specular saturation, and shadow exposure."""
    data = request.get_json() or {}
    image_payload = data.get("image", "")
    img_bgr = decode_image_payload(image_payload)

    if img_bgr is None:
        return jsonify({"passed": False, "error": "Unable to decode image payload."}), 400

    passed, report = core_engine.quality_gate(img_bgr)
    return jsonify(report)


@app.route("/api/record/baseline", methods=["POST"])
def set_baseline():
    """Sets the baseline image for the active consultation record."""
    global active_record
    data = request.get_json() or {}
    img_bgr = decode_image_payload(data.get("image", ""))

    if img_bgr is None:
        return jsonify({"success": False, "error": "Invalid image payload."}), 400

    metadata = CaptureMetadata(
        device_model="Google Pixel 7 (Reference Enclosure)",
        acquisition_mode="TIER2_JPEG",
        iso=100,
        exposure_time_sec=0.02,
        notes="Baseline Day 0 consultation capture."
    )
    passed, resp = active_record.set_baseline(img_bgr, metadata)
    return jsonify({"success": passed, "response": resp})


@app.route("/api/record/followup", methods=["POST"])
def add_followup():
    """Appends a follow-up image to the active consultation record."""
    global active_record
    data = request.get_json() or {}
    img_bgr = decode_image_payload(data.get("image", ""))

    if img_bgr is None:
        return jsonify({"success": False, "error": "Invalid image payload."}), 400

    metadata = CaptureMetadata(
        device_model="Google Pixel 7 (Reference Enclosure)",
        acquisition_mode="TIER2_JPEG",
        iso=100,
        exposure_time_sec=0.02,
        notes="Follow-up Day 7 observation capture."
    )
    passed, resp = active_record.add_followup(img_bgr, metadata)
    return jsonify({"success": passed, "response": resp})


@app.route("/api/record/load-sample-case", methods=["POST"])
def load_sample_case():
    """Loads a full Day 0 vs Day 7 sample case into active record."""
    global active_record
    active_record = SkinObservationRecord(
        patient_pseudonym="ANON-PT-4091",
        anatomical_location="Right Volar Forearm"
    )

    base_path = os.path.join(SRC_DIR, "web_ui", "static", "presets", "baseline_day0.png")
    follow_path = os.path.join(SRC_DIR, "web_ui", "static", "presets", "followup_day7.png")

    b_img = cv2.imread(base_path)
    f_img = cv2.imread(follow_path)

    if b_img is None or f_img is None:
        return jsonify({"success": False, "error": "Preset files missing on disk."}), 500

    meta_b = CaptureMetadata(device_model="Google Pixel 7", notes="Day 0 baseline.")
    meta_f = CaptureMetadata(device_model="Google Pixel 7", notes="Day 7 follow-up.")

    active_record.set_baseline(b_img, meta_b)
    active_record.add_followup(f_img, meta_f)

    active_record.add_clinician_annotation(
        clinician_id="PHARM-PARIS-042",
        comment="Patient completed 7-day application of soothing balm. Longitudinal comparison reveals substantial attenuation of localized erythema.",
        request_recapture=False
    )

    return jsonify({"success": True, "message": "Sample case loaded successfully."})


@app.route("/api/record/comparison", methods=["GET"])
def get_comparison():
    """Renders and returns the standardized side-by-side comparison canvas."""
    global active_record
    canvas = active_record.render_side_by_side_comparison(target_height=420)
    if canvas is None:
        # Fallback empty canvas if images missing
        blank = np.full((300, 600, 3), 40, dtype=np.uint8)
        cv2.putText(blank, "Awaiting Baseline & Follow-Up Images", (80, 160),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
        canvas = blank

    _, encoded = cv2.imencode(".jpg", canvas, [int(cv2.IMWRITE_JPEG_QUALITY), 92])
    return send_file(io.BytesIO(encoded.tobytes()), mimetype="image/jpeg")


@app.route("/api/record/difference-heatmap", methods=["GET"])
def get_difference_heatmap():
    """Renders and returns a differential chromatic heatmap overlay between baseline and follow-up."""
    global active_record
    if active_record.baseline_image is None or len(active_record.followup_images) == 0:
        blank = np.full((300, 600, 3), 40, dtype=np.uint8)
        cv2.putText(blank, "Differential Heatmap Requires 2 Images", (100, 160),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
        _, encoded = cv2.imencode(".jpg", blank)
        return send_file(io.BytesIO(encoded.tobytes()), mimetype="image/jpeg")

    b_img = active_record.baseline_image
    f_img = active_record.followup_images[-1]

    # Resize follow-up to match baseline dimensions if needed
    h, w, _ = b_img.shape
    f_resized = cv2.resize(f_img, (w, h), interpolation=cv2.INTER_AREA)

    # Convert to CIELAB
    b_lab = cv2.cvtColor(b_img, cv2.COLOR_BGR2Lab).astype(np.float32)
    f_lab = cv2.cvtColor(f_resized, cv2.COLOR_BGR2Lab).astype(np.float32)

    # Compute absolute change in the red-green chromatic channel |a*_base - a*_followup|
    delta_a = np.abs(b_lab[:, :, 1] - f_lab[:, :, 1])
    # Normalize with sensitivity scaling (30 delta_a maps to maximum color)
    norm_delta = np.clip((delta_a / 25.0) * 255.0, 0, 255).astype(np.uint8)

    # Apply colormap (INFERNO: black=0 -> purple -> orange -> yellow=max)
    heatmap = cv2.applyColorMap(norm_delta, cv2.COLORMAP_INFERNO)

    # Blend 60% skin background + 40% heatmap
    gray_bg = cv2.cvtColor(cv2.cvtColor(f_resized, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
    blended = cv2.addWeighted(gray_bg, 0.55, heatmap, 0.45, 0)

    # Top banner overlay
    banner = np.full((35, w, 3), 30, dtype=np.uint8)
    cv2.putText(
        banner, "DIFFERENTIAL CHROMATIC HEATMAP (|Δa*| RED-GREEN SHIFT)", (15, 24),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 220, 255), 2, cv2.LINE_AA
    )
    final_view = np.vstack([banner, blended])

    _, encoded = cv2.imencode(".jpg", final_view, [int(cv2.IMWRITE_JPEG_QUALITY), 92])
    return send_file(io.BytesIO(encoded.tobytes()), mimetype="image/jpeg")


@app.route("/api/record/annotate", methods=["POST"])
def add_annotation():
    """Adds clinician observation and severity note."""
    global active_record
    data = request.get_json() or {}
    clinician_id = data.get("clinician_id", "ANON_CLINICIAN")
    comment = data.get("comment", "")
    request_recapture = bool(data.get("request_recapture", False))

    annotation = active_record.add_clinician_annotation(
        clinician_id=clinician_id,
        comment=comment,
        request_recapture=request_recapture
    )
    return jsonify({"success": True, "annotation": annotation})


@app.route("/api/record/report", methods=["GET"])
def get_report():
    """Returns the full consultation report."""
    global active_record
    report = active_record.generate_consultation_report()
    return jsonify(report)


@app.route("/api/research/analyze", methods=["POST"])
def analyze_research():
    """Executes isolated research metrics (RCC, ITA, GLCM) on active image."""
    data = request.get_json() or {}
    img_bgr = decode_image_payload(data.get("image", ""))

    if img_bgr is None:
        return jsonify({"error": "No image loaded."}), 400

    h, w, _ = img_bgr.shape
    # Preset coordinates (x, y, width, height): 18% gray patch at top-left, lesion in center
    ref_box = (30, 30, min(70, w - 35), min(70, h - 35))
    roi_box = (int(w * 0.35), int(h * 0.35), int(w * 0.30), int(h * 0.30))

    rcc_res = research_module.compute_experimental_rcc(img_bgr, roi_box, ref_box)
    ita_res = research_module.compute_research_ita(img_bgr, roi_box)
    glcm_res = research_module.compute_research_glcm(img_bgr, roi_box)

    return jsonify({
        "rcc": rcc_res,
        "ita": ita_res,
        "glcm": glcm_res
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("=" * 70)
    print(" LA ROCHE-POSAY OPTICHROMA™ v2.4 INTERACTIVE PROTOTYPE")
    print(f" Web Server starting on: http://127.0.0.1:{port}")
    print("=" * 70)
    app.run(host="127.0.0.1", port=port, debug=False)

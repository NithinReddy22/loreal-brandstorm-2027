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
import json
import base64
import io
from typing import Optional, Tuple, Dict, Any, List

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
from optichroma_ai import OptiChromaEdgeAI

# Initialize Flask application with explicit template and static directories
app = Flask(
    __name__,
    template_folder=os.path.join(SRC_DIR, "web_ui", "templates"),
    static_folder=os.path.join(SRC_DIR, "web_ui", "static")
)

DATA_DIR = os.path.join(SRC_DIR, "web_ui", "static", "data")
os.makedirs(DATA_DIR, exist_ok=True)
SESSION_FILE = os.path.join(DATA_DIR, "session_state.json")

# Global active consultation session
active_record = SkinObservationRecord(
    patient_pseudonym="ANON-PT-4091",
    anatomical_location="Right Volar Forearm"
)
core_engine = OptiChromaCoreV2_3()
research_module = OptiChromaResearchModule()
edge_ai = OptiChromaEdgeAI()

# Track session days relative to baseline
session_day_offsets: List[int] = [0]


def save_session_state() -> None:
    """Persists active session to disk to prevent data loss on process restart."""
    try:
        report = active_record.generate_consultation_report()
        report["session_day_offsets"] = session_day_offsets
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
    except Exception as e:
        print(f"Warning: Failed to persist session state: {e}")


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


def get_standard_boxes(img_shape: Tuple[int, int, int]) -> Tuple[Tuple[int, int, int, int], Tuple[int, int, int, int], Tuple[int, int, int, int]]:
    """
    Returns verified standardized coordinates (x, y, w, h):
    1. gray_calib_patch: In-frame 18% gray ceramic disc (top-left) for exposure balance.
    2. lesion_roi: Central diagnostic area of interest.
    3. perilesional_skin_ref: Adjacent healthy unaffected skin (NOT the gray disc) for true chromatic contrast.
    """
    h, w, _ = img_shape
    gray_patch = (30, 30, min(75, w - 35), min(75, h - 35))
    lesion_roi = (int(w * 0.35), int(h * 0.35), int(w * 0.30), int(h * 0.30))
    # Unaffected perilesional skin on the left lateral margin
    perilesional_skin_ref = (int(w * 0.05), int(h * 0.35), int(w * 0.18), int(h * 0.25))
    return gray_patch, lesion_roi, perilesional_skin_ref


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
            "title": "Baseline Day 0 (Flare)",
            "expected_verdict": "PASS",
            "description": "Standardized cross-polarized capture of an acute erythematous flare with in-frame calibration target."
        },
        {
            "id": "followup_day7.png",
            "title": "Follow-Up Day 7 (Balm Rx)",
            "expected_verdict": "PASS",
            "description": "7 days post-intervention with topical barrier balm showing initial erythema attenuation."
        },
        {
            "id": "followup_day14.png",
            "title": "Follow-Up Day 14 (Attenuating)",
            "expected_verdict": "PASS",
            "description": "14 days longitudinal capture showing continuous inflammatory reduction."
        },
        {
            "id": "followup_day21.png",
            "title": "Follow-Up Day 21 (Near Resolution)",
            "expected_verdict": "PASS",
            "description": "21 days longitudinal capture showing near-complete contrast resolution."
        },
        {
            "id": "followup_day28.png",
            "title": "Follow-Up Day 28 (Full Resolution)",
            "expected_verdict": "PASS",
            "description": "28 days follow-up confirming stabilized non-erythematous baseline."
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
    global active_record, session_day_offsets
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
    if passed:
        session_day_offsets = [0]
        save_session_state()
    return jsonify({"success": passed, "response": resp})


@app.route("/api/record/followup", methods=["POST"])
def add_followup():
    """Appends a follow-up image to the active consultation record."""
    global active_record, session_day_offsets
    data = request.get_json() or {}
    img_bgr = decode_image_payload(data.get("image", ""))
    day_offset = int(data.get("day_offset", len(active_record.followup_images) * 7 + 7))

    if img_bgr is None:
        return jsonify({"success": False, "error": "Invalid image payload."}), 400

    metadata = CaptureMetadata(
        device_model="Google Pixel 7 (Reference Enclosure)",
        acquisition_mode="TIER2_JPEG",
        iso=100,
        exposure_time_sec=0.02,
        notes=f"Follow-up Day {day_offset} observation capture."
    )
    passed, resp = active_record.add_followup(img_bgr, metadata)
    if passed:
        session_day_offsets.append(day_offset)
        save_session_state()
    return jsonify({"success": passed, "response": resp})


@app.route("/api/record/load-sample-case", methods=["POST"])
def load_sample_case():
    """
    Loads a full 28-day longitudinal clinical case (Day 0, 7, 14, 21, 28)
    demonstrating progressive soothing and clinical resolution.
    """
    global active_record, session_day_offsets
    active_record = SkinObservationRecord(
        patient_pseudonym="ANON-PT-4091",
        anatomical_location="Right Volar Forearm"
    )
    session_day_offsets = [0, 7, 14, 21, 28]

    preset_sequence = [
        ("baseline_day0.png", "Day 0: Acute erythematous flare with pruritus."),
        ("followup_day7.png", "Day 7: Initiated La Roche-Posay Cicaplast Baume B5+ regimen; early erythema softening."),
        ("followup_day14.png", "Day 14: Substantial reduction in peripheral redness; patient reports pruritus resolved."),
        ("followup_day21.png", "Day 21: Lesion boundary contracted; minimal residual pink chromaticity."),
        ("followup_day28.png", "Day 28: Full clinical resolution; skin tone returned to baseline perilesional level.")
    ]

    p_dir = os.path.join(SRC_DIR, "web_ui", "static", "presets")
    for i, (fname, note) in enumerate(preset_sequence):
        fpath = os.path.join(p_dir, fname)
        img = cv2.imread(fpath)
        if img is None:
            continue
        meta = CaptureMetadata(
            device_model="Google Pixel 7 (Reference Enclosure)",
            notes=note
        )
        if i == 0:
            active_record.set_baseline(img, meta)
        else:
            active_record.add_followup(img, meta)

    active_record.add_clinician_annotation(
        clinician_id="PHARM-PARIS-042",
        comment="Patient completed 28-day soothing balm regimen. Objective Chromatic Healing Trajectory demonstrates 98.4% erythema contrast attenuation.",
        request_recapture=False
    )

    save_session_state()
    return jsonify({"success": True, "message": "28-Day Longitudinal Clinical Case loaded successfully."})


@app.route("/api/record/comparison", methods=["GET"])
def get_comparison():
    """Renders and returns the standardized side-by-side comparison canvas."""
    global active_record
    canvas = active_record.render_side_by_side_comparison(target_height=420)
    if canvas is None:
        blank = np.full((320, 640, 3), 35, dtype=np.uint8)
        cv2.putText(blank, "Awaiting Baseline & Follow-Up Images", (90, 165),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
        canvas = blank

    _, encoded = cv2.imencode(".jpg", canvas, [int(cv2.IMWRITE_JPEG_QUALITY), 94])
    return send_file(io.BytesIO(encoded.tobytes()), mimetype="image/jpeg")


@app.route("/api/record/difference-heatmap", methods=["GET"])
def get_difference_heatmap():
    """
    Renders and returns a differential chromatic heatmap overlay between baseline and follow-up
    with an integrated scale bar and publication-grade annotations baked into the image.
    """
    global active_record
    if active_record.baseline_image is None or len(active_record.followup_images) == 0:
        blank = np.full((320, 640, 3), 35, dtype=np.uint8)
        cv2.putText(blank, "Differential Heatmap Requires 2 Images", (100, 165),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
        _, encoded = cv2.imencode(".jpg", blank)
        return send_file(io.BytesIO(encoded.tobytes()), mimetype="image/jpeg")

    b_img = active_record.baseline_image
    f_img = active_record.followup_images[-1]

    h, w, _ = b_img.shape
    f_resized = cv2.resize(f_img, (w, h), interpolation=cv2.INTER_AREA)

    # Convert to CIELAB
    b_lab = cv2.cvtColor(b_img, cv2.COLOR_BGR2Lab).astype(np.float32)
    f_lab = cv2.cvtColor(f_resized, cv2.COLOR_BGR2Lab).astype(np.float32)

    # Compute absolute red-green chromatic shift |a*_base - a*_followup|
    delta_a = np.abs(b_lab[:, :, 1] - f_lab[:, :, 1])
    norm_delta = np.clip((delta_a / 25.0) * 255.0, 0, 255).astype(np.uint8)

    # Apply INFERNO colormap
    heatmap = cv2.applyColorMap(norm_delta, cv2.COLORMAP_INFERNO)
    gray_bg = cv2.cvtColor(cv2.cvtColor(f_resized, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
    blended = cv2.addWeighted(gray_bg, 0.52, heatmap, 0.48, 0)

    # Top Header Banner
    banner_top = np.full((38, w, 3), 28, dtype=np.uint8)
    cv2.putText(
        banner_top, "LA ROCHE-POSAY OPTICHROMA -- DIFFERENTIAL CHROMATIC HEATMAP", (14, 25),
        cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0, 215, 255), 1, cv2.LINE_AA
    )

    # Bottom Integrated Scale Bar (Self-contained in image for exports/screenshots)
    scale_bar_h = 48
    banner_bottom = np.full((scale_bar_h, w, 3), 22, dtype=np.uint8)
    bar_w, bar_h = 240, 12
    bar_x = w - bar_w - 20
    bar_y = 18

    # Create gradient bar
    grad = np.linspace(0, 255, bar_w, dtype=np.uint8).reshape(1, bar_w)
    grad_color = cv2.applyColorMap(grad, cv2.COLORMAP_INFERNO)
    banner_bottom[bar_y:bar_y+bar_h, bar_x:bar_x+bar_w] = grad_color[0]
    cv2.rectangle(banner_bottom, (bar_x - 1, bar_y - 1), (bar_x + bar_w, bar_y + bar_h), (120, 120, 120), 1)

    cv2.putText(
        banner_bottom, "Erythema Shift (|Da*|):", (14, 28),
        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1, cv2.LINE_AA
    )
    cv2.putText(
        banner_bottom, "0.0 (Unchanged)", (bar_x - 100, 28),
        cv2.FONT_HERSHEY_SIMPLEX, 0.38, (160, 160, 160), 1, cv2.LINE_AA
    )
    cv2.putText(
        banner_bottom, ">=25.0 (Resolved)", (bar_x + bar_w + 8, 28),
        cv2.FONT_HERSHEY_SIMPLEX, 0.38, (255, 200, 50), 1, cv2.LINE_AA
    )

    final_view = np.vstack([banner_top, blended, banner_bottom])
    _, encoded = cv2.imencode(".jpg", final_view, [int(cv2.IMWRITE_JPEG_QUALITY), 94])
    return send_file(io.BytesIO(encoded.tobytes()), mimetype="image/jpeg")


@app.route("/api/record/trajectory", methods=["GET"])
def get_healing_trajectory():
    """
    CLIFFHANGER FEATURE: Chromatic Healing Trajectory (CHT)
    Calculates longitudinal Relative Chromatic Contrast (RCC = a*_lesion - a*_perilesional_skin)
    across all sessions to track objective erythema resolution over time.
    """
    global active_record, session_day_offsets
    if active_record.baseline_image is None:
        return jsonify({
            "has_trajectory": False,
            "error": "Baseline capture required."
        })

    all_images = [active_record.baseline_image] + active_record.followup_images
    n_sessions = len(all_images)
    
    # Ensure day offsets match images count
    days = session_day_offsets[:n_sessions]
    while len(days) < n_sessions:
        days.append(days[-1] + 7 if days else 0)

    rcc_values = []
    ita_values = []
    labels = []

    h, w, _ = all_images[0].shape
    _, lesion_roi, perilesional_skin_ref = get_standard_boxes((h, w, 3))

    rx, ry, rw, rh = lesion_roi
    px, py, pw, ph = perilesional_skin_ref

    for i, img in enumerate(all_images):
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab).astype(np.float32)
        L_ch = lab[:, :, 0] * (100.0 / 255.0)
        a_ch = lab[:, :, 1] - 128.0
        b_ch = lab[:, :, 2] - 128.0

        mean_a_lesion = float(np.mean(a_ch[ry:ry+rh, rx:rx+rw]))
        mean_a_peri = float(np.mean(a_ch[py:py+ph, px:px+pw]))
        rcc = round(mean_a_lesion - mean_a_peri, 2)
        rcc_values.append(rcc)

        # ITA on healthy perilesional skin to prove optical stability
        mean_L_peri = float(np.mean(L_ch[py:py+ph, px:px+pw]))
        mean_b_peri = float(np.mean(b_ch[py:py+ph, px:px+pw]))
        delta_L = mean_L_peri - 50.0
        ita = float(np.arctan(delta_L / max(abs(mean_b_peri), 1e-4)) * (180.0 / np.pi))
        ita_values.append(round(ita, 1))

        day_num = days[i]
        if i == 0:
            labels.append(f"Day {day_num} (Baseline Flare)")
        else:
            labels.append(f"Day {day_num} (Follow-Up #{i})")

    baseline_rcc = rcc_values[0]
    current_rcc = rcc_values[-1]

    if abs(baseline_rcc) > 0.1:
        net_reduction = round(((baseline_rcc - current_rcc) / baseline_rcc) * 100.0, 1)
    else:
        net_reduction = 0.0

    if current_rcc <= 1.0 and net_reduction >= 75.0:
        trend = "CLINICALLY RESOLVED (STABLE)"
    elif net_reduction >= 30.0:
        trend = "MARKED IMPROVEMENT"
    elif net_reduction >= -10.0:
        trend = "STABLE / INDETERMINATE"
    else:
        trend = "POSSIBLE FLARE / WORSENING"

    return jsonify({
        "has_trajectory": True,
        "sessions_count": n_sessions,
        "days": days,
        "rcc_values": rcc_values,
        "ita_values": ita_values,
        "labels": labels,
        "baseline_rcc": baseline_rcc,
        "current_rcc": current_rcc,
        "net_reduction_pct": net_reduction,
        "clinical_trend": trend,
        "lesion_roi_box": lesion_roi,
        "perilesional_ref_box": perilesional_skin_ref,
        "scientific_note": "RCC = Da* (lesion ROI vs adjacent perilesional healthy skin). Non-diagnostic image metric."
    })


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
    save_session_state()
    return jsonify({"success": True, "annotation": annotation})


@app.route("/api/record/report", methods=["GET"])
def get_report():
    """Returns the full consultation report."""
    global active_record
    report = active_record.generate_consultation_report()
    return jsonify(report)


@app.route("/api/research/analyze", methods=["POST"])
def analyze_research():
    """
    Executes isolated research metrics (RCC, ITA, GLCM) on active image.
    Scientifically corrected: RCC reference samples healthy perilesional skin, NOT the gray disc!
    """
    data = request.get_json() or {}
    img_bgr = decode_image_payload(data.get("image", ""))

    if img_bgr is None:
        return jsonify({"error": "No image loaded."}), 400

    gray_patch, lesion_roi, perilesional_skin_ref = get_standard_boxes(img_bgr.shape)

    # Scientific correction: RCC is computed against adjacent perilesional skin
    rcc_res = research_module.compute_experimental_rcc(img_bgr, lesion_roi, perilesional_skin_ref)
    # ITA is computed on healthy perilesional skin
    ita_res = research_module.compute_research_ita(img_bgr, perilesional_skin_ref)
    # GLCM texture computed on lesion ROI
    glcm_res = research_module.compute_research_glcm(img_bgr, lesion_roi)

    return jsonify({
        "rcc": rcc_res,
        "ita": ita_res,
        "glcm": glcm_res,
        "perilesional_ref_box": perilesional_skin_ref,
        "gray_calib_patch_box": gray_patch
    })


@app.route("/api/ai/segment", methods=["POST"])
def ai_segment_lesion():
    """
    Explainable Edge AI: Extracts lesion contour, boundary box, circularity,
    and area in mm2 (calibrated against 35mm optical standoff and 25mm FOV).
    """
    data = request.get_json() or {}
    img_bgr = decode_image_payload(data.get("image", ""))
    if img_bgr is None:
        return jsonify({"error": "No image loaded."}), 400

    seg_result = edge_ai.segment_lesion_contour(img_bgr)
    if not seg_result.get("success", False):
        return jsonify(seg_result), 400

    # Render visual AI overlay
    overlay_bgr = edge_ai.render_ai_overlay(img_bgr, seg_result)
    _, buffer = cv2.imencode(".png", overlay_bgr)
    overlay_b64 = "data:image/png;base64," + base64.b64encode(buffer).decode("utf-8")

    return jsonify({
        "success": True,
        "bounding_box": seg_result["bounding_box"],
        "area_pixels": seg_result["area_pixels"],
        "area_mm2": seg_result["area_mm2"],
        "perimeter_px": seg_result.get("perimeter_px", 0),
        "circularity": seg_result["circularity"],
        "mean_lesion_delta_a": seg_result["mean_lesion_delta_a"],
        "contour_points_count": len(seg_result.get("contour_points", [])),
        "overlay_image": overlay_b64,
        "governance_notice": "Explainable contour extraction. Non-diagnostic image metric."
    })


@app.route("/api/ai/align", methods=["POST"])
def ai_align_longitudinal():
    """
    Explainable Edge AI: Aligns follow-up capture to baseline perspective
    using ORB keypoint matching and RANSAC homography.
    """
    global active_record
    if active_record.baseline_image is None:
        return jsonify({"error": "Baseline image must be established first."}), 400

    data = request.get_json() or {}
    followup_img = decode_image_payload(data.get("followup_image", ""))
    if followup_img is None:
        if active_record.followup_images:
            followup_img = active_record.followup_images[-1]
        else:
            return jsonify({"error": "No follow-up image available to align."}), 400

    reg_result = edge_ai.register_longitudinal_images(active_record.baseline_image, followup_img)
    if not reg_result.get("success", False):
        return jsonify(reg_result), 400

    _, buffer = cv2.imencode(".png", reg_result["aligned_image"])
    aligned_b64 = "data:image/png;base64," + base64.b64encode(buffer).decode("utf-8")

    return jsonify({
        "success": True,
        "inlier_ratio": reg_result["inlier_ratio"],
        "matched_keypoints": reg_result["matched_keypoints"],
        "transformation_type": reg_result["transformation_type"],
        "aligned_image": aligned_b64
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("=" * 70)
    print(" LA ROCHE-POSAY OPTICHROMA™ v2.4 INTERACTIVE PROTOTYPE")
    print(f" Web Server starting on: http://127.0.0.1:{port}")
    print("=" * 70)
    app.run(host="127.0.0.1", port=port, debug=False)

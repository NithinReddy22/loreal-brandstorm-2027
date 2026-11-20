"""
OptiChroma MVP Core Module (v2.4 - Frozen Student MVP Baseline)
==============================================================
System: Standardized Optical Smartphone Documentation & Consultation Platform
Classification: Non-Diagnostic Visual Documentation MVP

SCOPE & BOUNDARIES:
- Focuses strictly on:
  1. Standardized image acquisition & quality verification.
  2. Baseline and follow-up longitudinal image storage.
  3. Side-by-side visual comparison.
  4. User and clinician annotations.
  5. Timestamped metadata preservation.
  6. Shareable consultation report generation.
- RCC is retained as an EXPERIMENTAL feature.
- ITA and GLCM are isolated in the RESEARCH module.
- NO autonomous diagnosis, flare prediction, treatment recommendation, or biomarker quantification.
"""

from typing import Dict, Any, Tuple, Optional, List
import uuid
import datetime
import numpy as np
import cv2

# Import core image quality engine
from optichroma_v2_3_core import OptiChromaCoreV2_3


class CaptureMetadata:
    """Metadata container for a captured skin image."""
    def __init__(
        self,
        device_model: str,
        acquisition_mode: str = "TIER2_JPEG",
        iso: Optional[int] = 100,
        exposure_time_sec: Optional[float] = 0.02,
        notes: str = ""
    ) -> None:
        self.timestamp: str = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.device_model: str = str(device_model)
        self.acquisition_mode: str = str(acquisition_mode) # "TIER1_RAW" or "TIER2_JPEG"
        self.iso: Optional[int] = iso
        self.exposure_time_sec: Optional[float] = exposure_time_sec
        self.notes: str = str(notes)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "device_model": self.device_model,
            "acquisition_mode": self.acquisition_mode,
            "iso": self.iso,
            "exposure_time_sec": self.exposure_time_sec,
            "notes": self.notes
        }


class SkinObservationRecord:
    """
    Manages the minimum demonstrable patient-to-dermatologist workflow:
    1. Create skin record.
    2. Add baseline capture with quality verification.
    3. Add follow-up captures.
    4. Render side-by-side comparison.
    5. Generate consultation report.
    6. Record clinician annotations.
    """

    def __init__(self, patient_pseudonym: str, anatomical_location: str) -> None:
        if not patient_pseudonym or not anatomical_location:
            raise ValueError("Patient pseudonym and anatomical location are required.")

        self.record_id: str = str(uuid.uuid4())
        self.patient_pseudonym: str = patient_pseudonym
        self.anatomical_location: str = anatomical_location
        self.created_at: str = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        self.engine = OptiChromaCoreV2_3()
        
        self.baseline_image: Optional[np.ndarray] = None
        self.baseline_metadata: Optional[Dict[str, Any]] = None
        self.baseline_quality: Optional[Dict[str, Any]] = None
        
        self.followup_images: List[np.ndarray] = []
        self.followup_metadata: List[Dict[str, Any]] = []
        self.followup_quality: List[Dict[str, Any]] = []
        
        self.patient_notes: List[Dict[str, str]] = []
        self.clinician_annotations: List[Dict[str, Any]] = []

    def set_baseline(
        self,
        img_bgr: np.ndarray,
        metadata: CaptureMetadata
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Validates and sets the baseline skin image.
        Rejects capture if blur or specular glare exceeds quality thresholds.
        """
        passed, q_report = self.engine.quality_gate(img_bgr)
        if not passed:
            return False, {
                "accepted": False,
                "reason": "Image Quality Gate Rejected capture.",
                "quality_report": q_report
            }

        self.baseline_image = img_bgr.copy()
        self.baseline_metadata = metadata.to_dict()
        self.baseline_quality = q_report
        return True, {
            "accepted": True,
            "record_id": self.record_id,
            "stage": "baseline",
            "quality_report": q_report
        }

    def add_followup(
        self,
        img_bgr: np.ndarray,
        metadata: CaptureMetadata
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Validates and appends a follow-up longitudinal skin image.
        """
        if self.baseline_image is None:
            return False, {
                "accepted": False,
                "reason": "Cannot add follow-up before baseline image is established."
            }

        passed, q_report = self.engine.quality_gate(img_bgr)
        if not passed:
            return False, {
                "accepted": False,
                "reason": "Image Quality Gate Rejected capture.",
                "quality_report": q_report
            }

        self.followup_images.append(img_bgr.copy())
        self.followup_metadata.append(metadata.to_dict())
        self.followup_quality.append(q_report)
        return True, {
            "accepted": True,
            "record_id": self.record_id,
            "stage": "followup",
            "followup_index": len(self.followup_images) - 1,
            "quality_report": q_report
        }

    def add_patient_note(self, note_text: str) -> Dict[str, str]:
        """Allows patient to add a symptom or context note."""
        entry = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "note": str(note_text)
        }
        self.patient_notes.append(entry)
        return entry

    def add_clinician_annotation(
        self,
        clinician_id: str,
        comment: str,
        request_recapture: bool = False
    ) -> Dict[str, Any]:
        """Allows reviewing clinician/pharmacist to log observations or request recapture."""
        annotation = {
            "annotation_id": str(uuid.uuid4()),
            "clinician_id": str(clinician_id),
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "comment": str(comment),
            "request_recapture": bool(request_recapture)
        }
        self.clinician_annotations.append(annotation)
        return annotation

    def render_side_by_side_comparison(
        self,
        followup_index: int = -1,
        target_height: int = 420
    ) -> Optional[np.ndarray]:
        """
        Renders a publication-grade, standardized clinical side-by-side
        comparison canvas between baseline and specified follow-up image.
        Includes clinical metadata headers, calibrated 10mm scale bar,
        and optical quality indicators.
        """
        if self.baseline_image is None or len(self.followup_images) == 0:
            return None

        if followup_index < 0:
            followup_index = len(self.followup_images) + followup_index

        if followup_index < 0 or followup_index >= len(self.followup_images):
            return None

        followup_img = self.followup_images[followup_index]

        # Resize both images to uniform height maintaining aspect ratio
        def resize_to_h(img: np.ndarray, h: int) -> np.ndarray:
            orig_h, orig_w, _ = img.shape
            w = int(orig_w * (h / orig_h))
            return cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)

        b_resized = resize_to_h(self.baseline_image, target_height)
        f_resized = resize_to_h(followup_img, target_height)

        # Concatenate horizontally with a crisp separator bar
        separator_w = 4
        separator = np.full((target_height, separator_w, 3), 45, dtype=np.uint8)
        canvas = np.hstack([b_resized, separator, f_resized])
        total_w = canvas.shape[1]

        # 1. Master Clinical Header Banner (Navy/Graphite)
        header_h = 56
        header = np.full((header_h, total_w, 3), (25, 20, 15), dtype=np.uint8) # Dark BGR

        cv2.putText(
            header, "LA ROCHE-POSAY OPTICHROMA - STANDARDIZED CLINICAL COMPARISON", (16, 24),
            cv2.FONT_HERSHEY_DUPLEX, 0.52, (255, 255, 255), 1, cv2.LINE_AA
        )
        subhead = f"Patient: {self.patient_pseudonym}  |  Site: {self.anatomical_location}  |  Non-Diagnostic Documentation"
        cv2.putText(
            header, subhead, (16, 44),
            cv2.FONT_HERSHEY_SIMPLEX, 0.38, (160, 175, 190), 1, cv2.LINE_AA
        )

        # 2. Stage Sub-Banners directly above images
        sub_h = 32
        sub_banner = np.full((sub_h, total_w, 3), (35, 30, 25), dtype=np.uint8)
        
        # Baseline label
        b_tg = self.baseline_quality.get("tenengrad_energy", 0.0) if self.baseline_quality else 0.0
        b_label = f"BASELINE (DAY 0)  |  Sharpness: {b_tg:.1f}"
        cv2.putText(
            sub_banner, b_label, (16, 21),
            cv2.FONT_HERSHEY_SIMPLEX, 0.44, (0, 205, 255), 1, cv2.LINE_AA
        )

        # Follow-up label
        f_tg = self.followup_quality[followup_index].get("tenengrad_energy", 0.0) if self.followup_quality else 0.0
        f_x = b_resized.shape[1] + separator_w + 16
        f_label = f"FOLLOW-UP #{followup_index + 1}  |  Sharpness: {f_tg:.1f}"
        cv2.putText(
            sub_banner, f_label, (f_x, 21),
            cv2.FONT_HERSHEY_SIMPLEX, 0.44, (0, 255, 140), 1, cv2.LINE_AA
        )

        # 3. Footer Bar with Calibrated 10mm Optical Scale Bar
        footer_h = 30
        footer = np.full((footer_h, total_w, 3), (25, 20, 15), dtype=np.uint8)
        
        disclaimer = "Cross-Polarized Optical Imaging | Extinction >100:1 | 5000K Calibrated High-CRI"
        cv2.putText(
            footer, disclaimer, (16, 19),
            cv2.FONT_HERSHEY_SIMPLEX, 0.36, (140, 150, 160), 1, cv2.LINE_AA
        )

        # 10 mm scale bar on right side (nominal FOV = 25mm across 420px height)
        scale_px = int((10.0 / 25.0) * (b_resized.shape[1]))
        bar_x1 = total_w - scale_px - 25
        bar_x2 = total_w - 25
        bar_y = 15
        cv2.line(footer, (bar_x1, bar_y), (bar_x2, bar_y), (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(
            footer, "10 mm", (bar_x1 - 42, 19),
            cv2.FONT_HERSHEY_SIMPLEX, 0.36, (255, 255, 255), 1, cv2.LINE_AA
        )

        final_comparison = np.vstack([header, sub_banner, canvas, footer])
        return final_comparison

    def generate_consultation_report(self) -> Dict[str, Any]:
        """
        Compiles a structured, non-diagnostic consultation report
        for review between patient, pharmacist, and physician.
        """
        return {
            "report_type": "La Roche-Posay OptiChroma Visual Documentation Record",
            "version": "2.4.0 (MVP)",
            "record_id": self.record_id,
            "created_at": self.created_at,
            "patient_pseudonym": self.patient_pseudonym,
            "anatomical_location": self.anatomical_location,
            "has_baseline": self.baseline_image is not None,
            "baseline_metadata": self.baseline_metadata,
            "baseline_quality": self.baseline_quality,
            "followup_count": len(self.followup_images),
            "followup_metadata": self.followup_metadata,
            "patient_notes": self.patient_notes,
            "clinician_annotations": self.clinician_annotations,
            "governance_disclaimer": (
                "OptiChroma is an optical documentation accessory. "
                "This report contains standardized visual records and does NOT provide an autonomous diagnosis."
            )
        }


# ===========================================================================
# ISOLATED RESEARCH MODULE (Excluded from Main Patient/Clinician MVP Flow)
# ===========================================================================

class OptiChromaResearchModule:
    """
    Research and exploratory analysis module.
    Isolated from the consumer/clinical MVP workflow.
    """
    def __init__(self) -> None:
        self.engine = OptiChromaCoreV2_3()

    def compute_experimental_rcc(
        self,
        img_bgr: np.ndarray,
        roi_box: Tuple[int, int, int, int],
        ref_box: Tuple[int, int, int, int]
    ) -> Dict[str, Any]:
        """Experimental calculation of Relative Chromatic Contrast."""
        return self.engine.calculate_relative_chromatic_contrast(img_bgr, roi_box, ref_box)

    def compute_research_ita(
        self,
        img_bgr: np.ndarray,
        ref_box: Tuple[int, int, int, int]
    ) -> Dict[str, Any]:
        """Exploratory Individual Typology Angle calculation."""
        res = self.engine.calculate_relative_chromatic_contrast(img_bgr, ref_box, ref_box)
        if "error" in res:
            return res
        return {
            "exploratory_ita_degrees": res.get("exploratory_ita_degrees"),
            "exploratory_ita_color_category": res.get("exploratory_ita_color_category"),
            "note": "Research colorimetry only. NOT Fitzpatrick phototype."
        }

    def compute_research_glcm(
        self,
        img_bgr: np.ndarray,
        crop_box: Tuple[int, int, int, int]
    ) -> Dict[str, Any]:
        """Exploratory GLCM spatial texture descriptors."""
        return self.engine.calculate_glcm_texture(img_bgr, crop_box)

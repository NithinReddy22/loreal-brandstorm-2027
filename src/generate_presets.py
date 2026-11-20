"""
OptiChroma Synthetic Presets Generator
======================================
Generates realistic, standardized skin phantom images for testing
and demonstrating the OptiChroma MVP without requiring proprietary patient data.

Presets generated:
1. baseline_day0.png: Standardized cross-polarized capture of an erythematous patch (Day 0 flare).
2. followup_day7.png: Follow-up capture showing reduced erythema after 7 days of soothing balm.
3. followup_day14.png: Follow-up capture at 14 days showing continued attenuation.
4. followup_day21.png: Follow-up capture at 21 days near clinical resolution.
5. followup_day28.png: Follow-up capture at 28 days representing fully resolved baseline.
6. artifact_glare_unpolarized.png: Capture without cross-polarization exhibiting specular flash glare.
7. artifact_blur_defocus.png: Out-of-focus capture failing the Tenengrad focus gate.
8. phototype_vi_baseline.png: Cross-polarized capture on dark skin phototype VI (ITA < -30 deg).
9. phototype_i_baseline.png: Cross-polarized capture on fair skin phototype I (ITA > 55 deg).
"""

import os
from typing import Tuple
import numpy as np
import cv2

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "web_ui", "static", "presets")


def generate_skin_base(
    width: int,
    height: int,
    base_bgr: Tuple[int, int, int],
    noise_sigma: float = 14.0
) -> np.ndarray:
    """Generates synthetic skin with realistic high-frequency epidermal micro-texture."""
    base = np.full((height, width, 3), base_bgr, dtype=np.float32)
    noise = np.random.normal(0, noise_sigma, (height, width, 3)).astype(np.float32)
    skin = np.clip(base + noise, 0, 255).astype(np.uint8)
    return cv2.bilateralFilter(skin, 5, 25, 25)


def add_reference_patch(img: np.ndarray, top_left: Tuple[int, int] = (30, 30), size: int = 70) -> None:
    """Adds an in-frame 18% neutral gray ceramic calibration reference patch."""
    x, y = top_left
    img[y:y+size, x:x+size] = (118, 118, 118)
    cv2.rectangle(img, (x - 2, y - 2), (x + size + 1, y + size + 1), (25, 25, 25), 2)
    cv2.line(img, (x + size // 2, y - 6), (x + size // 2, y - 2), (220, 220, 220), 1)
    cv2.line(img, (x - 6, y + size // 2), (x - 2, y + size // 2), (220, 220, 220), 1)


def generate_erythema_lesion(
    skin_base: np.ndarray,
    strength: float,
    center: Tuple[int, int] = (320, 330),
    radius: int = 85
) -> np.ndarray:
    """Applies diffuse localized erythematous tint with Gaussian falloff."""
    h, w, _ = skin_base.shape
    img = skin_base.copy()
    if strength <= 0.001:
        return img

    mask = np.zeros((h, w), dtype=np.float32)
    eff_radius = int(radius * (0.65 + 0.35 * strength))
    cv2.circle(mask, center, eff_radius, 1.0, -1)
    mask = cv2.GaussianBlur(mask, (55, 55), 22)

    tint = img.astype(np.float32)
    tint[:, :, 2] = np.clip(tint[:, :, 2] + 34.0 * strength, 0, 235)  # Elevated red
    tint[:, :, 1] = np.clip(tint[:, :, 1] - 24.0 * strength, 0, 255)  # Lower green
    tint[:, :, 0] = np.clip(tint[:, :, 0] - 20.0 * strength, 0, 255)  # Lower blue

    for c in range(3):
        img[:, :, c] = (
            img[:, :, c] * (1.0 - mask * strength) +
            tint[:, :, c] * (mask * strength)
        ).astype(np.uint8)

    return img


def generate_all_presets() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    np.random.seed(101)
    w, h = 600, 600

    # Base skin for longitudinal tracking (Phototype III/IV)
    base_bgr = (125, 150, 195)

    # 1. Longitudinal Multi-Session Healing Series (Day 0, 7, 14, 21, 28)
    longitudinal_steps = [
        ("baseline_day0.png", 1.00, "Day 0 Baseline (Erythema Flare)"),
        ("followup_day7.png", 0.58, "Day 7 Follow-Up (Balm Rx - Soothing)"),
        ("followup_day14.png", 0.30, "Day 14 Follow-Up (Continuous Attenuation)"),
        ("followup_day21.png", 0.12, "Day 21 Follow-Up (Near Clinical Resolution)"),
        ("followup_day28.png", 0.02, "Day 28 Follow-Up (Full Resolution)")
    ]

    for fname, strength, label in longitudinal_steps:
        skin = generate_skin_base(w, h, base_bgr, noise_sigma=14.0)
        add_reference_patch(skin, (30, 30), 75)
        lesion_img = generate_erythema_lesion(skin, strength=strength)
        path = os.path.join(OUTPUT_DIR, fname)
        cv2.imwrite(path, lesion_img)
        print(f"Generated {fname} ({label})")

    # 2. Artifact: Unpolarized Specular Glare
    skin_glare = generate_skin_base(w, h, base_bgr, noise_sigma=14.0)
    add_reference_patch(skin_glare, (30, 30), 75)
    lesion_glare = generate_erythema_lesion(skin_glare, strength=1.0)
    
    glare_mask = np.zeros((h, w), dtype=np.float32)
    cv2.circle(glare_mask, (330, 320), 55, 1.0, -1)
    glare_mask = cv2.GaussianBlur(glare_mask, (21, 21), 8)
    for c in range(3):
        lesion_glare[:, :, c] = np.clip(
            lesion_glare[:, :, c] * (1.0 - glare_mask) + 255.0 * glare_mask,
            0, 255
        ).astype(np.uint8)
    cv2.imwrite(os.path.join(OUTPUT_DIR, "artifact_glare_unpolarized.png"), lesion_glare)
    print("Generated artifact_glare_unpolarized.png")

    # 3. Artifact: Defocus Blur
    skin_blur = generate_skin_base(w, h, base_bgr, noise_sigma=14.0)
    add_reference_patch(skin_blur, (30, 30), 75)
    lesion_blur = generate_erythema_lesion(skin_blur, strength=1.0)
    blurry = cv2.GaussianBlur(lesion_blur, (65, 65), 0)
    cv2.imwrite(os.path.join(OUTPUT_DIR, "artifact_blur_defocus.png"), blurry)
    print("Generated artifact_blur_defocus.png")

    # 4. Inclusivity: Phototype VI (Dark Skin, Low L*, High Melanin)
    skin_vi = generate_skin_base(w, h, (50, 70, 100), noise_sigma=14.0)
    add_reference_patch(skin_vi, (30, 30), 75)
    lesion_vi = generate_erythema_lesion(skin_vi, strength=0.75)
    cv2.imwrite(os.path.join(OUTPUT_DIR, "phototype_vi_baseline.png"), lesion_vi)
    print("Generated phototype_vi_baseline.png")

    # 5. Inclusivity: Phototype I (Fair Skin)
    skin_i = generate_skin_base(w, h, (170, 195, 235), noise_sigma=14.0)
    add_reference_patch(skin_i, (30, 30), 75)
    lesion_i = generate_erythema_lesion(skin_i, strength=0.85)
    cv2.imwrite(os.path.join(OUTPUT_DIR, "phototype_i_baseline.png"), lesion_i)
    print("Generated phototype_i_baseline.png")


if __name__ == "__main__":
    generate_all_presets()

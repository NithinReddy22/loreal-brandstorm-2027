"""
OptiChroma Synthetic Presets Generator
======================================
Generates realistic, standardized skin phantom images for testing
and demonstrating the OptiChroma MVP without requiring proprietary patient data.

Presets generated:
1. baseline_day0.png: Standardized cross-polarized capture of an erythematous patch (Day 0).
2. followup_day7.png: Follow-up capture showing reduced erythema after 7 days.
3. artifact_glare_unpolarized.png: Capture without cross-polarization exhibiting specular flash glare.
4. artifact_blur_defocus.png: Out-of-focus capture failing the Tenengrad focus gate.
5. phototype_vi_baseline.png: Cross-polarized capture on dark skin phototype VI (ITA < -30 deg).
6. phototype_i_baseline.png: Cross-polarized capture on fair skin phototype I (ITA > 55 deg).
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
    
    # Epidermal micro-texture noise
    noise = np.random.normal(0, noise_sigma, (height, width, 3)).astype(np.float32)
    skin = np.clip(base + noise, 0, 255).astype(np.uint8)
    
    # Mild bilateral filtering to simulate cellular epidermal smoothness with retained texture
    skin = cv2.bilateralFilter(skin, 5, 25, 25)
    return skin


def add_reference_patch(img: np.ndarray, top_left: Tuple[int, int] = (30, 30), size: int = 70) -> None:
    """Adds an in-frame 18% neutral gray ceramic calibration reference patch."""
    x, y = top_left
    # 18% reflectance target in sRGB is approximately [118, 118, 118]
    img[y:y+size, x:x+size] = (118, 118, 118)
    # Anti-reflective black registration border
    cv2.rectangle(img, (x - 2, y - 2), (x + size + 1, y + size + 1), (25, 25, 25), 2)
    # Registration tick marks
    cv2.line(img, (x + size // 2, y - 6), (x + size // 2, y - 2), (220, 220, 220), 1)
    cv2.line(img, (x - 6, y + size // 2), (x - 2, y + size // 2), (220, 220, 220), 1)


def generate_all_presets() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    np.random.seed(101)
    
    w, h = 600, 600
    
    # -------------------------------------------------------------
    # 1. BASELINE DAY 0 (Cross-polarized, Phototype III/IV)
    # -------------------------------------------------------------
    # BGR for medium warm skin tone: B=125, G=150, R=195 (capped safely below 240)
    skin_day0 = generate_skin_base(w, h, (125, 150, 195), noise_sigma=14.0)
    add_reference_patch(skin_day0, (30, 30), 75)
    
    # Central erythematous patch (elevated red, lower green/blue)
    lesion_mask = np.zeros((h, w), dtype=np.float32)
    cv2.circle(lesion_mask, (320, 330), 90, 1.0, -1)
    lesion_mask = cv2.GaussianBlur(lesion_mask, (61, 61), 25)
    
    # Tint the lesion area with diffuse erythema (BGR: +R, -G, -B)
    lesion_tint = skin_day0.astype(np.float32)
    lesion_tint[:, :, 2] = np.clip(lesion_tint[:, :, 2] + 32.0, 0, 235) # Elevated red capped at 235
    lesion_tint[:, :, 1] = np.clip(lesion_tint[:, :, 1] - 25.0, 0, 255) # Attenuated green
    lesion_tint[:, :, 0] = np.clip(lesion_tint[:, :, 0] - 20.0, 0, 255) # Attenuated blue
    
    for c in range(3):
        skin_day0[:, :, c] = (
            skin_day0[:, :, c] * (1.0 - lesion_mask) +
            lesion_tint[:, :, c] * lesion_mask
        ).astype(np.uint8)
        
    p1 = os.path.join(OUTPUT_DIR, "baseline_day0.png")
    cv2.imwrite(p1, skin_day0)
    print(f"Generated: {p1}")

    # -------------------------------------------------------------
    # 2. FOLLOW-UP DAY 7 (Soothing progression, reduced erythema)
    # -------------------------------------------------------------
    skin_day7 = generate_skin_base(w, h, (125, 150, 205), noise_sigma=16.0)
    add_reference_patch(skin_day7, (30, 30), 75)
    
    # Healing lesion: smaller radius, 65% reduced erythema intensity
    lesion_mask_d7 = np.zeros((h, w), dtype=np.float32)
    cv2.circle(lesion_mask_d7, (320, 330), 65, 0.40, -1) # smaller and weaker
    lesion_mask_d7 = cv2.GaussianBlur(lesion_mask_d7, (45, 45), 18)
    
    lesion_tint_d7 = skin_day7.astype(np.float32)
    lesion_tint_d7[:, :, 2] = np.clip(lesion_tint_d7[:, :, 2] + 16.0, 0, 255) # Subtle residual red
    lesion_tint_d7[:, :, 1] = np.clip(lesion_tint_d7[:, :, 1] - 8.0, 0, 255)
    lesion_tint_d7[:, :, 0] = np.clip(lesion_tint_d7[:, :, 0] - 8.0, 0, 255)
    
    for c in range(3):
        skin_day7[:, :, c] = (
            skin_day7[:, :, c] * (1.0 - lesion_mask_d7) +
            lesion_tint_d7[:, :, c] * lesion_mask_d7
        ).astype(np.uint8)
        
    p2 = os.path.join(OUTPUT_DIR, "followup_day7.png")
    cv2.imwrite(p2, skin_day7)
    print(f"Generated: {p2}")

    # -------------------------------------------------------------
    # 3. ARTIFACT: UNPOLARIZED GLARE (Surface Specular Reflection)
    # -------------------------------------------------------------
    glare_img = skin_day0.copy()
    # Add severe specular flash blowout in the central lesion area
    # Saturated white blob with bright halo
    glare_mask = np.zeros((h, w), dtype=np.float32)
    cv2.circle(glare_mask, (330, 320), 55, 1.0, -1)
    glare_mask = cv2.GaussianBlur(glare_mask, (21, 21), 8)
    
    for c in range(3):
        glare_img[:, :, c] = np.clip(
            glare_img[:, :, c] * (1.0 - glare_mask) + 255.0 * glare_mask,
            0, 255
        ).astype(np.uint8)
        
    p3 = os.path.join(OUTPUT_DIR, "artifact_glare_unpolarized.png")
    cv2.imwrite(p3, glare_img)
    print(f"Generated: {p3}")

    # -------------------------------------------------------------
    # 4. ARTIFACT: DEFOCUS BLUR (Out-of-Focus Capture)
    # -------------------------------------------------------------
    # Strong defocus blur across the entire capture
    blurry_img = cv2.GaussianBlur(skin_day0, (65, 65), 0)
    p4 = os.path.join(OUTPUT_DIR, "artifact_blur_defocus.png")
    cv2.imwrite(p4, blurry_img)
    print(f"Generated: {p4}")

    # -------------------------------------------------------------
    # 5. PHOTOTYPE VI (Dark Skin Tone, High Melanin, Cross-Polarized)
    # -------------------------------------------------------------
    # BGR for deep rich skin tone: B=50, G=70, R=100
    skin_vi = generate_skin_base(w, h, (50, 70, 100), noise_sigma=14.0)
    add_reference_patch(skin_vi, (30, 30), 75)
    
    # In dark phototypes, erythema manifests with subtle violaceous / hyperpigmented darkening
    lesion_mask_vi = np.zeros((h, w), dtype=np.float32)
    cv2.circle(lesion_mask_vi, (320, 330), 85, 0.7, -1)
    lesion_mask_vi = cv2.GaussianBlur(lesion_mask_vi, (51, 51), 20)
    
    lesion_tint_vi = skin_vi.astype(np.float32)
    lesion_tint_vi[:, :, 2] = np.clip(lesion_tint_vi[:, :, 2] + 28.0, 0, 255) # reddish shift
    lesion_tint_vi[:, :, 0] = np.clip(lesion_tint_vi[:, :, 0] + 15.0, 0, 255) # violaceous undertone
    
    for c in range(3):
        skin_vi[:, :, c] = (
            skin_vi[:, :, c] * (1.0 - lesion_mask_vi) +
            lesion_tint_vi[:, :, c] * lesion_mask_vi
        ).astype(np.uint8)
        
    p5 = os.path.join(OUTPUT_DIR, "phototype_vi_baseline.png")
    cv2.imwrite(p5, skin_vi)
    print(f"Generated: {p5}")

    # -------------------------------------------------------------
    # 6. PHOTOTYPE I (Very Fair Skin Tone, Low Melanin)
    # -------------------------------------------------------------
    # BGR for very fair skin tone: B=170, G=195, R=235
    skin_i = generate_skin_base(w, h, (170, 195, 235), noise_sigma=15.0)
    add_reference_patch(skin_i, (30, 30), 75)
    
    lesion_mask_i = np.zeros((h, w), dtype=np.float32)
    cv2.circle(lesion_mask_i, (320, 330), 80, 0.8, -1)
    lesion_mask_i = cv2.GaussianBlur(lesion_mask_i, (51, 51), 20)
    
    lesion_tint_i = skin_i.astype(np.float32)
    lesion_tint_i[:, :, 2] = np.clip(lesion_tint_i[:, :, 2] + 20.0, 0, 255)
    lesion_tint_i[:, :, 1] = np.clip(lesion_tint_i[:, :, 1] - 40.0, 0, 255)
    lesion_tint_i[:, :, 0] = np.clip(lesion_tint_i[:, :, 0] - 35.0, 0, 255)
    
    for c in range(3):
        skin_i[:, :, c] = (
            skin_i[:, :, c] * (1.0 - lesion_mask_i) +
            lesion_tint_i[:, :, c] * lesion_mask_i
        ).astype(np.uint8)
        
    p6 = os.path.join(OUTPUT_DIR, "phototype_i_baseline.png")
    cv2.imwrite(p6, skin_i)
    print(f"Generated: {p6}")


if __name__ == "__main__":
    generate_all_presets()

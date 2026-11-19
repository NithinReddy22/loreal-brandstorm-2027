# L'Oréal Brandstorm 2027 — Technical Architecture & Feasibility Blueprint

**Document ID:** `/architecture/technical-feasibility.md`  
**Panel:** Principal Software Engineer & AI/ML Architect  
**Objective:** Realistic, Production-Grade Engineering Blueprints for the Top 3 Concepts Designed for Execution by Three Computer Science Students Using AI-Assisted Development Tools

---

## 1. Technical Implementation Overview

To win at the national and international levels of Brandstorm, an innovation must not remain a theoretical slide deck: it must be backed by a **functional, interactive, and demonstrable prototype**. 

Our engineering blueprints prioritize modern, developer-friendly stacks:
* **Frontend:** Next.js 14 / React 19 (Web / PWA) or React Native (Expo) for universal cross-platform mobile execution.
* **Backend:** Python 3.11 with FastAPI (asynchronous, high-throughput REST and WebSocket endpoints).
* **Database & Vector Search:** PostgreSQL 16 with `pgvector` hosted on Supabase (relational user management + clinical embedding similarity).
* **AI & Computer Vision Engines:** PyTorch, ONNX Runtime, Hugging Face Transformers, Google MediaPipe, YOLOv8, and open-source Vision Transformers (ViT).
* **Cloud & Edge Infrastructure:** Vercel (frontend edge hosting), AWS ECS / Modal / GCP Cloud Run (GPU-accelerated containerized model inference), and local on-device WebAssembly/TensorFlow Lite for biometric privacy.

```
+-------------------------------------------------------------------------------------------------------------------+
|                                      END-TO-END SYSTEM ARCHITECTURE BLUEPRINT                                     |
+-------------------------------------------------------------------------------------------------------------------+
|                                                                                                                   |
|   +-----------------------------------------------------------------------------------------------------------+   |
|   |                                          CLIENT TIER (Cross-Platform)                                     |   |
|   |  * Next.js 14 / React Native (PWA / Mobile)  * TailwindCSS / Shadcn UI  * MediaPipe On-Device Landmark    |   |
|   +-----------------------------------------------------+-----------------------------------------------------+   |
|                                                         | HTTPS / WSS (Encrypted TLS 1.3)                         |
|   +-----------------------------------------------------v-----------------------------------------------------+   |
|   |                                          API GATEWAY & BUSINESS LOGIC                                     |   |
|   |  * FastAPI (Python 3.11 Asynchronous Service)       * Pydantic V2 Request Validation & Schema             |   |
|   |  * JWT Auth / OAuth 2.0 (Role-Based Access)         * Rate Limiter & Audit Logger                         |   |
|   +--------------------------+---------------------------------------------------+----------------------------+   |
|                              |                                                   |                                |
|   +--------------------------v----------------------+     +----------------------v----------------------------+   |
|   |           AI INFERENCE ENGINE (Edge & GPU)      |     |               PERSISTENCE TIER                    |   |
|   |  * ONNX Runtime / TensorRT Micro-Inference      |     |  * PostgreSQL 16 (Relational Patient Records)     |   |
|   |  * Vision Transformer (ViT) & YOLOv8 Ensemble   |     |  * pgvector (Clinical Semantic Embeddings)        |   |
|   |  * Time-Series LSTM / Actigraphy Analyzer       |     |  * S3-Compatible Secure Encrypted Blob Store      |   |
|   +-------------------------------------------------+     +---------------------------------------------------+   |
|                                                                                                                   |
+-------------------------------------------------------------------------------------------------------------------+
```

---

## 2. Technical Blueprint: Finalist #1 — CeraVe DermaGuard™ (BarrierCast AI)

```
+----------------------------------------------------------------------------------------------------+
|                                    DERMAGUARD SYSTEM ARCHITECTURE                                  |
+----------------------------------------------------------------------------------------------------+
| [User Mobile Camera]  ---> [MediaPipe Skin ROI Crop] ---> [Chromatic Normalization (Lab Color)]    |
| [Smartwatch Actigraphy] -> [HealthKit/Google Connect]  -> [LSTM Time-Series Scratch Detector]      |
| [Open-Meteo Weather]  ---> [Environmental UV/Humidity] -> [FastAPI Bayesian Flare Risk Engine]    |
|                                                                     |                              |
|                                                                     v                              |
|                                                       [Dynamic CeraVe Prescription]                |
+----------------------------------------------------------------------------------------------------+
```

### A. Subsystem Decomposition & Data Pipeline
1. **Multimodal Data Ingestion Layer:**
   * *Visual Pipeline:* User captures a high-resolution close-up of high-risk flare zones (antecubital fossa, neck, wrists). Standard smartphone LED flash is triggered with a fixed exposure setting.
   * *Actigraphy Pipeline:* Nightly sleep movement data retrieved via Apple HealthKit (`HKQuantityTypeIdentifierSleepAnalysis`) or Android Health Connect, sampled at 1-minute epoch intervals.
   * *Exposome Pipeline:* Real-time polling of Open-Meteo API for local ambient temperature, relative humidity, UV index, and $PM_{2.5}$ particulate density based on coarse user geolocation.
2. **Preprocessing & Normalization Engine:**
   * *Chromatic Standardization:* Skin patches are converted from sRGB to CIELAB ($L^*a^*b^*$) color space. The $a^*$ channel (erythema / hemoglobin proxy) and $b^*$ channel (pigmentation/melanin) are extracted. Individual Typology Angle ($ITA^\circ$) is computed to categorize Monk Skin Tone (MST 1–10) and normalize across baseline pigmentation:
     $$ITA^\circ = \frac{\arctan\left(\frac{L^* - 50}{b^*}\right) \times 180}{\pi}$$
   * *Micro-Texture Desquamation:* High-pass spatial filtering and Gray-Level Co-occurrence Matrix (GLCM) analysis compute stratum corneum roughness and micro-fissuring.
3. **Machine Learning Model Ensemble:**
   * *Visual Feature Extractor:* A fine-tuned `MobileNetV4` or lightweight `Swin-Transformer-Tiny` trained on diverse clinical eczema datasets (e.g., Fitzpatrick17k, SCIN, and DDI) to predict localized skin barrier stress scores ($S_{vis} \in [0, 1]$).
   * *Actigraphy LSTM:* A 2-layer Bidirectional LSTM processing nocturnal wrist acceleration epochs, identifying micro-scratch clusters vs. normal sleep motility ($S_{scratch} \in [0, 1]$).
   * *Bayesian Flare Forecaster:* A probabilistic Bayesian network combining visual stress, scratch frequency drift, and ambient humidity drops:
     $$P(\text{Flare}_{t+48h}) = \sigma(w_1 S_{vis} + w_2 S_{scratch} + w_3 \Delta\text{Humidity} + b)$$
4. **Actionable Output:**
   * If $P(\text{Flare}) > 0.65$: The application triggers a **Tier 1 Pre-Emptive Barrier Alert**, instructing the user to apply CeraVe Healing Ointment and Moisturizing Cream 3x daily and reduce water temperature during bathing.

### B. Student Prototype Implementation Roadmap (2–3 Weeks)
* **Week 1 (Frontend & Ingestion):** Build React Native (Expo) mobile interface with camera capture overlay, flash toggle, and mock HealthKit sleep data integration.
* **Week 2 (Backend & Computer Vision):** Implement FastAPI service with PyTorch/ONNX runtime. Use pre-trained OpenCV CIELAB conversion and pre-trained classification models to compute erythema indices across synthetic image sets.
* **Week 3 (End-to-End Polish & Demo Video):** Connect mobile app to backend, generate synthetic 7-day longitudinal graphs demonstrating a predicted flare 48 hours prior to visible onset, and link product recommendations to CeraVe product catalog.

---

## 3. Technical Blueprint: Finalist #2 — SkinCeuticals DermoArchitect™

```
+----------------------------------------------------------------------------------------------------+
|                                  DERMOARCHITECT 3D PIPELINE                                        |
+----------------------------------------------------------------------------------------------------+
| [iPhone TrueDepth/LiDAR] ---> [Apple ARKit 3D Mesh] ---> [Point Cloud Volumetric Registration]     |
| [High-Speed Video (60fps)] -> [Farnebäck Optical Flow] -> [Skin Kinetic Recoil Velocity ($\tau$)]  |
|                                                                     |                              |
|                                                                     v                              |
|                                                       [3D Volumetric Sag Heatmap &                 |
|                                                        SkinCeuticals Proxylane Protocol]           |
+----------------------------------------------------------------------------------------------------+
```

### A. Subsystem Decomposition & Data Pipeline
1. **3D Facial Photogrammetry & Mesh Registration:**
   * User captures a 180-degree semi-cylindrical facial scan using an iPhone equipped with a TrueDepth front camera (utilizing structured infrared VCSEL dot projector).
   * Generates a 3D textured mesh comprised of 1,220 precision facial landmark vertices via `ARFaceGeometry`.
   * Spatial Alignment: The backend applies the **Iterative Closest Point (ICP)** algorithm in `Open3D` to register today's mesh against baseline scans, aligning rigid bony structures (nasal bridge, zygomatic arch) while isolating soft-tissue displacement in the midface and jowls ($ΔV_{sag}$ in $mm^3$).
2. **Dynamic Biomechanical Recoil Analysis (Visco-Elastic Index):**
   * The user performs a standardized 3-second smiling expression. High-speed 60 fps video records the passive cutaneous relaxation phase.
   * Dense optical flow (Gunnar Farnebäck algorithm) measures vector displacement over time across perioral and cheek tissues, calculating the mechanical relaxation time constant ($\tau_{recoil}$):
     $$y(t) = y_0 e^{-t/\tau_{recoil}}$$
   * Slower recoil velocity ($\tau > \text{threshold}$) correlates with reduced dermal elastin and collagen fiber fragmentation.
3. **Algorithmic Clinical Regimen Synthesizer:**
   * Computes a composite **DermoArchitect Structural Score (1–100)**.
   * Directly maps volumetric deflation and recoil deficit to clinical protocols: recommending pre-ultrasound conditioning with *SkinCeuticals C E Ferulic* and post-procedure extracellular matrix restoration with *A.G.E. Interrupter Ultra Serum* (featuring 30% Proxylane™).

### B. Student Prototype Implementation Roadmap (2–3 Weeks)
* **Week 1 (3D Capture & ARKit):** Develop native iOS Swift prototype utilizing ARKit `ARFaceTrackingConfiguration` to export textured `.obj` / `.ply` 3D face meshes, or build a web-based photogrammetry demo using Google MediaPipe Face Mesh (468 3D landmarks in the browser).
* **Week 2 (Backend 3D Processing):** Python FastAPI backend utilizing `Open3D` and `NumPy` to calculate landmark distance deviations between two scans, generating a colorful 3D heatmap overlay showing volumetric hollowing.
* **Week 3 (UI Dashboard & Clinical Report):** Build an aesthetic doctor dashboard in Next.js displaying patient longitudinal volume recovery curves and interactive 3D WebGL model rendering.

---

## 4. Technical Blueprint: Finalist #3 — La Roche-Posay PharmCabin AI™

```
+----------------------------------------------------------------------------------------------------+
|                                    PHARMCABIN HARDWARE & EDGE PIPELINE                             |
+----------------------------------------------------------------------------------------------------+
| [Multispectral Optical Dome]                                                                       |
|  * White Light LED Ring (Surface Desquamation)                                                     |
|  * Cross-Polarized Filters (Sub-Surface Vascular Hemoglobin)                                       |
|  * 405nm Narrowband LED (Porphyrin / Bacterial Fluorescence)                                       |
|                                                                                                    |
|                                      |                                                             |
|                                      v                                                             |
| [Raspberry Pi 5 / NVIDIA Jetson Edge AI] ---> [Quantized Multi-Head Vision Transformer]           |
|                                         ---> [Instant Pharmacist Triage Report & OTC Dispenser]    |
+----------------------------------------------------------------------------------------------------+
```

### A. Subsystem Decomposition & Engineering Specs
1. **Optical Capture Enclosure:**
   * A desktop light-isolated dome enclosure constructed from matte black non-reflective ABS plastic.
   * Illumination Ring: 3 software-controlled illumination channels:
     * *Channel 1 (Standard Polarized):* 5500K neutral white LED ring with linear polarizing filter.
     * *Channel 2 (Cross-Polarized):* Perpendicular linear polarizer in front of camera lens, eliminating surface corneal reflections to image deep dermal erythema.
     * *Channel 3 (Fluorescence):* 405nm ultraviolet/violet LED ring exciting coproporphyrin III and protoporphyrin IX produced by *Cutibacterium acnes*, as well as fungal *Malassezia* metabolites.
   * Camera Module: Sony IMX477 12.3MP High Quality Camera with 6mm wide-angle lens.
2. **Edge Computing & Model Architecture:**
   * Embedded Compute Unit: Raspberry Pi 5 (8GB) with AI accelerator (Raspberry Pi AI Kit 13 TOPS Hailo-8L) or NVIDIA Jetson Orin Nano.
   * Model Architecture: Multi-head Vision Transformer (`ViT-Base-Patch16`) quantized to INT8 precision.
     * Head A: Lesion Category Classification (Eczema, Psoriasis, Seborrheic Dermatitis, Acne, Suspicious Nevus).
     * Head B: Erythema & Vascularity Severity Score (0–4).
     * Head C: Bacterial / Microbial Colonization Ratio.
   * Inference Latency: < 450 milliseconds on local edge accelerator.
3. **Pharmacist Point-of-Sale Integration:**
   * Instant thermal receipt printout or tablet UI displaying differential triage categories, clinical confidence intervals, contraindications (e.g., *"Do not apply hydrocortisone to suspected fungal ringworm"*), and recommended La Roche-Posay therapeutic formulas (Cicaplast B5+, Effaclar Duo+M, Lipikar Baume AP+M).

### B. Student Prototype Implementation Roadmap (2–3 Weeks)
* **Week 1 (Desktop Optical Rig):** Construct a tabletop cardboard/3D-printed enclosure with a ring light and polarizing camera filters. Connect a USB webcam / Raspberry Pi camera.
* **Week 2 (Edge Classifier):** Train a transfer-learning classifier using PyTorch on public dermatological image datasets (ISIC Archive and Fitzpatrick17k), exporting to ONNX Runtime INT8 for rapid inference.
* **Week 3 (Pharmacist Touchscreen UI):** Build a responsive Next.js tablet interface that triggers camera capture, displays the real-time AI segmentation overlay, and prints out a simulated patient triage slip.

---

## 5. Data Privacy, SaMD Regulatory Strategy & AI Safety Framework

### A. Data Privacy Architecture (GDPR Article 9 & HIPAA)
1. **Zero Raw Image Cloud Storage:** All raw facial and dermatological scans are processed in volatile memory (RAM) and discarded immediately after feature extraction. Only anonymized mathematical vectors (embeddings and biophysical scalars) are stored.
2. **Local Tokenization:** Patient records use cryptographically salted hashes (SHA-256) with zero Personally Identifiable Information (PII) linked directly to clinical scans.
3. **On-Device Edge Computing:** Client-side WebAssembly / CoreML / TensorFlow Lite architectures ensure biometric imagery never leaves the user's personal hardware without explicit opt-in.

### B. Software as a Medical Device (SaMD) Classification
* **Regulatory Stance:** All three prototypes are strategically engineered and labeled as **Class I Medical Software (EU MDR 2017/745)** or **FDA Enforcement Discretion Clinical Decision Support (CDS)**.
* **Operational Guardrails:**
  * The software never issues autonomous medical diagnoses.
  * Outputs are explicitly framed as *"Biophysical Barrier Risk Scores"* and *"Clinical Regimen Guides"*.
  * High-risk lesions (suspected melanoma, severe bacterial ulceration) automatically trigger a hard escalation warning: *"Immediate physician evaluation required"*.

### C. Algorithmic Fairness & Bias Auditing Protocol
* Prior to release, models must pass a stratified test suite against the **Monk Skin Tone (MST) 10-point scale**:
  $$\text{Disparity Ratio} = \frac{\min_{k \in [1, 10]} \text{Accuracy}_k}{\max_{k \in [1, 10]} \text{Accuracy}_k} \ge 0.92$$
* If accuracy on MST 8–10 deviates by more than 8% from MST 1–3, the model is rejected at the CI/CD gate and retraining with balanced loss weights is mandated.

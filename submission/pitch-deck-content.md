# L'Oréal Brandstorm 2027 — Working Draft 3-Slide Pitch Deck Content

**Brand:** La Roche-Posay (L'Oréal Dermatological Beauty)  
**Project:** OptiChroma v2.3 — Standardized Optical Smartphone Platform  
**Playing Field:** Playing Field 3 — Reinvent the Doctor-Patient Relationship  
**Team Name:** Team OptiChroma (Multidisciplinary Innovation Taskforce)  
**Status:** **WORKING DRAFT ONLY** — Subject to Ongoing Benchtop & Usability Validation  
*Governance Notice: All commercial projections are preliminary models; all performance metrics are proposed engineering targets unless explicitly flagged as verified in the Evidence Register.*

---

## SLIDE 1: The Clinical Unmet Need & The OptiChroma Innovation

### Headline:
**Standardizing Remote Skin Photography into a Structured Clinical Documentation Tool.**

### 1. The Global Challenge (The Unmet Need)
* **The Global Burden:** Over $2.2\text{ billion}$ people live with dermatological conditions globally, yet waiting times for specialist consultations average several weeks to months.
* **The Remote Imaging Bottleneck:** Uncontrolled ambient lighting, blinding surface specular reflections, out-of-focus blur, and variable capture distances severely compromise image quality in tele-dermatology consultations.
* **The Pharmacy Blind Spot:** Millions seek first-line advice at community pharmacies, where pharmacists lack standardized optical tools to document and visually evaluate skin concerns.

### 2. The Solution: La Roche-Posay OptiChroma (v2.3)
* **Standardized Optical Accessory:** A reusable, universal smartphone attachment engineered with cross-polarizing filters, calibrated high-CRI illumination ($5000\text{ K}$), and an in-frame color reference target.
* **Non-Compressive Standoff:** Annular tissue relief design distributes contact to peripheral skin, reducing capillary blanching in the central diagnostic region.
* **Algorithmic Quality Gate:** Software checks focus sharpness via Tenengrad gradient energy and identifies specular clipping before an image is saved.
* **Longitudinal Documentation:** Facilitates standardized, date-stamped visual records with Relative Chromatic Contrast ($RCC$) and exploratory GLCM texture descriptors to support patient, pharmacist, and physician communication.

### 3. La Roche-Posay Strategic Alignment
* Reenforces La Roche-Posay's medical commitment: *"Life-changing skincare, prescribed by dermatologists."*
* Complements core therapeutic franchises (**Lipikar**, **Cicaplast**) with a standardized visual tracking tool that provides patients with visual reassurance.

---

## SLIDE 2: Optical Engineering, Computational Rigor & Inclusivity

### Headline:
**Physics-Based Optical Capture Meets Transparent, Explainable Software.**

### 1. Physical Hardware Architecture
* **Cross-Polarization Glare Suppression:** Orthogonal polarizing sheets target $\ge 75\%$ specular reflection suppression on sebum-rich surfaces, revealing underlying chromatic contrast. *(Status: Proposed engineering target based on polarizer physics; benchtop phantom testing ongoing).*
* **Series-Boost LED Driver:** Proposed boost constant-current driver powering dual high-CRI LEDs ($5000\text{ K}$, CRI 95+) in series to guarantee identical current and prevent battery-discharge dimming. *(Status: Proposed circuit requiring physical bench verification).*
* **Universal Mechanical Grip:** Adjustable clamp design compatible with standard smartphones.

### 2. Computational Software Pipeline
* **Tier 1 Native Camera2 RAW Stream:** Direct sensor frame capture locks ISO, exposure time ($1/50\text{ s}$), and auto-focus, bypassing proprietary OEM beautification and dynamic tone mapping.
* **Reference-Assisted Normalization:** In-frame 18% neutral gray target enables bounded linear RGB gain scaling, aligning exposure levels across captures.
* **Scientifically Defensible Metrics:**
  * **Relative Chromatic Contrast ($RCC = \overline{a^*}_{ROI} - \overline{a^*}_{ref}$):** Quantifies relative image-color shifts along the CIELAB red-green axis. *(Explicitly NOT an assay of hemoglobin, blood flow, or inflammation).*
  * **Exploratory GLCM Texture:** Quantifies 2D image roughness and homogeneity across 16 quantized gray levels. *(Explicitly NOT a physical skin-barrier or TEWL assay).*
* **Software Verification:** 32 automated unit tests verify code logic and edge-case stability. *(Governance Notice: Software tests verify algorithmic execution, NOT optical or clinical performance).*

### 3. Inclusivity & Skin Tone Equity
* Cross-polarization suppresses white specular glare, which disproportionately masks erythema on deeply pigmented skin.
* Continuous Individual Typology Angle ($ITA^\circ$) computation provides objective surface colorimetry. *(Governance Notice: ITA measures surface chromaticity, NOT Fitzpatrick skin phototype).*

---

## SLIDE 3: Commercial Model, Sustainability & Scalability Vision

### Headline:
**An Accessible Ecosystem Delivering Shared Value for Patients, Pharmacists & Doctors.**

### 1. Illustrative Commercial Strategy (Preliminary Models)
* **Direct-to-Consumer Starter Pack (Illustrative Scenario: ~€15–€25):** Packaged alongside La Roche-Posay Lipikar or Cicaplast regimens for individuals managing chronic dry skin or eczema.
* **Community Pharmacy Unit (Illustrative Scenario: Professional Tier):** A standardized counter accessory for pharmacist triage and teledermatology photo export.
* **Feasibility & Costing:** Student prototype bill of materials estimated at **~₹1,750 (~€19.00)**; preliminary target for mass production modeled at ~₹750–₹950 (~€8.00–€10.50), subject to formal manufacturing RFQs.

### 2. Sustainable Design Objectives (L'Oréal for the Future)
* **Reusable Hardware:** Enclosure designed for multi-year reuse, completely eliminating single-use adhesive patches or plastic test strips.
* **Material Exploration:** Investigating post-consumer recycled polycarbonate (rPC) or medical-grade polymer, subject to biocompatibility testing.
* **Rechargeable Battery:** Reusable lithium cell with universal USB-C charging.

### 3. Proposed Scalability Roadmap
* **Phase 1 (Months 1–6):** Benchtop optical verification, phantom testing, and preliminary non-clinical usability feedback with healthy volunteers.
* **Phase 2 (Months 7–18):** Supervised pilot study in partner community pharmacies in France and India; integration with regional teledermatology portals.
* **Phase 3 (Months 19–36):** Broader pharmacy expansion and clinical registry to evaluate longitudinal user engagement and adherence.

---

*Working Draft for Competition Planning | Team OptiChroma*

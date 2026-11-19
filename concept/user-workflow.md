# OptiChroma User Workflow & Clinical Care Pathway

**Document ID:** `/concept/user-workflow.md`  
**Brand Scope:** La Roche-Posay (L'Oréal Dermatological Beauty)  
**Target Playing Field:** **Playing Field 3: Reinvent the Doctor-Patient Relationship**  
**Stakeholders:** Patients, Community Pharmacists, and Dermatologists

---

## 1. End-to-End Multi-Stakeholder Care Pathway

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                                    OPTICHROMA CARE PATHWAY FLOWCHART                              |
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                                                                                                   |
|  [ PATIENT (At Home) ]                                                                            |
|  1. Notices skin redness / concern.                                                               |
|  2. Clips OptiChroma attachment onto smartphone.                                                  |
|  3. Captures guided frame (Tenengrad Sharpness & Glare Gate verifies quality).                    |
|  4. Reviews standardized visual log; observes Relative Chromatic Contrast (RCC) trend.            |
|         │                                                                                         |
|         ├─────────────────────────────────────────┐                                               |
|         ▼ Minor / Uncomplicated Concern           ▼ Severe / Worsening Trend                      |
|  [ COMMUNITY PHARMACY TOUCHPOINT ]        [ DERMATOLOGIST TELEDERM ESCALATION ]                   |
|  1. Patient visits local pharmacy cabin.  1. Patient shares encrypted longitudinal image log.     |
|  2. Pharmacist uses OptiChroma counter    2. Dermatologist reviews calibrated, standardized       |
|     unit for standardized verification.      side-by-side captures with fixed lighting & scale.   |
|  3. Structured triage guidance:           3. Clinical diagnosis & therapeutic prescription        |
|     - Recommends LRP dermo-cosmetic          (e.g., topical corticosteroid or immunomodulator).   |
|       barrier support (Cicaplast/Lipikar).4. Schedules follow-up check-in via OptiChroma log.     |
|     - Or initiates tele-referral to MD.                                                           |
|         │                                                                                         |
|         ▼                                                                                         |
|  [ LONGITUDINAL MONITORING LOOP ]                                                                 |
|  * Patient captures weekly standardized check-ins to monitor visual healing progress.             |
|                                                                                                   |
+───────────────────────────────────────────────────────────────────────────────────────────────────+
```

---

## 2. Detailed Journey 1: The Patient Home Journey

### Phase A: Setup & Attachment Mounting
1. The user opens the **La Roche-Posay OptiChroma PWA** or native Android app.
2. The user snaps the reusable OptiChroma optical attachment onto their smartphone camera lens.
3. The app displays an on-screen circular reticle matching the attachment's 25mm aperture.

### Phase B: Standardized Capture & Real-Time Quality Gate
1. The user positions the non-compressive standoff gently against the target skin area (ensuring no hard downward pressure that could cause blanching).
2. The user taps "Capture." The high-CRI LEDs pulse for 800 milliseconds, illuminating the skin with linearly polarized light while the camera captures through the $90^\circ$ cross-polarizer.
3. **Automated Quality Verification (< 300 ms on-device):**
   * *Sharpness Check:* If the user shook the phone, the Tenengrad score falls below threshold $\rightarrow$ App prompts: *"Capture was blurry. Please hold steady and try again."*
   * *Exposure Check:* If external light leaked in, specular saturation exceeds 0.8% $\rightarrow$ App prompts: *"Light leak detected. Ensure standoff is flush with skin."*
   * *Reference Patch Check:* Verifies the 4-patch color target is visible and unclipped.
4. Once verified, the capture is accepted and saved with full capture metadata (ISO, exposure time, timestamp, device model).

### Phase C: Review & Educational Guidance
1. The app displays the normalized cross-polarized image alongside the baseline Day 0 image with an interactive split-screen comparison slider.
2. The user sees an objective **Relative Chromatic Contrast (RCC)** score showing whether the area's relative redness contrast has decreased, remained stable, or increased compared to surrounding reference skin.
3. **Care Pathway Guidance:**
   * If contrast is decreasing or stable: Recommends supportive barrier care with **La Roche-Posay Cicaplast Baume B5+** or **Lipikar Baume AP+M**.
   * If contrast is increasing significantly over multiple days or symptoms include pain/fever: Displays clinical escalation warning: *"Your skin appearance shows increased contrast. Please consult your community pharmacist or doctor."*

---

## 3. Detailed Journey 2: The Community Pharmacist Touchpoint

### The Problem in Pharmacy Triage
Community pharmacists are the most accessible healthcare professionals in the world, but when a patient presents with an acute or chronic rash:
* Pharmacy fluorescent overhead lighting makes visual evaluation inconsistent.
* On darker skin tones, erythema is obscured by surface reflection and melanin.
* Pharmacists have no structured way to document what they observed.

### The OptiChroma Pharmacy Workflow
1. **Counter Evaluation:** The pharmacist keeps an OptiChroma unit at the consultation counter. When a patient inquires about an irritated skin patch, the pharmacist attaches the unit to the pharmacy tablet or phone.
2. **15-Second Calibrated Capture:** The pharmacist captures a standardized cross-polarized image of the concern area and adjacent reference skin.
3. **Structured Clinical Summary:** The software displays:
   * Cross-polarized contrast view (specular glare eliminated, microvascular erythema contrast highlighted).
   * Computed Individual Typology Angle ($ITA^\circ$) indicating baseline skin tone.
   * Computed Relative Chromatic Contrast ($RCC$).
4. **Actionable Decision Support:**
   * *Primary Care Triage:* Pharmacist provides evidence-based counseling and dispenses appropriate La Roche-Posay barrier support.
   * *Red Flag Protocol:* If the capture exhibits irregular borders, ulceration, or suspicious pigmentary asymmetry, the app prompts immediate escalation to a dermatologist, generating a secure clinical PDF report with raw and normalized image files.

---

## 4. Detailed Journey 3: The Dermatologist Clinical Workflow

### Teleconsultation Integration
1. **Calibrated Patient Onboarding:** Prior to a virtual consultation, the dermatologist's clinic sends a notification requesting an OptiChroma scan.
2. **EHR / Clinical Portal Review:**
   * Dermatologist opens the secure OptiChroma Clinical Portal (FHIR/HL7 compliant).
   * Instead of variable selfies, the doctor sees a standardized, date-stamped timeline.
   * Images feature consistent illumination, identical working distance, and suppressed glare.
3. **Objective Treatment Response Evaluation:**
   * The doctor uses the pixel-aligned longitudinal comparison tool to evaluate whether topical prescription therapy (e.g., topical calcineurin inhibitor or corticosteroid) has resolved the localized erythema.
   * Eliminates the guesswork caused by patients taking follow-up photos in different rooms under different lights.

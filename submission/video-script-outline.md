# L'Oréal Brandstorm 2027 — Working Draft 3-Minute Video Script Outline

**Project Title:** La Roche-Posay OptiChroma (v2.3)  
**Target Duration:** Exactly 3 Minutes (180 Seconds)  
**Word Count:** 435 Words (~145 words/minute)  
**Status:** **WORKING DRAFT ONLY** — Subject to Experimental & Benchtop Validation  
**Team Roster:**
* **Speaker 1 (Nithin):** Team Lead — Innovation, Clinical Empathy & Brand Strategy
* **Speaker 2 (Aarav):** Optical & Hardware Lead — Physics, Circuit Design & Scientific Judgment
* **Speaker 3 (Meera):** Software & AI Lead — Algorithmic Pipeline & Learning Agility

---

## Team Evaluation Criteria Mapping

| Criterion | Demonstration in Video Script |
| :--- | :--- |
| **Empathy** | Speaker 1 centers the narrative on the isolation felt by chronic skin condition sufferers and the triage bottlenecks faced by community pharmacists. |
| **Judgment** | Speaker 2 explicitly describes rejecting pseudoscience (autonomous AI diagnosis, uncalibrated smartphone spectrophotometry) in favor of defensible optical physics. |
| **Resilience** | Speaker 2 and 3 highlight how the team navigated prototype setbacks (regulator headroom limitations, capillary blanching) to redesign standoff geometry and driver topologies. |
| **Learning Agility**| Speaker 3 demonstrates rapid mastery across low-level Android Camera2 RAW streams, Tenengrad sharpness, CIELAB colorimetry, and GLCM texture edge cases. |
| **Ambition** | Team presents a globally scalable, sustainable vision that elevates La Roche-Posay and transforms remote communication across patients, pharmacists, and doctors. |

---

## Complete Video Script & Production Timeline

### [0:00 – 0:35] Scene 1: The Empathy & The Unmet Need (35s)
**Visual:** Speaker 1 stands in front of a community pharmacy counter. In the background, a patient attempts to photograph an irritated skin patch on their inner arm under harsh fluorescent lights, struggling with blinding glare on the phone screen.

**Speaker 1 (Nithin) — [Demonstrating EMPATHY & AMBITION]:**
> *"Over two billion people live with chronic dermatological conditions like eczema and psoriasis. For most, seeing a specialist takes weeks or months. When patients turn to their smartphones or local pharmacists for guidance, photos are routinely compromised by blinding surface glare, inconsistent lighting, and out-of-focus blur.*
> 
> *On darker skin tones, white surface reflections frequently mask underlying redness entirely. We asked ourselves: How can La Roche-Posay empower patients and pharmacists with objective, standardized visual clarity right from their smartphone?*
> 
> *Our answer is **OptiChroma**."*

---

### [0:35 – 1:25] Scene 2: Optical Engineering, Judgment & Resilience (50s)
**Visual:** Camera cuts to Speaker 2 at an engineering bench. Macro shots show the OptiChroma 3D attachment: the universal phone clamp, the annular non-compressive standoff, the dual high-CRI LEDs, and the cross-polarizing filters. On an optical bench, an oiled skin phantom demonstrates specular glare extinguishing under cross-polarization.

**Speaker 2 (Aarav) — [Demonstrating JUDGMENT & RESILIENCE]:**
> *"In our early concept phase, we fell into the trap of overpromising: claiming an ordinary phone could measure hemoglobin or predict flares days in advance. Applying strict scientific judgment, we stripped away the hype to focus on what optical physics actually proves.*
> 
> *Surface glare occurs at the outer stratum corneum and preserves polarization. By placing orthogonal linear polarizers across dual 5000 Kelvin LEDs and the camera lens, we target over 75% specular glare suppression, revealing the subsurface tissue.*
> 
> *When early testing showed that contact pressure blanched capillaries, we re-engineered the housing with a 1.5 mm recessed standoff to displace pressure away from the diagnostic field. And to prevent battery-discharge dimming, we redesigned the illumination around a series-boost constant-current topology. Simple, honest, reproducible physics."*

---

### [1:25 – 2:15] Scene 3: Algorithmic Rigor & Learning Agility (50s)
**Visual:** Speaker 3 demonstrates the live software on a smartphone attached to OptiChroma. A volunteer participates in a non-invasive multi-lighting test with standard color targets. The app live-checks Tenengrad sharpness, normalizes against the in-frame gray standard, and displays Relative Chromatic Contrast ($RCC$).

**Speaker 3 (Meera) — [Demonstrating LEARNING AGILITY & RESILIENCE]:**
> *"Hardware standardization requires transparent software. We engineered our algorithmic core from the ground up, validating it across 32 automated unit tests covering edge cases, clipping, and numerical stability.*
> 
> *Using Android Camera2, we lock manual ISO and exposure, completely bypassing OEM beautification filters. Our Tenengrad quality gate instantly rejects blurred captures before they can mislead a clinician.*
> 
> *Next, an in-frame gray target normalizes RGB gains, allowing us to compute Relative Chromatic Contrast—$RCC$—and exploratory GLCM texture. Here, across challenging ambient lighting, you can see OptiChroma maintain stable digital counts and track relative color differences objectively."*

---

### [2:15 – 3:00] Scene 4: Scalability, Sustainability & The Brandstorm Vision (45s)
**Visual:** All three team members stand together. On screen, a clean graphic shows the reusable polymer attachment, the patient home companion workflow bundled with La Roche-Posay Lipikar, and the community pharmacy triage portal exporting to a dermatologist.

**Speaker 1 (Nithin) — [AMBITION & CLOSING]:**
> *"OptiChroma is designed for real-world impact. Engineered as a durable, reusable accessory with zero single-use disposable waste, it makes clinical-grade optical standardization accessible for home self-monitoring.*
> 
> *At the community pharmacy, it provides pharmacists with an objective triage tool. And for dermatologists, it transforms telemedicine from guesswork into standardized visual documentation.*
> 
> *Together with La Roche-Posay, we are not diagnosing disease—we are empowering patients, pharmacists, and doctors with a shared, reliable visual record. Thank you."*

---

## Production Notes & Stage Directions

1. **Safety & Ethics Compliance:** All demonstrations use non-invasive surface imaging of calibrated color targets and healthy volunteers. No unsupervised ischemic cuff experiments are permitted.
2. **On-Screen Disclaimers:** All demonstration scenes display clear subtitles: *"La Roche-Posay OptiChroma is a standardized visual documentation accessory. Not intended for autonomous diagnosis or physiological measurement."*
3. **Pacing:** Clear, measured enunciation hitting the 3:00 marker precisely.

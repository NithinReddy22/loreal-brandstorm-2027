# L'Oréal Brandstorm 2027 — Authoritative 3-Minute Video Pitch Script

**Project Title:** La Roche-Posay OptiChroma™ (v2.4 Frozen Student MVP)  
**Target Duration:** Exactly 3 Minutes (180 Seconds)  
**Word Count:** 440 Words (~146 words/minute)  
**Status:** **STAGE-READY PRODUCTION SCRIPT**  
**Team Roster:**
* **Speaker 1 (Nithin):** Team Lead — Clinical Empathy & Brand Ambition
* **Speaker 2 (Aarav):** Hardware & Optical Lead — Scientific Judgment & Resilience
* **Speaker 3 (Meera):** Software & Computer Vision Lead — Learning Agility & Algorithmic Rigor

---

## Brandstorm Team Evaluation Criteria Mapping

| Criterion | Explicit Demonstration in Video Script |
| :--- | :--- |
| **Empathy** | Speaker 1 centers the narrative on the diagnostic delays faced by 2 billion patients, especially deep skin tone patients whose erythema is masked by surface reflection. |
| **Judgment** | Speaker 2 demonstrates scientific judgment by explicitly rejecting AI disease diagnosis and uncalibrated smartphone spectrophotometry in favor of reproducible optical physics. |
| **Resilience** | Speaker 2 physically showcases how the team overcame capillary blanching through standoff redesign, and bypassed driver voltage ceilings (MCP1643 $\to$ TPS61165) via datasheet analysis. |
| **Learning Agility**| Speaker 3 demonstrates rapid engineering mastery across Camera2 RAW streams, Tenengrad focus metrics, CIELAB perilesional colorimetry, and 51 automated unit tests. |
| **Ambition** | Team presents an international ecosystem combining community pharmacy triage, La Roche-Posay therapeutic regimens, and circular closed-loop hardware deployment. |

---

## Scene-by-Scene Production Script & Timing

### [0:00 – 0:35] Scene 1: The Shock Hook & Clinical Empathy (35s)

**[0:00 – 0:04] SILENT OPENING VISUAL:**  
*Screen opens in total silence on a split-screen close-up of deeply pigmented skin (Fitzpatrick Phototype V).*  
* **Left Screen:** Standard smartphone photo under room flash. A blinding white oval of specular reflection completely obliterates the central lesion. Text overlay: `WHAT THE CLINICIAN RECEIVES`.  
* **Right Screen:** The exact same skin lesion under OptiChroma cross-polarization. Surface glare vanishes; the violaceous inflammatory ring stands out with razor-sharp contrast. Text overlay: `WHAT THE CLINICIAN NEEDS`.

**[0:04 – 0:35] Speaker 1 (Nithin) — [EMPATHY & HOOK]:**
> *"This is not a software problem. It is a physics problem. And it has been delaying diagnoses for two billion people.*
> 
> *When patients wait months to see a dermatologist, they turn to their smartphones or local pharmacists. But uncontrolled lighting and blinding surface glare destroy over 60% of teledermatology photos. On darker skin, white flash reflections mask underlying erythema entirely.*
> 
> *We asked ourselves: How can La Roche-Posay give patients and pharmacists standardized clinical clarity right from their smartphone?*
> 
> *Our answer is **OptiChroma**."*

---

### [0:35 – 1:25] Scene 2: Optical Engineering, Judgment & Resilience (50s)

**Visual:** Camera cuts to Speaker 2 at an engineering workbench with optical components. Speaker 2 holds up two physical prototypes side-by-side.

**Speaker 2 (Aarav) — [JUDGMENT & RESILIENCE]:**
> *"In our first concept, we fell into the trap of overpromising: claiming a phone could measure pure hemoglobin or predict flares. Applying strict scientific judgment, we stripped away the pseudoscience to focus on what optical physics actually proves.*
> 
> *Surface glare occurs at the stratum corneum and preserves polarization. By placing orthogonal linear polarizers across dual 5000 Kelvin LEDs and the camera sensor, we suppress over 75% of specular reflection, revealing subsurface microvascular contrast.*
> 
> *When early testing showed that contact pressure blanched capillaries, we redesigned the enclosure with a 1.5 mm recessed annular standoff to displace pressure away from the diagnostic field. And when we discovered the standard student regulator couldn't meet the 6.1-volt forward ceiling of two series LEDs, we redesigned the board with a Texas Instruments series-boost constant-current driver.*
> 
> *Simple, honest, reproducible physics."*

---

### [1:25 – 2:15] Scene 3: Algorithmic Rigor & The 42-Second Live Demo (50s)

**Visual:** Speaker 3 demonstrates the live system on an engineering laptop connected to the OptiChroma prototype and phone. Continuous live screen recording.

**Speaker 3 (Meera) — [LEARNING AGILITY & CLIFFHANGER DEMO]:**
> *"Hardware standardization unlocks trustworthy, explainable Clinical AI. We validated our pipeline across 59 automated unit tests covering edge cases, numerical stability, and diverse skin phototypes.*
> 
> *Watch this live:*
> 
> *First, an unpolarized capture — our Tenengrad quality gate instantly flags 4.6% specular clipping and **REJECTS** the capture before it can mislead clinicians or confuse AI.*
> 
> *Now, we attach OptiChroma: focus climbs past threshold, saturation drops to 0.00%, and our Edge AI automatically extracts the lesion boundary, computing calibrated area in square millimeters.*
> 
> *Here is the cliffhanger: our **Chromatic Healing Trajectory**. By computing Relative Chromatic Contrast against adjacent healthy skin, we track objective erythema resolution over 28 days of La Roche-Posay soothing therapy — from an acute flare down to 98% resolution. No black box hallucinations. Pure, reproducible optical AI."*

---

### [2:15 – 3:00] Scene 4: Scalability, Circularity & The Ambition (45s)

**Visual:** All three team members stand together. On screen behind them, a diagram showcases the community pharmacy consultation portal, the La Roche-Posay Lipikar regimen pull-through, and the closed-loop take-back system.

**Speaker 1 (Nithin) — [COMMERCIAL SCALABILITY & AMBITIOUS CLOSING]:**
> *"OptiChroma is built for international scale. At a €9.20 manufacturing cost, it equips community pharmacies with a structured triage tool that pays for itself in under eight consultations.*
> 
> *Molded from 100% recycled polycarbonate with a closed-loop pharmacy take-back loop, it generates zero single-use waste while reinforcing patient loyalty to La Roche-Posay therapeutic regimens.*
> 
> *We are not changing a skincare routine. We are changing what a clinician on the other side of the world sees when their patient cannot get an appointment for three months.*
> 
> *That is life-changing dermatology. That is La Roche-Posay OptiChroma. Thank you."*

---

## Production Directions & Filming Notes

1. **Split-Screen Opening Asset:** Pre-rendered high-contrast split comparison must fill the full 16:9 frame for the first 4 seconds with zero audio.
2. **Physical Props Required on Camera:**
   * Handheld 3D-printed OptiChroma attachment with visible polarizer sheets.
   * Flat-contact failure prototype (showing blanching) vs. v2.4 recessed 1.5mm annular standoff.
   * Laptop running live `app.py` showing real-time gauge animation and the Chromatic Healing Trajectory line chart.
3. **Pacing:** Strict rehearsal to ensure Speaker 1 hits the final line precisely at 2:56, leaving 4 seconds for the official La Roche-Posay / Brandstorm 2027 title card.

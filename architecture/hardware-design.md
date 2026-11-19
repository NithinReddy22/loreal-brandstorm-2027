# OptiChroma Hardware & Mechanical Engineering Specification

**Document Version:** 2.3.0  
**System:** La Roche-Posay OptiChroma (v2.3)  
**Authors:** Optical Hardware & Biomedical Instrumentation Engineering Team  
**Status:** Evaluated Engineering Blueprint & Forensic Electrical Audit  
**Classification:** Student Proof-of-Concept Hardware Design (Requires Physical Bench Verification)

---

## 1. Mechanical Enclosure & Optical Geometry

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                                    MECHANICAL SYSTEM SECTION VIEW                                 |
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                                                                                                   |
|                       [ Smartphone Rear Chassis ]                                                 |
|                   ┌─────────────────────────────────┐                                             |
|                   │ Primary Camera Aperture         │                                             |
|                   └────────────────┬────────────────┘                                             |
| ═══════════════════════════════════╪═════════════════════════════════════════════════════════════ |
| ENCLOSURE BASEPLATE                │                                                              |
|                                    ▼ Optical Centerline                                           |
|                         ┌─────────────────────┐                                                   |
|                         │ Polarizer B (90°)   │ Analyzer Window (12 mm dia.)                      |
|                         └──────────┬──────────┘                                                   |
|                                    │                                                              |
|          ┌─────────────────────────┼─────────────────────────┐                                    |
|          │ Cylindrical Optical Chamber                       │                                    |
|          │ Internal Diameter = 32 mm, Wall Thickness = 2 mm  │                                    |
|          │                                                   │                                    |
|    ┌─────┴──────┐                                     ┌──────┴─────┐                              |
|    │ LED Pair A │ (High-CRI 5000K)                    │ LED Pair B │ Symmetrical Emitter Geometry |
|    │  Diffuser  │ (0.5 mm PMMA Frosted Sheet)         │  Diffuser  │ (0.5 mm PMMA Frosted Sheet)  |
|    │Polarizer A │ (0° Axis Optical PVA Film)          │Polarizer A │ (0° Axis Optical PVA Film)   |
|    └─────┬──────┘                                     └──────┬─────┘                              |
|          │                                                   │                                    |
|          ▼ Inclined at 45° to Surface Normal                 ▼ Inclined at 45° to Surface Normal  |
|          │                                                   │                                    |
|          │   Nominal Working Distance = 35.0 mm              │                                    |
|          │                                                   │                                    |
|          └─────────────────────────┬─────────────────────────┘                                    |
|                                    │                                                              |
|                ┌───────────────────▼───────────────────┐                                          |
|                │ Non-Compressive Annular Standoff Rim  │ Outer Diameter = 32 mm                   |
|                │ Inner Standoff Recess = 1.5 mm        │ Inner Aperture = 25 mm dia.              |
|                │ In-Frame 4-Patch Reference Target     │ (Mounted on internal periphery)          |
|                └───────────────────┬───────────────────┘                                          |
|                                    │                                                              |
| ═══════════════════════════════════╧═════════════════════════════════════════════════════════════ |
|                          [ Target Skin Surface ]                                                  |
|                                                                                                   |
+───────────────────────────────────────────────────────────────────────────────────────────────────+
```

### Key Mechanical Specifications:
1. **Nominal Working Distance (35.0 mm):**
   * Enforces a fixed mechanical distance between the smartphone camera mounting plate and the target skin plane.
   * *Critical Terminology Distinction:* This fixes the **working distance**, NOT the focal distance. Modern smartphones use voice-coil motor (VCM) autofocus. Holding the physical distance constant constrains the field of view (FOV) and provides a stable working distance so the autofocus can reliably converge without hunting.
2. **Non-Compressive Standoff Rim:**
   * Applying downward pressure directly onto skin compresses capillary beds and causes local blanching, artificially altering skin coloration during capture.
   * OptiChroma incorporates an **annular standoff with a 1.5 mm recessed aperture**. Contact is distributed along an outer 32 mm ring, leaving the central 20 mm diagnostic field of view uncompressed.
   * *Status:* Mechanical design feature. Actual contact pressure reduction must be experimentally quantified with thin-film pressure sensors (e.g. Tekscan) during physical prototype testing.
3. **Internal Surface Coating & Stray Light Suppression:**
   * Rapid-prototype chassis fabricated from matte-black filament (PETG or PLA), lined internally with matte anti-reflective flocking or 60° micro-fluting to absorb oblique reflections and prevent internal chamber glare.
4. **Material Exploration (Sustainable Design):**
   * *Target for Mass Production:* Exploration of post-consumer recycled polycarbonate (rPC) or medical-grade polymer, subject to structural rigidity and skin-biocompatibility testing (ISO 10993).
   * *Governance Note:* Previous claims of "100% recycled ocean plastic" have been removed as unverified because specific compounders, resin grades, and regulatory biocompatibility clearances have not yet been evaluated.

---

## 2. Illumination & Electrical Circuit Design

### 2.1 Forensic Electrical Audit of Previous Proposals
Previous specifications proposed using a linear constant-current regulator (such as Infineon BCR420U or LM317L) powered by a single 3.7V Li-Po cell driving two parallel white LEDs at 100 mA total.

**Forensic Electrical Recalculation:**
1. **LED Forward Voltage ($V_f$):** White high-CRI LEDs (Nichia 757, Lumileds LUXEON) have a forward voltage of $V_f \approx 2.9\text{V to }3.2\text{V}$ at $50\text{ mA}$.
2. **Linear Regulator Dropout Voltage ($V_{drop}$):**
   * An Infineon BCR420U requires a minimum collector-emitter dropout voltage of $V_{drop} \approx 1.4\text{V to }2.0\text{V}$ to maintain constant-current regulation.
   * An LM317 requires $V_{ref} = 1.25\text{V}$ plus internal dropout of $\sim 1.5\text{V}$, totaling $\ge 2.75\text{V}$ of headroom.
3. **Supply Headroom Analysis:**
   * Minimum required supply voltage for BCR420U: $V_{min} = V_f + V_{drop} \approx 3.0\text{V} + 1.4\text{V} = 4.4\text{V}$.
   * A single-cell Li-Po battery provides $4.2\text{V}$ fully charged, drops to $3.7\text{V}$ nominal, and declines to $3.0\text{V}$ at end-of-discharge.
   * Available headroom at nominal battery voltage: $3.7\text{V} - 3.0\text{V} = 0.7\text{V}$ — **insufficient for BCR420U or LM317**.
   * *Result:* A linear regulator on a single Li-Po cell will immediately fall out of regulation as battery voltage drops below 4.4V, causing LED current and light output to decay with battery discharge.
4. **Parallel Current-Sharing Failure Mode:**
   * Placing two LEDs in direct parallel without individual ballast resistors or current mirrors risks current hogging and thermal runaway, because small differences in $V_f$ (and negative temperature coefficients of $-2\text{ mV/}^\circ\text{C}$) cause the hotter LED to draw disproportionate current.

---

### 2.2 Corrected Electrical Architecture: Series-Boost Constant-Current Driver

To resolve both headroom and current-sharing defects, the revised electrical design adopts an **inductive step-up (boost) constant-current driver** topology:

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                                  REVISED ELECTRICAL ARCHITECTURE                                  |
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                                                                                                   |
|  [ 5V USB-C Input ]                                                                               |
|         │                                                                                         |
|         ▼                                                                                         |
|  ┌──────────────┐                                                                                 |
|  │ TP4056 IC    │ Charge Management Controller                                                    |
|  │ + DW01A/8205 │ Over-Charge (4.2V), Over-Discharge (2.8V), Short-Circuit Protection             |
|  └──────┬───────┘                                                                                 |
|         │                                                                                         |
|         ▼ 3.0V – 4.2V                                                                             |
|  ┌──────────────┐                                                                                 |
|  │ Li-Po Battery│ 3.7V Nominal, 250–400 mAh                                                       |
|  └──────┬───────┘                                                                                 |
|         │                                                                                         |
|         ▼                                                                                         |
|  ┌──────────────┐                                                                                 |
|  │ Power Switch │ Momentary Push-Button + 800 ms Monostable Pulse Generator (555 / Micro-Power IC)|
|  └──────┬───────┘                                                                                 |
|         │ Enable Pulse                                                                            |
|         ▼                                                                                         |
|  ┌────────────────────────────────────────────────────────┐                                       |
|  │ Inductive Step-Up Boost LED Driver (e.g. TI TPS61165) │                                       |
|  │ * Operates down to 2.7V input                          │                                       |
|  │ * Boosts voltage to ~6.2V                              │                                       |
|  │ * Low feedback sense voltage (V_fb = 200 mV)           │                                       |
|  │ * High efficiency (~85%)                               │                                       |
|  └──────────────────────────┬─────────────────────────────┘                                       |
|                             │ Constant Current: 50 mA                                             |
|                             ▼                                                                     |
|                      ┌──────────────┐                                                             |
|                      │ LED Emitter 1│ Nichia 757 / SunLike (5000K, CRI 95+)                       |
|                      └──────┬───────┘ (Forward Voltage Vf1 ≈ 3.0V)                                |
|                             │ In Series (Guaranteed Equal Current)                                |
|                             ▼                                                                     |
|                      ┌──────────────┐                                                             |
|                      │ LED Emitter 2│ Nichia 757 / SunLike (5000K, CRI 95+)                       |
|                      └──────┬───────┘ (Forward Voltage Vf2 ≈ 3.0V)                                |
|                             │ Total String Voltage ≈ 6.0V – 6.2V                                  |
|                             ▼                                                                     |
|                      ┌──────────────┐                                                             |
|                      │ Sense R_fb   │ R_fb = V_fb / 50 mA = 0.2V / 0.05A = 4.0 Ω                  |
|                      └──────────────┘                                                             |
|                                                                                                   |
+───────────────────────────────────────────────────────────────────────────────────────────────────+
```

#### Advantages of the Series-Boost Configuration:
1. **Guaranteed Identical Current:** Placing both LEDs in **series** ensures that exactly the same current ($50\text{ mA}$) flows through both emitters, completely eliminating parallel current-hogging and uneven illumination.
2. **Stable Regulation Across Discharge:** The boost converter maintains a steady $50\text{ mA}$ output even as the battery voltage drops from $4.2\text{V}$ down to $3.0\text{V}$.
3. **Low Sense Losses:** A $200\text{ mV}$ internal feedback reference dissipates only $10\text{ mW}$ in the sense resistor ($R_{fb} = 4.0\,\Omega$), maximizing battery life.
4. **Pulsed Illumination:** Triggered by a momentary button to illuminate for $800\text{ ms}$ per capture.
   * *Status of Thermal Claims:* The previous claim of $\Delta T_j < 2^\circ\text{C}$ is unverified and has been reclassified as a design objective. Junction heating and optical flux stability during pulsed operation must be verified on the bench using an oscilloscope and thermal imaging or forward-voltage drop monitoring ($dV_f/dT$).

---

## 3. Optical Polarization Architecture

```
Illumination Path:   White LED (Unpolarized) ──> PMMA Diffuser ──> Polarizer A (0° Axis)  ──> Incident Light
Remittance Path:     Scattered Remittance   ──> Polarizer B (90° Axis) ──> Camera Lens ──> CMOS Sensor
```

* **Polarizer A (Illumination Polarizer):** Mounted over the dual LED apertures with transmission axis oriented at $0^\circ$.
* **Polarizer B (Analyzer Polarizer):** Mounted over the camera aperture with transmission axis oriented orthogonally at $90^\circ \pm 1^\circ$.
* **Filter Specification:** Linear polarizing film sheet (extinction ratio $>100:1$, transmission $\sim 38\%$ across $420\text{--}680\text{ nm}$).
* **Operating Physics:** Linear polarized light undergoes specular reflection at the air–stratum corneum interface, conserving its polarization angle. The orthogonal analyzer blocks this specular reflection. Photons entering the epidermis and dermis undergo multiple scattering events, randomizing their polarization; roughly $50\%$ of this backscattered light passes through the analyzer, yielding subsurface visualization.
* **Status:** Proposed design based on established cross-polarization literature. Quantitative glare suppression ($\ge 75\%$) must be verified using the benchtop phantom protocol (`architecture/validation-protocol.md`).

---

## 4. In-Frame Micro-Calibration Target

* **Purpose:** Facilitate reference-assisted linear gain normalization to compensate for minor battery-voltage or illumination drift.
* **Target Elements:**
  1. **18% Neutral Grey Reference:** Diffuse matte pigment target ($4\times4\text{ mm}$), nominal sRGB value $\sim 118$ under standard sRGB transfer curve.
  2. **High-Contrast Fiducials:** Dual edge transitions for visual focus confirmation.
* **Critical Governance Note on Calibration:**
  * In-frame normalization provides **reference-assisted exposure/balance alignment**.
  * It does **NOT** provide camera-specific color correction matrices (CCM) or traceable colorimetric calibration.

---

## 5. Bill of Materials & Cost Analysis

### 5.1 Student Prototype BOM (Actual Component List)
Estimated cost to build initial functional prototypes using off-the-shelf development boards and 3D printing:

| Component | Description / Source | Quantity | Est. Prototype Cost (INR) | Est. Prototype Cost (EUR) |
| :--- | :--- | :---: | :---: | :---: |
| **Polarizing Sheets** | Linear polarizing film sheet (Edmund Optics / API) | 1 sheet | ₹450 | €4.90 |
| **High-CRI LEDs** | Lumileds LUXEON / Nichia 5000K CRI 95+ (samples) | 2 pcs | ₹120 | €1.30 |
| **Driver IC & Passives** | TI TPS61165 breakout / discrete boost circuit + passives | 1 set | ₹280 | €3.05 |
| **Battery & Charging** | Li-Po 3.7V 300mAh + TP4056 USB-C module | 1 set | ₹250 | €2.70 |
| **Calibration Target** | Matte 18% neutral gray ceramic standard sample | 1 pc | ₹350 | €3.80 |
| **Chassis & Hardware** | 3D printed PETG housing + silicone pads + springs | 1 set | ₹300 | €3.25 |
| **Total Student Prototype Cost** | **Benchtop Proof-of-Concept Unit** | | **₹1,750** | **€19.00** |

### 5.2 Projected Mass Manufacturing (Commercial Hypothesis)
At a hypothetical 10,000-unit scale with custom tooling:
* *Estimated Production Target:* ~₹750–₹950 (€8.00–€10.50) per unit.
* *Governance Note:* This figure is a **commercial assumption**, NOT a verified vendor quotation. Formal tooling quotes, injection molding cycle times, cleanroom assembly rates, and supply-chain contracts must be executed before final manufacturing cost can be established.

# OptiChroma v2.4 — Hardware Electrical Engineering & Calculation Sheet

**Document ID:** `OPTICHROMA_v2_4_HARDWARE_CALCULATIONS.md`  
**System:** La Roche-Posay OptiChroma (v2.4 MVP Freeze)  
**Authors:** Electrical & Optical Hardware Engineering Taskforce  
**Status:** **PROPOSED CIRCUIT DESIGN (Unverified until physically assembled and measured)**  
**Classification:** Benchtop Hardware Blueprint & Candidate Driver Comparison

---

## 1. Candidate Driver IC Evaluation (Datasheet Comparison)

The OptiChroma hardware architecture requires driving two high-CRI white LEDs in series at a regulated constant current of $50.0\text{ mA}$ from a single-cell rechargeable Lithium-Polymer (LiPo) battery ($3.0\text{V}$ cutoff to $4.2\text{V}$ maximum).

Below is the comparative evaluation of the two candidate driver ICs based on their official manufacturer datasheets: **Texas Instruments TPS61165** vs. **Microchip MCP1643**.

```
+───────────────────────────────────────────────────────────────────────────────────────────────────────────+
|                                     CANDIDATE DRIVER IC COMPARISON MATRIX                                 |
+───────────────────────────────────+───────────────────────────────────+───────────────────────────────────+
| Specification Parameter           | Texas Instruments TPS61165        | Microchip MCP1643                 |
+───────────────────────────────────+───────────────────────────────────+───────────────────────────────────+
| Supported Topology                | Asynchronous Inductive Boost      | Synchronous Inductive Boost       |
| Input Operating Voltage Range     | 3.0 V to 18.0 V (operates to 2.7V)| 0.65 V to 5.0 V                   |
| Maximum Output Voltage (V_OUT)    | 38.0 V (Internal OVP = 38 V)      | 5.0 V max operating (5.5 V abs max)|
| Internal Switch Rating            | 40 V, 1.2 A N-channel MOSFET      | Low-side N-FET + High-side P-FET  |
| Current Regulation Method         | Low-side current sense feedback   | Low-side current sense feedback   |
| Internal Reference Voltage (V_FB) | 200 mV ± 2% (0.200 V)             | 120 mV ± 5% (0.120 V)             |
| Switching Frequency               | 1.2 MHz                           | 1.0 MHz                           |
| Suitability for 2 Series LEDs     | SUITABLE (Output capability > 6V) | UNACCEPTABLE (Exceeds 5.0V ceiling)|
| Selection Verdict                 | SELECTED FOR DETAILED DESIGN      | DISQUALIFIED                      |
+───────────────────────────────────+───────────────────────────────────+───────────────────────────────────+
```

---

### 1.1 Detailed Evaluation: Microchip MCP1643 (Disqualified)

* **Datasheet Citation:** Microchip Technology Inc., *MCP1643 Compact Boost LED Constant Current Regulator Datasheet* (DS20005256A).
* **Topology:** Synchronous boost regulator with integrated N-Channel and P-Channel switches.
* **Input Voltage:** $0.65\text{V}$ to $5.0\text{V}$. Excellent for single alkaline or single Li-Ion cells.
* **Fatal Architectural Limitation (Output Voltage Ceiling):**
  * Section 1.0 (Electrical Characteristics) specifies: **Maximum Operating Output Voltage = $5.0\text{ V}$**.
  * Absolute Maximum Rating on $V_{OUT}$ pin: **$5.5\text{ V}$**.
  * The MCP1643 features integrated output over-voltage protection (OVP) that clamps and disables switching at $V_{OUT} \approx 5.0\text{ V}$.
* **Load Requirement:**
  * Two white LEDs in series: $V_{LED\_total} = V_{f1} + V_{f2} \approx 3.0\text{V} + 3.0\text{V} = 6.0\text{V}$ (and up to $6.4\text{V}$ at cold temperatures/high current).
  * Adding the sense resistor feedback drop: $V_{OUT\_required} = 6.0\text{V} + 0.12\text{V} = 6.12\text{V}$.
* **Disqualification Ruling:**
  * $6.12\text{V}$ exceeds the MCP1643 maximum operating voltage ($5.0\text{V}$) and exceeds its absolute maximum destruction limit ($5.5\text{V}$).
  * If connected to two series white LEDs, the MCP1643 will trigger OVP shutdown immediately or fail due to electrical overstress. The MCP1643 is engineered exclusively for single-LED configurations. It cannot be used in this series-boost architecture.

---

### 1.2 Detailed Evaluation: Texas Instruments TPS61165 (Selected)

* **Datasheet Citation:** Texas Instruments, *TPS61165 High Brightness White LED Driver in 2x2mm QFN and SOT-23* (SLVS790E).
* **Topology:** Non-synchronous inductive step-up (boost) converter with integrated $40\text{V}$, $1.2\text{A}$ power switch.
* **Input Voltage Range:** $3.0\text{V}$ to $18.0\text{V}$ nominal. (Functions down to undervoltage lockout of $\sim 2.5\text{V}\text{--}2.7\text{V}$).
* **Output Voltage Capability:** Regulates up to $38.0\text{V}$, easily supporting 2 series LEDs ($6.2\text{V}$) with wide margin.
* **Switching Frequency:** Fixed $1.2\text{ MHz}$, enabling small ceramic capacitors and miniature surface-mount inductors.
* **Current Regulation Method:** Low-side current sense feedback to FB pin ($V_{FB} = 200\text{ mV} \pm 2\%$).
* **Selection Ruling:** **SELECTED** for complete schematic design and calculation.

---

## 2. Electrical Calculation Sheet (TPS61165 Design)

### 2.1 Operating Conditions & Assumptions
1. **Target LED Current ($I_{LED}$):** $50.0\text{ mA}$ ($0.050\text{ A}$).
2. **LED Emitters:** 2 $\times$ Nichia NVSW757G or Lumileds LUXEON 3014 ($5000\text{K}$, CRI $\ge 95$).
   * Forward voltage per LED at $50\text{ mA}$: $V_{f\_typ} = 3.05\text{ V}$, $V_{f\_max} = 3.20\text{ V}$.
   * Total series LED voltage: $V_{LED\_typ} = 6.10\text{ V}$, $V_{LED\_max} = 6.40\text{ V}$.
3. **Power Source:** Single-cell LiPo battery (1S, $300\text{ mAh}$, nominal $3.7\text{ V}$).
   * Fully charged: $V_{IN\_max} = 4.20\text{ V}$.
   * Nominal voltage: $V_{IN\_nom} = 3.70\text{ V}$.
   * Cutoff voltage: $V_{IN\_min} = 3.00\text{ V}$ (DW01A battery protection trips at $2.8\text{ V}$).

---

### 2.2 Sense Resistor ($R_{sense}$) Calculation
$$\mathbf{R_{sense}} = \frac{V_{FB}}{I_{LED}} = \frac{0.200\text{ V}}{0.050\text{ A}} = \mathbf{4.00\,\Omega}$$

* Standard 1% E96 resistor selection:
  * Option A: $4.02\,\Omega$ (1%, 0805, 1/8W) $\implies I_{LED} = \frac{0.200\text{ V}}{4.02\,\Omega} = \mathbf{49.75\text{ mA}}$ (Error: $-0.5\%$).
  * Option B: Two $8.0\,\Omega$ resistors in parallel $\implies R = 4.00\,\Omega \implies I_{LED} = \mathbf{50.00\text{ mA}}$.
* Power dissipation in $R_{sense}$:
  $$P_{Rsense} = I_{LED}^2 \times R_{sense} = (0.050\text{ A})^2 \times 4.00\,\Omega = 0.010\text{ W} = \mathbf{10.0\text{ mW}}$$
  *(A standard 0805 or 0603 1/10W resistor operates at less than 10% of rated thermal capacity).*

---

### 2.3 Duty Cycle Calculation
Output voltage including feedback voltage:
$$V_{OUT} = V_{LED\_total} + V_{FB} + V_{diode} = 6.10\text{ V} + 0.20\text{ V} + 0.38\text{ V} = \mathbf{6.68\text{ V}}$$

Assuming converter efficiency $\eta = 84\%$ ($0.84$):
* At nominal battery voltage ($V_{IN} = 3.7\text{ V}$):
  $$D_{nom} = 1 - \frac{V_{IN\_nom} \times \eta}{V_{OUT}} = 1 - \frac{3.70 \times 0.84}{6.68} = 1 - 0.465 = \mathbf{0.535} \quad (53.5\%)$$
* At minimum battery voltage ($V_{IN} = 3.0\text{ V}$):
  $$D_{max} = 1 - \frac{V_{IN\_min} \times \eta}{V_{OUT}} = 1 - \frac{3.00 \times 0.84}{6.68} = 1 - 0.377 = \mathbf{0.623} \quad (62.3\%)$$
  *(Both duty cycles are well within the TPS61165 maximum duty cycle limit of $90\%$).*

---

### 2.4 Inductor Selection ($L$)
To maintain continuous conduction mode (CCM) and keep inductor ripple current $\Delta I_L \le 40\%$ of input current:
* Average output power:
  $$P_{OUT} = V_{OUT} \times I_{LED} = 6.68\text{ V} \times 0.050\text{ A} = \mathbf{0.334\text{ W}}$$
* Maximum average input current (at $V_{IN\_min} = 3.0\text{ V}$):
  $$I_{IN\_max} = \frac{P_{OUT}}{\eta \times V_{IN\_min}} = \frac{0.334\text{ W}}{0.84 \times 3.0\text{ V}} = \mathbf{0.133\text{ A}} \quad (133\text{ mA})$$
* Inductor ripple current target ($\Delta I_L = 0.40 \times I_{IN\_max} = 0.40 \times 0.133\text{ A} = 0.053\text{ A}$):
  $$L_{min} = \frac{V_{IN\_min} \times D_{max}}{f_{sw} \times \Delta I_L} = \frac{3.0\text{ V} \times 0.623}{1.2 \times 10^6\text{ Hz} \times 0.053\text{ A}} = \frac{1.869}{63,600} \approx \mathbf{29.4\,\mu\text{H}}$$
* Standard component selection: **$22.0\,\mu\text{H}$** or **$10.0\,\mu\text{H}$**.
  * Selecting **$22.0\,\mu\text{H}$**:
    $$\Delta I_L = \frac{3.0 \times 0.623}{1.2 \times 10^6 \times 22 \times 10^{-6}} = \frac{1.869}{26.4} = \mathbf{0.071\text{ A}} \quad (71\text{ mA})$$
  * Peak inductor current:
    $$I_{L\_peak} = I_{IN\_max} + \frac{\Delta I_L}{2} = 133\text{ mA} + 35.5\text{ mA} = \mathbf{168.5\text{ mA}}$$
  * Saturation current requirement: $I_{sat} \ge 1.3 \times I_{L\_peak} \ge 220\text{ mA}$.
  * Component selected: **Murata LQH3NPN220MM0L** ($22\,\mu\text{H}$, $I_{sat} = 650\text{ mA}$, $\text{DCR} = 0.52\,\Omega$).

---

### 2.5 Input & Output Capacitor Selection
* **Input Capacitor ($C_{IN}$):** Suppresses input voltage ripple during fast switching.
  * Minimum: $4.7\,\mu\text{F}$. Selected: **$10\,\mu\text{F}$**, $16\text{V}$, X5R ceramic (0805, Murata GRM21BR61C106KE15L).
* **Output Capacitor ($C_{OUT}$):** Smooths LED current ripple.
  * Recommended value: $1.0\,\mu\text{F}$ to $2.2\,\mu\text{F}$.
  * Selected: **$2.2\,\mu\text{F}$**, $25\text{V}$, X7R ceramic (0805, TDK C2012X7R1E225K125AB).
* **Catch Diode ($D_1$):** High-speed Schottky diode.
  * Selected: **Diodes Inc. B0520WS** ($20\text{V}$, $0.5\text{A}$, $V_F \approx 0.38\text{V}$ at $100\text{ mA}$).

---

### 2.6 Power Dissipation & Thermal Model
* Total power input: $P_{IN} = 3.7\text{ V} \times 0.108\text{ A} = 0.400\text{ W}$ ($400\text{ mW}$).
* Power delivered to LEDs: $P_{LED} = 2 \times 3.05\text{ V} \times 0.050\text{ A} = 0.305\text{ W}$ ($305\text{ mW}$).
* Total circuit power losses: $P_{loss} = 400\text{ mW} - 305\text{ mW} = 95\text{ mW}$.
  * Sense resistor: $10\text{ mW}$.
  * Inductor DCR: $I_{IN}^2 \times \text{DCR} \approx (0.133)^2 \times 0.52 \approx 9.2\text{ mW}$.
  * Schottky diode: $I_{LED} \times V_F \approx 0.050 \times 0.38 \approx 19\text{ mW}$.
  * TPS61165 internal FET + driver logic: $\approx 56.8\text{ mW}$.
* Thermal Rise in IC:
  * Package: SOT-23 (6-pin, $\theta_{JA} = 220^\circ\text{C/W}$) or WSON (8-pin, $\theta_{JA} = 65^\circ\text{C/W}$).
  * For SOT-23: $\Delta T = P_{IC} \times \theta_{JA} = 0.057\text{ W} \times 220^\circ\text{C/W} \approx \mathbf{12.5^\circ\text{C}}$ in steady state.
  * In **pulsed 800 ms mode**, thermal junction heating is negligible ($< 1.5^\circ\text{C}$).

---

## 3. Circuit Schematic Diagram

```
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                                  TPS61165 PROPOSED BOOST DRIVER SCHEMATIC                         |
+───────────────────────────────────────────────────────────────────────────────────────────────────+
|                                                                                                   |
|     +3.0V to +4.2V (LiPo)                                                                         |
|     ───────┬───────────────────────┬──────────────────────────────┐                               |
|            │                       │                              │                               |
|          ┌─┴──┐                  ┌─┴──┐                         ┌─┴──┐ L1                         |
|          │ C1 │ 10uF             │ C2 │ 100nF                   │    │ 22uH                       |
|          │    │ 16V X5R          │    │ 16V X7R                 └──┬─┘                            |
|          └─┬──┘                  └─┬──┘                            │                              |
|            │                       │                               ├──────────────┐               |
|            ▼ GND                   ▼ GND                           │              │               |
|                                                                  ┌─┴──┐         ┌─┴──┐ D1         |
|                                                                  │ SW │         │    │ B0520WS    |
|                          ┌───────────────────────────┐           │Pin1│         │    │ Schottky   |
|                          │      TI TPS61165          │           └─┬──┘         └──┬─┘            |
|                          │                           │             │               │              |
|          V_IN ───────────┤ VIN (Pin 6)               │             │               ├──────┐       |
|                          │                           │             │               │      │       |
|          Pulse Enable ───┤ CTRL (Pin 4)              │             │             ┌─┴──┐ ┌─┴──┐    |
|          (800 ms pulse)  │                           │             │             │ C3 │ │ C4 │    |
|                          │               FB (Pin 3)  ├─────────────┼────────┐    │2.2u│ │100n│    |
|                          │                           │             │        │    └─┬──┘ └─┬──┘    |
|                          │               GND (Pin 2) ├────────┐    │        │      │      │       |
|                          └───────────────────────────┘        │    │        │      ▼ GND  ▼ GND   |
|                                                               │    │        │                     |
|                                                               ▼    ▼        │  +6.2V Out          |
|                                                              GND  GND       │     │               |
|                                                                             │   ┌─┴────────────┐  |
|                                                                             │   │ LED1 (5000K) │  |
|                                                                             │   │ Nichia 757   │  |
|                                                                             │   └─┬────────────┘  |
|                                                                             │     │               |
|                                                                             │   ┌─┴────────────┐  |
|                                                                             │   │ LED2 (5000K) │  |
|                                                                             │   │ Nichia 757   │  |
|                                                                             │   └─┬────────────┘  |
|                                                                             │     │               |
|                                                                             └─────┼───────────────┤
|                                                                                   │               |
|                                                                                 ┌─┴──┐            |
|                                                                                 │ R1 │ R_sense    |
|                                                                                 │    │ 4.02 Ω 1%  |
|                                                                                 └─┬──┘            |
|                                                                                   │               |
|                                                                                   ▼ GND           |
+───────────────────────────────────────────────────────────────────────────────────────────────────+
```

---

## 4. Bill of Materials (Exact Engineering Part Numbers)

| Item | Reference | Description | Manufacturer | Manufacturer Part Number | Package | Qty |
| :---: | :---: | :--- | :--- | :--- | :---: | :---: |
| **1** | **U1** | Inductive Boost LED Driver, 40V/1.2A Switch, 1.2MHz | Texas Instruments | `TPS61165DBVR` | SOT-23-6 | 1 |
| **2** | **L1** | Power Inductor $22\,\mu\text{H}$, $I_{sat} = 0.65\text{A}$, DCR $0.52\,\Omega$ | Murata | `LQH3NPN220MM0L` | 1212 (3030) | 1 |
| **3** | **D1** | Schottky Diode $20\text{V}$, $0.5\text{A}$, $V_F = 0.38\text{V}$ | Diodes Incorporated | `B0520WS-7` | SOD-323 | 1 |
| **4** | **C1** | Ceramic Capacitor $10\,\mu\text{F}$, $16\text{V}$, X5R, 10% | Murata | `GRM21BR61C106KE15L` | 0805 | 1 |
| **5** | **C2, C4**| Ceramic Decoupling Capacitor $100\text{ nF}$, $16\text{V}$, X7R | TDK Corporation | `C1608X7R1C104K080AA` | 0603 | 2 |
| **6** | **C3** | Ceramic Capacitor $2.2\,\mu\text{F}$, $25\text{V}$, X7R, 10% | TDK Corporation | `C2012X7R1E225K125AB` | 0805 | 1 |
| **7** | **R1** | Current Sense Resistor $4.02\,\Omega$, 1%, 1/8W | Yageo | `RC0805FR-074R02L` | 0805 | 1 |
| **8** | **LED1, LED2** | High-CRI White SMD LED ($5000\text{K}$, CRI $\ge 95$, $V_F \approx 3.05\text{V}$) | Nichia Corporation | `NFSW757GT-V1-P12` | 3030 | 2 |
| **9** | **U2** | LiPo Battery Charger IC with DW01A/8205 Protection | TP4056 Sub-module | `TP4056-PROTECT-MOD` | Module | 1 |
| **10**| **BAT1** | Rechargeable LiPo Cell, $3.7\text{V}$, $300\text{ mAh}$, 1S | Standard OEM | `LP-502030` | Pouch | 1 |

---

## 5. Bench-Testing Procedure (Physical Measurement Protocol)

To validate the circuit before mechanical integration, execute the following steps in the electronics lab:

1. **Equipment Required:**
   * Variable DC Bench Power Supply ($0\text{--}10\text{V}$, $0\text{--}2\text{A}$ with digital current readout).
   * Digital Multimeter (Keysight 34461A or handheld Fluke 87V, set to DC mA).
   * 2-Channel Digital Oscilloscope ($100\text{ MHz}$, 10x passive probes).
   * Contact thermocouple (Type K) or thermal imaging camera (FLIR).
2. **Bench Setup:**
   * Assemble the TPS61165 circuit on a copper proto-board or dedicated breakout board.
   * Connect the two Nichia 757 LEDs in series to the output.
   * Insert the multimeter in series with the LED cathode return to measure exact LED current ($I_{LED}$).
3. **Line Regulation & Battery Discharge Sweep:**
   * Set bench power supply to $4.20\text{ V}$ (representing fully charged battery).
   * Power on circuit and record: $I_{IN}$, $V_{OUT}$, $I_{LED}$, and switch node waveform on oscilloscope.
   * Decrease input voltage in $0.2\text{ V}$ increments: $4.0\text{ V}, 3.8\text{ V}, 3.6\text{ V}, 3.4\text{ V}, 3.2\text{ V}, 3.0\text{ V}, 2.8\text{ V}$.
   * **Verification Criterion:** $I_{LED}$ must remain within $50.0\text{ mA} \pm 1.5\text{ mA}$ ($3\%$) from $V_{IN} = 4.2\text{ V}$ down to $3.0\text{ V}$.
4. **Pulsed Operation Verification:**
   * Apply an $800\text{ ms}$ pulse to the CTRL pin using a function generator or monostable switch.
   * Trigger the oscilloscope on the rising edge of CTRL.
   * Measure turn-on settling time: verify LED current rises smoothly without overshoot ($< 5\text{ ms}$ rise time).
5. **Thermal Stability Measurement:**
   * Attach thermocouple bead to LED1 thermal pad using thermal epoxy.
   * Trigger 10 consecutive $800\text{ ms}$ pulses spaced 10 seconds apart (simulating repeated clinical captures).
   * Log temperature rise $\Delta T$. Record actual data.

# Single-Phase Half-Bridge Inverter with PV Source Simulation

This project provides a Python-based simulation of a **Single-Phase Half-Bridge Inverter** powered by a Photovoltaic (PV) source. It analyzes the relationship between the switching signals ($V_{an}$) and the resulting current waveforms on a **purely resistive load**.

## Project Overview
The simulation uses **Sinusoidal Pulse Width Modulation (SPWM)** to convert a DC input into an AC output. The core focus is observing how the **Modulation Index ($m_a$)** and **Frequency Modulation Ratio ($m_f$)** influence harmonic distortion and fundamental power delivery.

## System Specifications

| Parameter | Value | Notes |
| :--- | :--- | :--- |
| **PV Source ($V_{dc}$)** | 60 V | Constant DC input from PV array |
| **Load Resistance ($R$)** | 10 $\Omega$ | Purely resistive (no inductor/filter) |
| **Fundamental Frequency ($f$)** | 50 Hz | Standard AC utility frequency |
| **Inverter Topology** | Half-Bridge | Uses two switches and a DC midpoint |
| **Modulation Strategy** | SPWM | Sine-Triangle carrier comparison |

## The Physics & Logic

### 1. Phase-to-Neutral Voltage ($V_{an}$)
In a half-bridge configuration, the output voltage toggles between the positive and negative rails of the split DC bus:
* **Switch 1 ON:** $V_{an} = +\frac{V_{dc}}{2} = +30V$
* **Switch 2 ON:** $V_{an} = -\frac{V_{dc}}{2} = -30V$

### 2. Resistive Load Current
Because the load is purely resistive, the current waveform is an exact replica of the voltage pulses, scaled by $1/R$:
$$i_{load}(t) = \frac{V_{an}(t)}{R}$$
*Note: Without an LC filter, the current remains a pulse train (PWM) and is not a smooth sine wave.*

### 3. Fundamental Harmonic
The peak of the "hidden" 50Hz sine wave within the PWM signal is defined by:
$$V_{peak} = \frac{m_a \cdot V_{dc}}{2}$$

## Simulated Cases

The simulation loops through three distinct scenarios to compare power quality:

| Case | $m_a$ | $m_f$ | $f_{sw}$ | Characteristics |
| :--- | :--- | :--- | :--- | :--- |
| **1** | 0.5 | 7 | 350 Hz | Low amplitude, very coarse pulses |
| **2** | 0.5 | 10 | 500 Hz | Low amplitude, better resolution |
| **3** | 0.9 | 4 | 200 Hz | High amplitude, high harmonic distortion |

## Installation & Requirements
Ensure you have Python installed along with the necessary scientific libraries:

```bash
pip install numpy scipy matplotlib pandas

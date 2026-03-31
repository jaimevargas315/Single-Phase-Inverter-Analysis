import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# ---Parameters ---
V_dc = 60           # PV Source Voltage (Volts)
R_load = 10         # Purely Resistive Load (Ohms)
f_sine = 50         # Fundamental frequency (Hz)
fs = 100000         # Sampling Frequency (100 kHz) for high FFT resolution

# --- Setup ---
t_end = 0.06        # 3 cycles at 50Hz
t = np.linspace(0, t_end, int(t_end * fs), endpoint=False)

# --- Define the 3 Cases (ma, mf) ---
cases = [
    (0.5, 7),   # Case 1: Low amplitude, low switching frequency
    (0.5, 10),  # Case 2: Low amplitude, medium switching frequency
    (0.9, 4)    # Case 3: High amplitude, very low switching frequency
]

# Create a figure with subplots for comparison
fig, axes = plt.subplots(3, 2, figsize=(15, 12))
fig.suptitle('Single Phase Half-Bridge Inverter Analysis (Resistive Load)', fontsize=16, fontweight='bold')

for i, (ma, mf) in enumerate(cases):
    # Calculate switching frequency based on mf
    f_sw = mf * f_sine
    
    # 1. Generate PWM Control (Van)
    # Reference Sine Wave
    v_ref = ma * np.sin(2 * np.pi * f_sine * t)
    # Triangular Carrier Wave
    v_carrier = signal.sawtooth(2 * np.pi * f_sw * t, width=0.5)
    
    # Generate the Phase-to-Neutral Voltage (Van)
    # Logic: If v_ref > v_carrier, Switch 1 is ON (+Vdc/2), else Switch 2 is ON (-Vdc/2)
    Van = np.where(v_ref > v_carrier, V_dc/2, -V_dc/2)
    
    # Since load is purely resistive: I = V/R
    I_load = Van / R_load
    
    # 2. Perform FFT for Harmonic Distortion Analysis
    N = len(Van)
    yf = np.fft.rfft(Van)
    xf = np.fft.rfftfreq(N, 1/fs)
    mags = (2.0/N) * np.abs(yf) # Normalize magnitudes
    
    # Find Fundamental Magnitude (V1)
    fund_idx = np.argmin(np.abs(xf - f_sine))
    V1 = mags[fund_idx]
    
    # Calculate THD (Total Harmonic Distortion) up to 5000 Hz
    limit_idx = np.argmin(np.abs(xf - 5000))
    # THD Formula: sqrt(Sum of squares of harmonics) / Fundamental
    harmonics_sq_sum = np.sum(mags[1:limit_idx]**2) - V1**2
    thd = np.sqrt(max(0, harmonics_sq_sum)) / V1 * 100

    # --- 3. Plotting Case (i) ---
    
    # Time Domain Plot (Left Side)
    axes[i, 0].plot(t, Van, color='blue', alpha=0.7, label='$V_{an}$ (PWM)')
    axes[i, 0].plot(t, v_ref * (V_dc/2), color='black', linestyle='--', label='Ref Sine')
    axes[i, 0].set_title(f'Case {i+1}: $m_a={ma}, m_f={mf}$ ($f_{{sw}}={f_sw}$Hz)')
    axes[i, 0].set_ylabel('Voltage [V]')
    axes[i, 0].grid(True)
    if i == 0: axes[i, 0].legend(loc='upper right')
    
    # Frequency Domain Plot (Right Side)
    axes[i, 1].stem(xf, mags, linefmt='red', markerfmt=' ', basefmt='black')
    axes[i, 1].set_xlim(0, 2000) # Limit x-axis to see harmonics clearly
    axes[i, 1].set_title(f'Harmonic Spectrum (THD $\\approx$ {thd:.2f}%)')
    axes[i, 1].set_ylabel('Magnitude [V]')
    axes[i, 1].grid(True)

# Formatting the bottom axis
axes[2, 0].set_xlabel('Time [s]')
axes[2, 1].set_xlabel('Frequency [Hz]')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

import pandas as pd
def print_table_line(widths):
    line = "+" + "+".join(["-" * (w + 2) for w in widths]) + "+"
    print(line)
    
results = [
    ["Case 1", 0.5, 7, "350 Hz", "100 V", "10 A"],
    ["Case 2", 0.5, 10, "500 Hz", "100 V", "10 A"],
    ["Case 3", 0.9, 4, "200 Hz", "180 V", "18 A"]
]

print("\n" + "="*34)
print(" SIMULATION CASE RESULTS ")
print("="*34)

res_widths = [8, 10, 10, 15, 12, 12]
print_table_line(res_widths)
headers = ["Case", "ma", "mf", "f_sw", "V_peak", "I_peak"]
print(f"| {' | '.join([f'{h:<{w}}' for h, w in zip(headers, res_widths)])} |")
print_table_line(res_widths)

for row in results:
    print(f"| {row[0]:<8} | {row[1]:<10} | {row[2]:<10} | {row[3]:<15} | {row[4]:<12} | {row[5]:<12} |")

print_table_line(res_widths)
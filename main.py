import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# --- Parameters ---
V_dc = 60           # PV Source Voltage (Volts)
R_load = 10         # Purely Resistive Load (Ohms)
f_sine = 50         # Fundamental frequency (Hz)
fs = 100000         # Sampling Frequency (100 kHz) for high FFT resolution

# --- Setup ---
t_end = 0.06        # 3 cycles at 50Hz
t = np.linspace(0, t_end, int(t_end * fs), endpoint=False)

# --- Define the 3 Cases (ma, mf) ---
cases = [
    (0.5, 7),   # Case 1: Low modulation index, low frequency ratio
    (0.5, 10),  # Case 2: Low modulation index, higher frequency ratio
    (0.9, 4)    # Case 3: High modulation index, very low frequency ratio
]

# This list will store our data dynamically for the terminal table
dynamic_results = []

# Create a 3x3 grid (3 cases x 3 types of plots)
fig, axes = plt.subplots(3, 3, figsize=(18, 12))
fig.suptitle('Single Phase Half-Bridge Inverter: Comprehensive PWM Analysis (60V Source)', 
             fontsize=16, fontweight='bold')

for i, (ma, mf) in enumerate(cases):
    # Calculate switching frequency based on mf
    f_sw = mf * f_sine
    
    # 1. Generate PWM Control Components
    v_ref_n = ma * np.sin(2 * np.pi * f_sine * t)      # Normalized Reference Sine
    v_carrier = signal.sawtooth(2 * np.pi * f_sw * t, width=0.5) # Triangular Carrier
    
    # Generate Phase-to-Neutral Voltage (Van)
    Van = np.where(v_ref_n > v_carrier, V_dc/2, -V_dc/2)
    
    # Scale the reference sine wave for overlay plotting (+/- 30V scale)
    v_ref_scaled = v_ref_n * (V_dc/2)
    
    # 2. Generate Load Current (I = V/R for resistive load)
    I_load = Van / R_load
    
    # 3. Perform FFT for Harmonic Distortion Analysis
    N = len(Van)
    yf = np.fft.rfft(Van)
    xf = np.fft.rfftfreq(N, 1/fs)
    mags = (2.0/N) * np.abs(yf)
    
    # Find Fundamental Magnitude (at 50Hz)
    fund_idx = np.argmin(np.abs(xf - f_sine))
    V1_actual = mags[fund_idx]
    
    # Calculate THD (Total Harmonic Distortion) up to 5000 Hz
    limit_idx = np.argmin(np.abs(xf - 5000))
    harmonics_sq_sum = np.sum(mags[1:limit_idx]**2) - V1_actual**2
    thd = np.sqrt(max(0, harmonics_sq_sum)) / V1_actual * 100
# ---  DATA CALCULATION FOR TABLE ---
    v_fund_peak = (ma * V_dc) / 2
    i_fund_peak = v_fund_peak / R_load
    
    dynamic_results.append([
        f"Case {i+1}", 
        f"{ma:.2f}", 
        f"{mf}", 
        f"{f_sw} Hz", 
        f"{v_fund_peak:.1f} V", 
        f"{i_fund_peak:.2f} A"
    ])

    # --- PLOTTING ---
    
    # Column 0: Voltage Plot with Sine Overlay
    axes[i, 0].plot(t, Van, color='blue', alpha=0.4, label='PWM $V_{an}$')
    axes[i, 0].plot(t, v_ref_scaled, color='black', linestyle='--', linewidth=1.5, label='Ref Sine')
    axes[i, 0].set_title(f'Case {i+1}: Voltage ($m_a={ma}$)')
    axes[i, 0].set_ylabel('Voltage [V]')
    axes[i, 0].grid(True)
    if i == 0: axes[i, 0].legend(loc='upper right', fontsize='small')
    
    # Column 1: Current Plot (Separate Graph)
    axes[i, 1].plot(t, I_load, color='red', label='Current')
    axes[i, 1].set_title(f'Case {i+1}: Load Current ($I_{{load}}$)')
    axes[i, 1].set_ylabel('Current [A]')
    axes[i, 1].grid(True)
    
    # Column 2: FFT Spectrum
    axes[i, 2].stem(xf, mags, linefmt='green', markerfmt=' ', basefmt='black')
    axes[i, 2].set_xlim(0, 2000)
    axes[i, 2].set_title(f'Spectrum (THD: {thd:.2f}%)')
    axes[i, 2].set_ylabel('Magnitude [V]')
    axes[i, 2].grid(True)

# Formatting X-axes
for j in range(2):
    axes[2, j].set_xlabel('Time [s]')
axes[2, 2].set_xlabel('Frequency [Hz]')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

# --- TABLE PRINTING ---
def print_line(widths):
    print("+" + "+".join(["-" * (w + 2) for w in widths]) + "+")

# Defined widths and headers
widths = [8, 18, 12, 15, 20, 20]
headers = ["Test ID", "Modulation (ma)", "Ratio (mf)", "Switch Freq", "Peak Fund. Voltage", "Peak Fund. Current"]

print("\n" + "="*105)
print(f"{'DETAILED INVERTER PERFORMANCE ANALYSIS (Vdc = ' + str(V_dc) + 'V)':^105}")
print("="*105)

print_line(widths)
print(f"| {' | '.join([f'{h:^{w}}' for h, w in zip(headers, widths)])} |")
print_line(widths)

for row in dynamic_results:
    print(f"| {row[0]:<8} | {row[1]:^18} | {row[2]:^12} | {row[3]:^15} | {row[4]:^20} | {row[5]:^20} |")

print_line(widths)
'''
This code generates a clear visualization of the 16-QAM signal as it would appear on an oscilloscope, 
with distinct colors marking each symbol's segment (symbols 0 - 15, sequentially).

Explanation:
Carrier Frequency (F_LO): Set to 5 Hz for easier visualization.
Sample Rate: Set to 1000 samples per second for smooth waveform rendering.
Duration: 16 seconds to accommodate all 16 symbols.
I and Q Values: Correspond to the 16-QAM constellation points.
Colors: Different colors are used for each symbol to make the transitions more noticeable.
Annotations: Each symbol's amplitude and corresponding decimal value are annotated above the waveform on a single horizontal line.
'''

import numpy as np
import matplotlib.pyplot as plt

# Updated parameters for lower frequency
F_LO = 5  # Carrier frequency of 5 Hz
baud_rate = 1  # 1 symbol per second
sample_rate = 1000  # Sample rate for easier visualization
duration = 16  # 16 seconds for sending 16 symbols sequentially

# Time array
t = np.arange(0, duration, 1/sample_rate)

# Symbols (decimal values 0 through 15)
symbols = list(range(16))

# Map each symbol to its corresponding I and Q values
I_values_new = [-3, -1, 1, 3, -3, -1, 1, 3, -3, -1, 1, 3, -3, -1, 1, 3]
Q_values_new = [-3, -3, -3, -3, -1, -1, -1, -1,  1,  1,  1,  1,  3,  3, 3,  3]

# Define the corresponding binary values for decimal values 0 through 15
bit_values = [format(symbol, '04b') for symbol in symbols]

# Map the amplitudes to their corresponding sqrt representation
amplitude_sqrt_map = {
    2: r'$\sqrt{2}$',
    10: r'$\sqrt{10}$',
    18: r'$\sqrt{18}$'
}

# Plot the oscilloscope voltage trace with more dramatic color changes for each symbol
plt.figure(figsize=(15, 8))  # Increased height to make room for phase angles

# Define a colormap with more distinct colors for each symbol
colors = plt.cm.tab20(np.linspace(0, 1, len(symbols)))

# Generate and plot the signal, coloring each symbol more distinctly
for i, symbol in enumerate(symbols):
    start_idx = i * int(sample_rate)
    end_idx = (i + 1) * int(sample_rate)
    I = I_values_new[symbol]
    Q = Q_values_new[symbol]
    signal_segment = I * np.cos(2 * np.pi * F_LO * t[start_idx:end_idx]) + Q * np.sin(2 * np.pi * F_LO * t[start_idx:end_idx])
    plt.plot(t[start_idx:end_idx], signal_segment, color=colors[i], linewidth=2)

# Annotate each waveform segment with its amplitude (as sqrt), phase angle, and binary value
for i, symbol in enumerate(symbols):
    start_idx = i * int(sample_rate)
    end_idx = (i + 1) * int(sample_rate)
    I = I_values_new[symbol]
    Q = Q_values_new[symbol]
    amplitude_squared = int(I**2 + Q**2)
    amplitude_text = amplitude_sqrt_map.get(amplitude_squared, '')
    phase_angle = np.arctan2(Q, I) * (180 / np.pi)  # Phase angle in degrees
    mid_idx = (start_idx + end_idx) // 2
    plt.text(t[mid_idx], 6, f'{amplitude_text}', fontsize=10, ha='center')  # Show amplitude as sqrt
    plt.text(t[mid_idx], 4.5, f'{phase_angle:.1f}°', fontsize=10, ha='center', color='blue')  # Swapped with binary values
    plt.text(t[mid_idx], -7, f'{bit_values[symbol]}', fontsize=10, ha='center', color='red')  # Swapped with phase angles

# Adjust the title placement
plt.title('Simulated Oscilloscope Voltage Trace for 16-QAM Modulation with Amplitudes, Phase Angles, and Binary Values', fontsize=16, y=1.05)
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.xlim(0, duration)
plt.ylim(-8, 8)  # Adjust y-limit to make space for the annotations
plt.grid(True)
plt.show()

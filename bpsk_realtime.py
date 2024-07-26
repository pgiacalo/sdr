"""
BPSK - realtime animation - Binary Phase Shift Keying animated example. 
This example shows the constellation plot updating in realtime.

A real-time updating plot in Python that shows changes in the BPSK signal.
We use matplotlib's animation capabilities, specifically FuncAnimation from matplotlib.animation. 
We'll adjust the parameters so that the baseband frequency (symbol rate) to update twice per second, 
and we'll animate the plots to reflect changes in the signal in real-time.

Adjusting Parameters
To update the plot twice per second with each update reflecting a change in the binary phase, we'll set the symbol rate to 2 Hz (2 symbols per second). This means each symbol has a duration of 0.5 seconds.

Explanation:

Setup for Real-Time Animation: The FuncAnimation class is used to update the plots in real-time.
Symbol Rate Adjustment: We adjusted the symbol rate to 2 Hz to match your requirement of updating the plot twice per second.
Animation Function: The update function is called every 500 ms (twice per second), which updates the plots according to the current symbol being transmitted.
This setup should provide a clear visualization of how the BPSK signal changes over time, including
	- how its time-domain waveform, frequency spectrum, and constellation diagram evolve.

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parameters
f_carrier = 8  # Carrier frequency in Hz
sample_rate = 1e4  # Sample rate in Hz
symbol_rate = 1  # Symbol rate in symbols per second, updating once per second
num_symbols = 10  # Number of symbols to display in the animation
duration = num_symbols / symbol_rate  # Duration of the signal in seconds

# Time array
t = np.arange(0, duration, 1/sample_rate)

# Generate alternating BPSK symbols (+1 or -1)
symbols = np.array([1 if i % 2 == 0 else -1 for i in range(num_symbols)])

# Repeat each symbol to match the sample rate and symbol rate
samples_per_symbol = int(sample_rate / symbol_rate)
signal = np.repeat(symbols, samples_per_symbol)

# Modulate the signal with the carrier
modulated_signal = signal * np.cos(2 * np.pi * f_carrier * t)

# Initialize the figure and axes
fig, axs = plt.subplots(3, 1, figsize=(10, 15))

# Time domain plot
axs[0].set_title('Time Domain Signal')
axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('Amplitude')
axs[0].set_xlim(0, duration)
axs[0].set_ylim(-1.5, 1.5)
line1, = axs[0].plot([], [], lw=2)

# Frequency domain plot
axs[1].set_title('Frequency Domain')
axs[1].set_xlabel('Frequency (Hz)')
axs[1].set_ylabel('Magnitude')
axs[1].set_xlim(-f_carrier * 5, f_carrier * 5)

# Constellation diagram
axs[2].set_title('Constellation Diagram')
axs[2].set_xlabel('In-phase (I)')
axs[2].set_ylabel('Quadrature (Q)')
axs[2].set_xlim(-1.5, 1.5)
axs[2].set_ylim(-1.5, 1.5)
axs[2].grid(True)
points, = axs[2].plot([], [], 'ro')

def update(frame):
    current_idx_start = frame * samples_per_symbol
    current_modulated_signal = modulated_signal[current_idx_start:current_idx_start + samples_per_symbol]
    current_time = t[current_idx_start:current_idx_start + samples_per_symbol]
    current_symbol = symbols[frame]
    
    # Define color based on current symbol
    color = 'b' if current_symbol == 1 else 'r'
    
    # Update time domain plot
    line1.set_data(current_time, current_modulated_signal)
    line1.set_color(color)
    
    # Update frequency domain plot
    current_spectrum = np.fft.fft(current_modulated_signal)
    frequencies = np.fft.fftfreq(len(current_modulated_signal), 1/sample_rate)
    axs[1].clear()
    axs[1].stem(frequencies, np.abs(current_spectrum), linefmt=color+'-', markerfmt=color+'o', basefmt='k-')
    axs[1].set_xlim(-f_carrier * 5, f_carrier * 5)
    axs[1].set_ylim(0, np.max(np.abs(current_spectrum)) + 1)
    
    # Update constellation diagram to show only the latest point
    points.set_data([current_symbol], [0])
    points.set_color(color)
    
    return line1, points

def init():
    line1.set_data([], [])
    points.set_data([], [])
    return line1, points

# Set up the animation
ani = FuncAnimation(fig, update, frames=num_symbols, init_func=init, blit=False, interval=1000)  # Update once per second

plt.tight_layout()
plt.show()


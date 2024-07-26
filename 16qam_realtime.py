# 16-QAM Signal Generation and Visualization

# Explanation:
# Time Domain Plot: The time domain signal now shows a more complex pattern due to the combination of I and Q modulations.
# Frequency Domain Plot: Displays the spectrum with the main component centered around the carrier frequency, showing how 16-QAM occupies the frequency spectrum.
# Constellation Diagram: Displays the 16 possible states (symbols) in the IQ plane, illustrating the amplitude and phase variations typical of 16-QAM.
# This script will help you visualize how 16-QAM works by showing how the I and Q components create a complex signal with 16 different states, each representing 4 bits of data. This visualization is crucial for understanding modulation in SDR systems. 

# Here’s what we’ll do:

# Generate 16-QAM Symbols: Define the possible values for I and Q components.
# Modulate the Signal: Combine I and Q components with the cosine and sine of the carrier frequency, respectively.
# Plot the Time Domain Signal: Show how the I and Q components combine to form the RF signal.
# Plot the Frequency Domain: Analyze the spectrum of the 16-QAM signal.
# Plot the Constellation Diagram: Visualize the 16 points in the IQ plane.


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parameters
f_carrier = 20  # Carrier frequency in Hz
sample_rate = 1000  # Sample rate for easier visualization
num_symbols = 16  # Total symbols (2 per second for 8 seconds)
symbol_rate = 2   # Symbol rate in symbols per second (updates twice per second)
duration = 8  # Duration of the signal in seconds

# Time array
t = np.arange(0, duration, 1/sample_rate)

# Generate random 16-QAM symbols
np.random.seed(0)  # For reproducibility
I_values = np.random.choice([-3, -1, 1, 3], size=num_symbols)
Q_values = np.random.choice([-3, -1, 1, 3], size=num_symbols)

# Repeat each symbol to match the sample rate and symbol rate
samples_per_symbol = int(sample_rate / symbol_rate)
I_signal = np.repeat(I_values, samples_per_symbol)
Q_signal = np.repeat(Q_values, samples_per_symbol)

# Modulate the signal with the carrier
modulated_I = I_signal * np.cos(2 * np.pi * f_carrier * t)
modulated_Q = Q_signal * np.sin(2 * np.pi * f_carrier * t)
modulated_signal = modulated_I + modulated_Q

# Initialize the figure and subplots
fig, axs = plt.subplots(3, 1, figsize=(10, 12))

# Configure plots for initial state
axs[0].set_title('Time Domain Signal')
axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('Amplitude')
axs[0].set_xlim(0, duration)
axs[0].set_ylim(-10, 10)
line1, = axs[0].plot([], [], 'b')

axs[1].set_title('Frequency Domain')
axs[1].set_xlabel('Frequency (Hz)')
axs[1].set_ylabel('Magnitude')
axs[1].set_xlim(-f_carrier * 2, f_carrier * 2)
axs[1].set_ylim(0, 50)

axs[2].set_title('Constellation Diagram')
axs[2].set_xlabel('In-phase (I)')
axs[2].set_ylabel('Quadrature (Q)')
axs[2].set_xlim(-4, 4)
axs[2].set_ylim(-4, 4)
axs[2].grid(True)
points, = axs[2].plot([], [], 'ro')

def update(frame):
    idx = frame % num_symbols  # Loop the frame index cyclically
    idx_end = (idx + 1) * samples_per_symbol
    # Time Domain Update
    line1.set_data(t[:idx_end], modulated_signal[:idx_end])
    
    # Frequency Domain Update
    spectrum = np.fft.fft(modulated_signal[:idx_end])
    frequencies = np.fft.fftfreq(idx_end, 1/sample_rate)
    axs[1].clear()
    axs[1].stem(frequencies, np.abs(spectrum), 'b', basefmt="-b")
    axs[1].set_title('Frequency Domain')
    axs[1].set_xlabel('Frequency (Hz)')
    axs[1].set_ylabel('Magnitude')
    axs[1].set_xlim(-f_carrier * 2, f_carrier * 2)
    axs[1].set_ylim(0, 50)
    
    # Constellation Diagram Update
    points.set_data(I_values[:idx+1], Q_values[:idx+1])
    
    return line1, points

def init():
    line1.set_data([], [])
    points.set_data([], [])
    axs[1].clear()
    axs[1].stem([0], [0], 'b', basefmt="-b")  # Reset frequency plot
    axs[1].set_xlim(-f_carrier * 2, f_carrier * 2)
    axs[1].set_ylim(0, 50)
    return line1, points

# Set up the animation
ani = FuncAnimation(fig, update, init_func=init, frames=np.arange(num_symbols * int(duration / symbol_rate)), 
                    blit=False, interval=500, repeat=True)

plt.tight_layout()
plt.show()

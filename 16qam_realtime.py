"""
16-QAM IQ Signal Generation and Animation Visualization of Constellation X-Y Graph

16-QAM animation script to generate the 16 IQ values sequentially rather than randomly, and ensure that all 16 points appear on the constellation diagram after 8 seconds, you can update the code as follows. Additionally, I'll include a delay of 4 seconds at the end of each loop before it repeats, which can be handled using a pause or delay mechanism in the animation loop.

Here’s the updated approach:

Approach:
Sequential IQ Values: Generates all possible combinations for a 16-QAM constellation.
End-of-Loop Delay: Incorporates a delay at the end of each cycle using time.sleep, which pauses the program. 
	Note: Using time.sleep in the animation update might block the GUI thread, making the interface unresponsive. 
	If that's an issue, consider alternative timing methods like a countdown or using additional callbacks to manage delays.
Initialization and Update Functions: Appropriately manage plot clearing and data updating for clear visualization.
This setup ensures that you can clearly see each of the 16 different states on the constellation diagram, 
with each state changing every half second, and the animation pausing for 4 seconds at the end of each cycle before repeating.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

# Parameters
f_carrier = 20  # Carrier frequency in Hz
sample_rate = 1000  # Sample rate for easier visualization
symbol_rate = 2  # 2 symbols per second
duration = 8  # Duration of the signal in seconds
delay_duration = 4  # Delay of 4 seconds at the end of each loop

# Generate all 16 QAM points sequentially (4x4 grid)
I_values = np.tile([-3, -1, 1, 3], 4)
Q_values = np.repeat([-3, -1, 1, 3], 4)

# Time array
t = np.arange(0, duration, 1/sample_rate)

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

# Color cycle for time domain signal
colors = ['blue', 'red']  # Alternating colors

def update(frame):
    if frame == 0:
        for ax in axs:
            ax.clear()  # Clear all axes at the beginning of each loop
        # Reconfigure the axes after clearing
        configure_axes()

    idx_start = frame * samples_per_symbol
    idx_end = (frame + 1) * samples_per_symbol
    color = colors[frame % 2]  # Alternate colors between blue and red
    axs[0].plot(t[idx_start:idx_end], modulated_signal[idx_start:idx_end], color=color)
    
    spectrum = np.fft.fft(modulated_signal[:idx_end])
    frequencies = np.fft.fftfreq(idx_end, 1/sample_rate)
    axs[1].clear()
    axs[1].stem(frequencies, np.abs(spectrum), 'b', basefmt="-b")
    axs[1].set_xlim(-f_carrier * 3, f_carrier * 3)  # Extended to 3 times the carrier frequency
    axs[1].set_ylim(0, np.max(np.abs(spectrum)) * 1.1)  # Adjust the y-axis to 110% of the max value
    
    axs[2].scatter(I_values[:frame + 1], Q_values[:frame + 1], color='red')
    
    if frame == len(I_values) - 1:  # Check if it's the last point
        fig.canvas.draw()  # Force drawing the updates
        fig.canvas.flush_events()  # Ensure all events are processed
        time.sleep(delay_duration)  # Delay before repeating loop

    return []

def configure_axes():
    axs[0].set_title('Time Domain Signal')
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Amplitude')
    axs[0].set_xlim(0, duration)
    axs[0].set_ylim(-10, 10)
    
    axs[1].set_title('Frequency Domain')
    axs[1].set_xlabel('Frequency (Hz)')
    axs[1].set_ylabel('Magnitude')
    axs[1].set_xlim(-f_carrier * 3, f_carrier * 3)  # Same extension as in update
    axs[1].set_ylim(0, 50)  # Set a default y-axis limit
    
    axs[2].set_title('Constellation Diagram')
    axs[2].set_xlabel('In-phase (I)')
    axs[2].set_ylabel('Quadrature (Q)')
    axs[2].set_xlim(-4, 4)
    axs[2].set_ylim(-4, 4)
    axs[2].grid(True)

def init():
    for ax in axs:
        ax.clear()  # Clear all axes on init
    configure_axes()  # Reconfigure after clearing
    return []

# Set up the animation
ani = FuncAnimation(fig, update, init_func=init, frames=np.arange(len(I_values)), 
                    blit=False, interval=500, repeat=True)

plt.tight_layout()
plt.show()

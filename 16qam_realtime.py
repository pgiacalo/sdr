"""
16-QAM IQ Signal Generation and Animation Visualization of Constellation X-Y Graph

In 16-QAM (Quadrature Amplitude Modulation), the variation in the signal to encode data 
is achieved by changing both the amplitude and the phase of the carrier wave, and not the frequency. 

Here’s a breakdown of how it works:

Amplitude and Phase Variation: In 16-QAM, each symbol represents 4 bits of data. 
There are 16 different symbols, each corresponding to a unique combination of amplitude and phase. 
This method effectively combines both amplitude modulation (AM) and phase modulation (PM).

IQ Components:

I (In-phase) and Q (Quadrature-phase) components determine the overall signal. 
Each component can take on one of four amplitude levels (for example, -3, -1, 1, 3 in your code). 
These levels can be seen as the x and y coordinates in a constellation diagram, which represents the phase and amplitude of the signal.

The combination of I and Q for each symbol thus determines the resultant vector's amplitude and angle relative to the carrier wave.

Constellation Diagram: The 16 different states (or symbols) are visually represented in the IQ plane on a constellation diagram. 
Each point on this diagram corresponds to a specific phase (angle) and amplitude (distance from the origin) configuration.

Carrier Frequency: It remains constant. What changes per symbol is the carrier’s phase and amplitude as influenced by the I and Q values. 
Changing the carrier frequency is a different modulation scheme called Frequency Shift Keying (FSK).

In summary, 16-QAM modulates the amplitude and phase of the carrier wave to transmit data. 
Each of the 16 possible combinations of I and Q values alters the carrier in a unique way, allowing it to carry 4 bits of information per symbol. 
The frequency of the carrier wave does NOT change; instead, it serves as the reference for modulating amplitude and phase.

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

# Add variable to control white space
subplot_spacing = 8.0  # Adjust this value to increase/decrease spacing

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

# Calculate amplitude and phase for each IQ pair
amplitudes = np.sqrt(I_values**2 + Q_values**2)
phases = np.arctan2(Q_values, I_values)  # arctan2 handles all quadrants

# Print carrier frequency and each symbol's amplitude and phase
print(f"Carrier Frequency: {f_carrier} Hz")
print("Amplitude and Phase for each Symbol:")
for i, (I, Q, A, theta) in enumerate(zip(I_values, Q_values, amplitudes, phases)):
    print(f"Symbol {i+1}: I = {I}, Q = {Q}, Amplitude = {A:.2f}, Phase = {np.degrees(theta):.2f} degrees")

# Initialize the figure and subplots
fig, axs = plt.subplots(3, 1, figsize=(10, 12))

def update(frame):
    if frame == 0:
        for ax in axs:
            ax.clear()
        configure_axes()
    idx_start = frame * samples_per_symbol
    idx_end = (frame + 1) * samples_per_symbol
    color = ['blue', 'red'][frame % 2]
    axs[0].plot(t[idx_start:idx_end], modulated_signal[idx_start:idx_end], color=color)
    
    spectrum = np.fft.fft(modulated_signal[:idx_end])
    frequencies = np.fft.fftfreq(idx_end, 1/sample_rate)
    axs[1].clear()
    axs[1].stem(frequencies, np.abs(spectrum), 'b', basefmt="-b")
    axs[1].set_xlim(-f_carrier * 3, f_carrier * 3)
    axs[1].set_ylim(0, np.max(np.abs(spectrum)) * 1.1)
    
    axs[2].scatter(I_values[:frame + 1], Q_values[:frame + 1], color='red')
    
    if frame == len(I_values) - 1:
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(delay_duration)

def configure_axes():
    axs[0].set_title('Time Domain Signal')
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Amplitude (Units)')
    axs[0].set_xlim(0, duration)
    axs[0].set_ylim(-10, 10)
    
    axs[1].set_title('Frequency Domain')
    axs[1].set_xlabel('Frequency (Hz)')
    axs[1].set_ylabel('Magnitude (Arbitrary Units)')
    axs[1].set_xlim(-f_carrier * 3, f_carrier * 3)
    axs[1].set_ylim(0, 50)
    
    axs[2].set_title('Constellation Diagram')
    axs[2].set_xlabel('In-phase (I)')
    axs[2].set_ylabel('Quadrature (Q)')
    axs[2].set_xlim(-4, 4)
    axs[2].set_ylim(-4, 4)
    axs[2].grid(True)

def init():
    for ax in axs:
        ax.clear()
    configure_axes()
    return []

ani = FuncAnimation(fig, update, init_func=init, frames=np.arange(len(I_values)), blit=False, interval=500, repeat=True)

# Adjust the layout with increased spacing
plt.tight_layout(rect=[0, 0.03, 1, 0.95], h_pad=subplot_spacing)

plt.show()
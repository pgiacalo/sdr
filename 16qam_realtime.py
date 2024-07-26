"""
16-QAM IQ Signal Generation and Animation (Visualization of waveforms, frequencies, and constellation graphs)

Let's break down how the quadrature signal is created in this program and how the 16 values can be used to encode data.

Quadrature Signal Creation:

The quadrature signal in this program is created using Quadrature Amplitude Modulation (QAM), specifically 16-QAM. Here's how it works:
a) Symbol Generation:

I_values = np.tile([-3, -1, 1, 3], 4)
Q_values = np.repeat([-3, -1, 1, 3], 4)

These lines create 16 unique combinations of In-phase (I) and Quadrature (Q) values, representing the 16 symbols in 16-QAM.

b) Signal Modulation:
python
modulated_I = I_signal * np.cos(2 * np.pi * f_carrier * t)
modulated_Q = Q_signal * np.sin(2 * np.pi * f_carrier * t)
modulated_signal = modulated_I + modulated_Q

Here, the I and Q values are modulated onto cosine and sine carrier waves, respectively. The sum of these two orthogonal signals creates the final modulated signal.

Encoding Data with 16 Values:

In 16-QAM, each symbol (combination of I and Q) can represent 4 bits of data. Here's how:

a) Bit to Symbol Mapping:

Each of the 16 unique I-Q combinations represents a 4-bit sequence.
For example:
(-3, -3) might represent 0000
(-3, -1) might represent 0001
(3, 3) might represent 1111
And so on for all 16 combinations

b) Data Capacity:

With 16 symbols, we can encode 4 bits per symbol (log₂(16) = 4).
In this program, we're transmitting 2 symbols per second (symbol_rate = 2).
This means we can transmit 8 bits (1 byte) of data per second.

c) Encoding Process:

Take a stream of binary data.
Group the data into 4-bit chunks.
Map each 4-bit chunk to its corresponding I-Q value.
Modulate these I-Q values as described earlier.

d) Decoding Process (not implemented in this code):

Demodulate the received signal to extract I-Q values.
Map each I-Q value back to its corresponding 4-bit sequence.
Concatenate these bit sequences to recover the original data.

The advantage of 16-QAM is that it allows for higher data rates compared to simpler modulation schemes like QPSK (which only has 4 symbols), at the cost of being more susceptible to noise and requiring more complex hardware.
This program demonstrates the modulation part of the process, showing how digital data (represented by the 16 I-Q combinations) can be converted into an analog signal for transmission. In a real-world application, you would add error correction, synchronization, and other features to make the communication more robust.

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
fig.suptitle('16QAM Animation', fontsize=16)  # Add title to the GUI

def update(frame):
    # Clear only frequency domain and constellation diagram
    axs[1].clear()
    axs[2].clear()
    
    configure_axes()
    
    # Time Domain Signal (additive drawing with alternating colors)
    for i in range(frame + 1):
        idx_start = i * samples_per_symbol
        idx_end = (i + 1) * samples_per_symbol
        color = 'blue' if i % 2 == 0 else 'red'
        axs[0].plot(t[idx_start:idx_end], modulated_signal[idx_start:idx_end], color=color)
    
    # Frequency Domain
    spectrum = np.fft.fft(modulated_signal[:(frame + 1) * samples_per_symbol])
    frequencies = np.fft.fftfreq((frame + 1) * samples_per_symbol, 1/sample_rate)
    axs[1].stem(frequencies, np.abs(spectrum), 'b', basefmt="-b")
    axs[1].set_xlim(-f_carrier * 3, f_carrier * 3)
    axs[1].set_ylim(0, np.max(np.abs(spectrum)) * 1.1)
    
    # Constellation Diagram
    axs[2].scatter(I_values[:frame + 1], Q_values[:frame + 1], color='red')
    
    if frame == len(I_values) - 1:
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(delay_duration)

def configure_axes():
    # Time Domain Signal
    axs[0].set_title('Time Domain Signal')
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Amplitude (Units)')
    axs[0].set_xlim(0, duration)
    axs[0].set_ylim(-5, 5)
    
    # Frequency Domain
    axs[1].set_title('Frequency Domain')
    axs[1].set_xlabel('Frequency (Hz)')
    axs[1].set_ylabel('Magnitude (Arbitrary Units)')
    axs[1].set_xlim(-f_carrier * 3, f_carrier * 3)
    axs[1].set_ylim(0, 50)
    
    # Constellation Diagram
    axs[2].set_title('Constellation Diagram')
    axs[2].set_xlabel('In-phase (I)')
    axs[2].set_ylabel('Quadrature (Q)')
    axs[2].set_xlim(-4, 4)
    axs[2].set_ylim(-4, 4)
    axs[2].grid(True)

def init():
    axs[0].clear()
    axs[1].clear()
    axs[2].clear()
    configure_axes()
    return []

ani = FuncAnimation(fig, update, init_func=init, frames=np.arange(len(I_values)), blit=False, interval=500, repeat=True)

# Adjust the layout with increased spacing
plt.tight_layout(rect=[0, 0.03, 1, 0.95], h_pad=subplot_spacing)

plt.show()



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

# Parameters
f_carrier = 1e3  # Carrier frequency in Hz
sample_rate = 1e4  # Sample rate in Hz
num_symbols = 100  # Number of symbols
symbol_rate = 100  # Symbol rate in symbols per second
duration = num_symbols / symbol_rate  # Duration of the signal in seconds

# Time array
t = np.arange(0, duration, 1/sample_rate)

# Generate random 16-QAM symbols
np.random.seed(0)  # For reproducibility
I_values = np.random.choice([
	-3, -1, 1, 3], size=num_symbols)
Q_values = np.random.choice([-3, -1, 1, 3], size=num_symbols)

# Repeat each symbol to match the sample rate and symbol rate
samples_per_symbol = int(sample_rate / symbol_rate)
I_signal = np.repeat(I_values, samples_per_symbol)
Q_signal = np.repeat(Q_values, samples_per_symbol)

# Modulate the signal with the carrier
modulated_I = I_signal * np.cos(2 * np.pi * f_carrier * t)
modulated_Q = Q_signal * np.sin(2 * np.pi * f_carrier * t)
modulated_signal = modulated_I - modulated_Q

# Plot in time domain
plt.figure(figsize=(10, 8))
plt.subplot(4, 1, 1)
plt.plot(t, modulated_signal)
plt.title('Time Domain Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

# Frequency domain
frequencies = np.fft.fftfreq(len(t), 1/sample_rate)
spectrum = np.fft.fft(modulated_signal)
plt.subplot(4, 1, 2)
plt.stem(frequencies, np.abs(spectrum), 'b', markerfmt=" ", basefmt="-b")
plt.title('Frequency Domain')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.xlim(-f_carrier*2, f_carrier*2)  # Limit x-axis to observe the carrier frequency

# Constellation diagram
plt.subplot(4, 1, 3)
plt.scatter(I_values, Q_values, color='red')
plt.title('Constellation Diagram')
plt.xlabel('In-phase (I)')
plt.ylabel('Quadrature (Q)')
plt.grid(True)
plt.axis('equal')

# Show all plots
plt.tight_layout()
plt.show()

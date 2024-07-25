# BPSK - Binary Phase Shift Keying example

# Explanation:
# Time Domain Plot: Shows the BPSK signal modulated with a cosine wave. The BPSK modulates the phase of the carrier wave, flipping it by 180 degrees per symbol.
# Frequency Domain Plot: Displays the frequency components of the signal, centered around the carrier frequency and its negative counterpart.
# Constellation Diagram: For BPSK, this is straightforward, showing points at +1 and -1 on the real axis, representing the two possible phases of the carrier (0 and π).
# This code will provide a basic visualization to help you understand how the signal behaves in time and frequency domains, and what the constellation diagram looks like for BPSK. 

# Here's what we'll do:

# Generate a simple BPSK signal as a starting point.
# Plot the signal in the time domain.
# Perform an FFT (Fast Fourier Transform) to view the signal in the frequency domain.
# Plot the IQ constellation diagram.


import numpy as np
import matplotlib.pyplot as plt

# Parameters
f_carrier = 1e3  # Carrier frequency in Hz
sample_rate = 1e4  # Sample rate in Hz
num_symbols = 10  # Number of symbols
symbol_rate = 100  # Symbol rate in symbols per second
duration = num_symbols / symbol_rate  # Duration of the signal in seconds

# Time array
t = np.arange(0, duration, 1/sample_rate)

# Generate random BPSK symbols (+1 or -1)
np.random.seed(0)  # For reproducibility
symbols = np.random.choice([-1, 1], size=num_symbols)

# Repeat each symbol to match the sample rate and symbol rate
samples_per_symbol = int(sample_rate / symbol_rate)
signal = np.repeat(symbols, samples_per_symbol)

# Modulate the signal with the carrier
modulated_signal = signal * np.cos(2 * np.pi * f_carrier * t)

# Plot in time domain
plt.figure(figsize=(10, 6))
plt.subplot(3, 1, 1)
plt.plot(t, modulated_signal)
plt.title('Time Domain Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

# Frequency domain
frequencies = np.fft.fftfreq(len(t), 1/sample_rate)
spectrum = np.fft.fft(modulated_signal)
plt.subplot(3, 1, 2)
plt.stem(frequencies, np.abs(spectrum), 'b', markerfmt=" ", basefmt="-b")
plt.title('Frequency Domain')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.xlim(-f_carrier*2, f_carrier*2)  # Limit x-axis to observe the carrier frequency

# Constellation diagram
plt.subplot(3, 1, 3)
plt.scatter(symbols, np.zeros_like(symbols), color='red')  # Only real parts since BPSK
plt.title('Constellation Diagram')
plt.xlabel('In-phase (I)')
plt.ylabel('Quadrature (Q)')
plt.grid(True)
plt.axis('equal')

# Show all plots
plt.tight_layout()
plt.show()

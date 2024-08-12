import numpy as np
import matplotlib.pyplot as plt

# Number of symbols
num_symbols = 100  # Reduced from 1000 for clarity

# Generate random symbols for 16-QAM (0 to 15)
data_symbols = np.random.randint(0, 16, num_symbols)

# Map symbols to constellation points (Gray coded)
# Constellation points: +/- 1, +/- 3 on both I (real) and Q (imaginary) axes
symbol_map = {0: (-3-3j), 1: (-3-1j), 2: (-3+3j), 3: (-3+1j),
              4: (-1-3j), 5: (-1-1j), 6: (-1+3j), 7: (-1+1j),
              8: (3-3j),  9: (3-1j), 10: (3+3j), 11: (3+1j),
              12: (1-3j), 13: (1-1j), 14: (1+3j), 15: (1+1j)}

# Modulate symbols
modulated_signal = np.array([symbol_map[symbol] for symbol in data_symbols])

# Time vector for plotting
time_vector = np.arange(len(modulated_signal))

# Compute the combined signal waveform by treating I and Q as a complex signal
combined_signal = modulated_signal.real + 1j * modulated_signal.imag

# Compute amplitude of the combined signal (envelope)
amplitude_envelope = np.abs(combined_signal)

# Plotting the In-Phase, Quadrature, and Combined Amplitude Envelope on the same figure
plt.figure(figsize=(12, 8))

# Plot In-phase component with markers
plt.subplot(3, 1, 1)
plt.stem(time_vector, modulated_signal.real, linefmt='b-', markerfmt='bo', basefmt='b-', label='In-Phase (I)')
plt.title('16-QAM Signal - In-Phase, Quadrature, and Combined Amplitude')
plt.ylabel('In-Phase Amplitude')
plt.legend()

# Plot Quadrature component with markers
plt.subplot(3, 1, 2)
plt.stem(time_vector, modulated_signal.imag, linefmt='g-', markerfmt='go', basefmt='g-', label='Quadrature (Q)')
plt.ylabel('Quadrature Amplitude')
plt.legend()

# Plot Combined Amplitude Envelope with markers
plt.subplot(3, 1, 3)
plt.stem(time_vector, amplitude_envelope, linefmt='r-', markerfmt='ro', basefmt='r-', label='Amplitude Envelope')
plt.xlabel('Time (symbol index)')
plt.ylabel('Amplitude')
plt.legend()

plt.tight_layout()
plt.show()

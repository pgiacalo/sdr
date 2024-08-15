import numpy as np
from pyhackrf import HackRF

# Define the I and Q values for 16-QAM
I_values = np.array([-3, -1, 1, 3, -3, -1, 1, 3, -3, -1, 1, 3, -3, -1, 1, 3])
Q_values = np.array([-3, -3, -3, -3, -1, -1, -1, -1, 1, 1, 1, 1, 3, 3, 3, 3])

# Normalize the amplitude
I_values = I_values / np.max(np.abs(I_values))
Q_values = Q_values / np.max(np.abs(Q_values))

# Define the data sequence (symbols 0 through 15)
data_sequence = np.arange(16)

# Symbol rate (1 baud = 1 symbol per second)
symbol_rate = 1
sample_rate = 8 * symbol_rate  # Higher sample rate for better waveform resolution

# Time array for one symbol period
t = np.linspace(0, 1/symbol_rate, sample_rate, endpoint=False)

# Create the 16-QAM signal
qam_signal = np.array([], dtype=np.complex64)
for symbol in data_sequence:
    i = I_values[symbol]
    q = Q_values[symbol]
    symbol_signal = (i + 1j*q) * np.exp(1j * 2 * np.pi * t)  # Create baseband signal
    qam_signal = np.concatenate((qam_signal, symbol_signal))

# Normalize the signal to the HackRF output range (-1 to 1)
qam_signal /= np.max(np.abs(qam_signal))

# Convert to 8-bit signed integers for HackRF
qam_signal = np.array(qam_signal * 127, dtype=np.int8)
iq_signal = np.empty(2 * len(qam_signal), dtype=np.int8)
iq_signal[0::2] = qam_signal.real  # I (real) part
iq_signal[1::2] = qam_signal.imag  # Q (imaginary) part

# HackRF setup
hackrf = HackRF()
hackrf.sample_rate = sample_rate * 1e6  # Sample rate in Hz
hackrf.center_freq = 915e6  # Frequency in Hz (915 MHz is an ISM band example)
hackrf.txvga_gain = 20  # TX gain

def transmit_callback(_):
    return iq_signal.tobytes()

hackrf.start_tx(transmit_callback)

try:
    print("Transmitting 16-QAM sequence 0 through 15 at 1 baud.")
    input("Press Enter to stop transmission...")
finally:
    hackrf.stop_tx()
    hackrf.close()

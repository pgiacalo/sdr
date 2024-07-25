"""
# QAM Signal Generation and Visualization

QAM stands for Quadrature Amplitude Modulation, a widely used modulation technique in digital communication systems 
that combines amplitude modulation of two carrier waves, which are out of phase by 90 degrees (in quadrature). 
This method efficiently utilizes bandwidth by transmitting two different signals simultaneously over the same channel.

How QAM Works
QAM works by varying both the amplitude and the phase of the carrier signal, allowing it to carry more information 
than either amplitude modulation (AM) or phase modulation (PM) alone. 
It encodes data into the amplitude of two carrier waves, typically one sine wave and one cosine wave.

# Explanation:
# Time Domain Plot: The time domain signal now shows a more complex pattern due to the combination of I and Q modulations.
# Frequency Domain Plot: Displays the spectrum with the main component centered around the carrier frequency, showing how 16-QAM occupies the frequency spectrum.
# Constellation Diagram: Displays the X possible states (symbols) in the IQ plane, illustrating the amplitude and phase variations typical of 16-QAM.
# This script will help you visualize how QAM works by showing how the I and Q components create a complex signal with 16 different states, each representing 4 bits of data. This visualization is crucial for understanding modulation in SDR systems. 

# Here’s what we’ll do:

Step 1: Generate QAM Constellation
We'll start by generating a QAM constellation. For simplicity, let's handle a generic QAM where you specify the square root of the number of points (e.g., 4 for 16-QAM).

Step 2: Modulate Signal
We'll create a time array, repeat the constellation points to match the sample rate and symbol rate, and then modulate these points using cosine and sine waves for I and Q respectively.

Step 3: Plotting
Finally, we'll plot the time-domain signal, frequency spectrum, and constellation diagram.
"""

import numpy as np
import matplotlib.pyplot as plt

def generate_qam_constellation(m):
    # m is the square root of the number of points (e.g., 4 for 16-QAM)
    x = np.arange(-m+1, m, 2)
    I, Q = np.meshgrid(x, x)
    return I.flatten(), Q.flatten()

def modulate_signal(I, Q, f_carrier, sample_rate, symbol_rate):
    num_symbols = len(I)  # Calculate the number of symbols from I or Q
    samples_per_symbol = int(sample_rate / symbol_rate)
    total_samples = samples_per_symbol * num_symbols
    
    # Time array
    t = np.linspace(0, num_symbols / symbol_rate, total_samples, endpoint=False)
    
    # Repeat symbols to match the sampling rate
    I_signal = np.repeat(I, samples_per_symbol)
    Q_signal = np.repeat(Q, samples_per_symbol)
    
    # Modulate the signal
    modulated_signal = I_signal * np.cos(2 * np.pi * f_carrier * t) + Q_signal * np.sin(2 * np.pi * f_carrier * t)
    return t, modulated_signal

def plot_results(t, signal, I, Q):
    plt.figure(figsize=(12, 8))
    
    # Time Domain Signal
    plt.subplot(3, 1, 1)
    plt.plot(t, signal)
    plt.title('Time Domain Signal')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    
    # Frequency Domain
    plt.subplot(3, 1, 2)
    spectrum = np.fft.fft(signal)
    frequencies = np.fft.fftfreq(len(spectrum), 1 / sample_rate)
    plt.stem(frequencies, np.abs(spectrum), linefmt='b', markerfmt=" ", basefmt="-b")
    plt.title('Frequency Domain')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.xlim(-f_carrier*2, f_carrier*2)
    
    # Constellation Diagram
    plt.subplot(3, 1, 3)
    plt.scatter(I, Q, color='red')
    plt.title('Constellation Diagram')
    plt.xlabel('In-phase (I)')
    plt.ylabel('Quadrature (Q)')
    plt.grid(True)
    plt.axis('equal')
    
    plt.tight_layout()
    plt.show()

# Main parameters
f_carrier = 1e3  # Carrier frequency in Hz
sample_rate = 1e4  # Sample rate in Hz
symbol_rate = 100  # Symbol rate in symbols per second

# Prompt the user for the number of QAM points
print("Select the number of QAM points from the following list: [4, 16, 64, 256, 1024]")
num_points = int(input("Enter the number of points (e.g., 16 for 16-QAM): "))
sqrt_num_points = int(np.sqrt(num_points))

# Generate the QAM constellation
I, Q = generate_qam_constellation(sqrt_num_points)

# Modulate the signal
t, modulated_signal = modulate_signal(I, Q, f_carrier, sample_rate, symbol_rate)

# Plot the results
plot_results(t, modulated_signal, I, Q)




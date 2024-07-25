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
f_carrier = 1e3  # Carrier frequency in Hz
sample_rate = 1e4  # Sample rate in Hz
symbol_rate = 2  # Symbol rate in symbols per second, updating twice per second
num_symbols = 20  # Number of symbols to display in the animation
duration = num_symbols / symbol_rate  # Duration of the signal in seconds

# Time array
t = np.arange(0, duration, 1/sample_rate)

# Generate random BPSK symbols (+1 or -1)
np.random.seed(0)  # For reproducibility
symbols = np.random.choice([-1, 1], size=num_symbols)

# Repeat each symbol to match the sample rate and symbol rate
samples_per_symbol = int(sample_rate / symbol_rate)
signal = np.repeat(symbols, samples_per_symbol)

# Initialize the figure and axes
fig, axs = plt.subplots(3, 1, figsize=(10, 12))  # Adjusted for better fit

# Initialize plots with initial data to avoid empty array issues
init_signal = signal[:1] if len(signal) > 0 else [0]
init_time = t[:1] if len(t) > 0 else [0]
frequencies = np.fft.fftfreq(max(len(init_signal), 1), 1/sample_rate)
spectrum = np.fft.fft(init_signal)

# Time domain plot
axs[0].set_title('Time Domain Signal')
axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('Amplitude')
line1, = axs[0].plot(init_time, init_signal, lw=2)

# Frequency domain plot
axs[1].set_title('Frequency Domain')
axs[1].set_xlabel('Frequency (Hz)')
axs[1].set_ylabel('Magnitude')
axs[1].set_xlim(-f_carrier*2, f_carrier*2)
axs[1].set_ylim(0, np.max(np.abs(spectrum))+1)
line2, stemlines, baseline = axs[1].stem(frequencies, np.abs(spectrum), 'b', markerfmt=" ", basefmt="-b")

# Constellation diagram
axs[2].set_title('Constellation Diagram')
axs[2].set_xlabel('In-phase (I)')
axs[2].set_ylabel('Quadrature (Q)')
axs[2].set_xlim(-1.5, 1.5)
axs[2].set_ylim(-1.5, 1.5)
axs[2].grid(True)
points, = axs[2].plot([], [], 'ro')

def update(frame):
    idx = max(1, frame * samples_per_symbol)  # Ensure idx is never zero
    # Update time domain plot
    line1.set_data(t[:idx], signal[:idx])
    # Update frequency domain plot
    if idx > 1:  # Avoid zero-length array for FFT computation
        frequencies = np.fft.fftfreq(idx, 1/sample_rate)
        spectrum = np.fft.fft(signal[:idx])
        axs[1].clear()
        axs[1].stem(frequencies, np.abs(spectrum), 'b', basefmt="-b")
        axs[1].set_xlim(-f_carrier*2, f_carrier*2)
        axs[1].set_ylim(0, np.max(np.abs(spectrum))+1)
        axs[1].set_title('Frequency Domain')
        axs[1].set_xlabel('Frequency (Hz)')
        axs[1].set_ylabel('Magnitude')
    # Update constellation diagram
    points.set_data(symbols[:frame+1], np.zeros(frame+1))
    return line1, line2, stemlines, baseline, points

ani = FuncAnimation(fig, update, frames=num_symbols + 1, blit=False, interval=500)

plt.tight_layout()
plt.show()


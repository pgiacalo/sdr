import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
from matplotlib.colors import hsv_to_rgb
from matplotlib.widgets import Button

# Parameters
F_LO = 20  # Local Oscillator frequency in Hz (the carrier frequency)
F_BB = 2   # Baseband frequency (the symbol rate) in Hz
sample_rate = 1000  # Sample rate for easier visualization
duration = 8  # Duration of the signal in seconds
delay_duration = 4  # Delay of 4 seconds at the end of each loop

# Generate all 16 QAM points sequentially (4x4 grid)
I_values = np.tile([-3, -1, 1, 3], 4)
Q_values = np.repeat([-3, -1, 1, 3], 4)

# Generate unique colors for each symbol
num_symbols = len(I_values)
hue_values = np.linspace(0, 1, num_symbols, endpoint=False)
colors = [hsv_to_rgb((h, 1, 1)) for h in hue_values]

# Time array
t = np.arange(0, duration, 1/sample_rate)

# Repeat each symbol to match the sample rate and symbol rate
samples_per_symbol = int(sample_rate / F_BB)
I_signal = np.repeat(I_values, samples_per_symbol)
Q_signal = np.repeat(Q_values, samples_per_symbol)

# Modulate the signal with the carrier
modulated_I = I_signal * np.cos(2 * np.pi * F_LO * t)
modulated_Q = Q_signal * np.sin(2 * np.pi * F_LO * t)
modulated_signal = modulated_I + modulated_Q

# Prompt the user to enable or disable noise
user_input = input("Would you like to add noise to the signal? (yes/no): ").strip().lower()
if user_input in ['yes', 'y']:
    noise_amplitude = 0.05  # Low level of noise
else:
    noise_amplitude = 0.0  # No noise

# Initialize the figure and subplots with constrained_layout
fig, axs = plt.subplots(3, 1, figsize=(10, 12), constrained_layout=True)
fig.suptitle('16QAM Animation with Noise' if noise_amplitude > 0 else '16QAM Animation', fontsize=16, y=0.98)

# Flag to toggle circles and lines visibility
show_circles_lines = True

def draw_amplitude_circles(ax):
    circle_radii = [np.sqrt(2), np.sqrt(10), np.sqrt(18)]
    for radius in circle_radii:
        circle = plt.Circle((0, 0), radius, fill=False, color='gray', linestyle='--')
        ax.add_artist(circle)

def draw_phase_lines(ax):
    max_radius = np.sqrt(18)  # Maximum radius of the outer circle
    angles = np.arctan2(Q_values, I_values)
    unique_angles = np.unique(angles)
    for angle in unique_angles:
        x = [0, max_radius * np.cos(angle)]
        y = [0, max_radius * np.sin(angle)]
        ax.plot(x, y, color='gray', linestyle='--', linewidth=1, zorder=1)

def update(frame):
    # Generate noise
    noise_I = noise_amplitude * np.random.randn(len(I_signal))
    noise_Q = noise_amplitude * np.random.randn(len(Q_signal))

    # Add noise to the signals
    noisy_modulated_I = modulated_I + noise_I
    noisy_modulated_Q = modulated_Q + noise_Q
    noisy_modulated_signal = noisy_modulated_I + noisy_modulated_Q

    # Clear all subplots
    for ax in axs:
        ax.clear()
    
    configure_axes()
    
    # Time Domain Signal
    for i in range(frame + 1):
        idx_start = i * samples_per_symbol
        idx_end = (i + 1) * samples_per_symbol
        axs[0].plot(t[idx_start:idx_end], noisy_modulated_signal[idx_start:idx_end], color=colors[i])
    
    # Constellation Diagram
    if show_circles_lines:
        draw_amplitude_circles(axs[1])
        draw_phase_lines(axs[1])
    for i in range(frame + 1):
        axs[1].scatter(I_values[i] + noise_I[i*samples_per_symbol], 
                       Q_values[i] + noise_Q[i*samples_per_symbol], 
                       color=colors[i], s=100, zorder=3)
    
    # Frequency Domain
    spectrum = np.fft.fft(noisy_modulated_signal[:(frame + 1) * samples_per_symbol])
    frequencies = np.fft.fftfreq((frame + 1) * samples_per_symbol, 1/sample_rate)
    axs[2].stem(frequencies, np.abs(spectrum), linefmt=f"C0-", markerfmt=f"C0o", basefmt="-k")
    axs[2].set_xlim(-F_LO * 3, F_LO * 3)
    axs[2].set_ylim(0, np.max(np.abs(spectrum)) * 1.1)
    
    # Highlight the current symbol in the frequency domain
    if frame < len(I_values):
        current_freq = F_LO
        current_magnitude = np.abs(spectrum[np.argmin(np.abs(frequencies - current_freq))])
        axs[2].scatter(current_freq, current_magnitude, color=colors[frame], s=100, zorder=5)
        axs[2].scatter(-current_freq, current_magnitude, color=colors[frame], s=100, zorder=5)
    
    if frame == len(I_values) - 1:
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(delay_duration)

def configure_axes():
    axs[0].set_title('Time Domain Signal')
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Amplitude (Units)')
    axs[0].set_xlim(0, duration)
    axs[0].set_ylim(-5, 5)
    
    axs[1].set_title('Constellation Diagram')
    axs[1].set_xlabel('In-phase (I)')
    axs[1].set_ylabel('Quadrature (Q)')
    axs[1].set_xlim(-4, 4)
    axs[1].set_ylim(-4, 4)
    axs[1].grid(True)
    axs[1].set_aspect('equal', adjustable='box')
    
    axs[2].set_title('Frequency Domain')
    axs[2].set_xlabel('Frequency (Hz)')
    axs[2].set_ylabel('Magnitude (Arbitrary Units)')
    axs[2].set_xlim(-F_LO * 3, F_LO * 3)
    axs[2].set_ylim(0, 50)

def init():
    for ax in axs:
        ax.clear()
    configure_axes()
    return []

def toggle_circles_lines(event):
    global show_circles_lines
    show_circles_lines = not show_circles_lines
    update(len(I_values) - 1)  # Redraw the last frame

# Create the button next to the constellation diagram
ax_button = plt.axes([0.8, 0.58, 0.15, 0.05])
btn_toggle = Button(ax_button, 'Toggle Circles/Lines')
btn_toggle.on_clicked(toggle_circles_lines)

animation = FuncAnimation(fig, update, init_func=init, frames=np.arange(len(I_values)), blit=False, interval=500, repeat=False)

# Start the figure in full screen mode
manager = plt.get_current_fig_manager()
manager.full_screen_toggle()

plt.show()

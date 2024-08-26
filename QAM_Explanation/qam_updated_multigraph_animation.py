import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.animation import FuncAnimation
from scipy import special

def qam_modulate(I_values, Q_values, binary_values):
    """Create QAM constellation points"""
    X, Y = np.meshgrid(I_values, Q_values)
    X = X.flatten()
    Y = Y.flatten()
    constellation = X + 1j * Y
    return constellation, dict(zip(binary_values, constellation))

def calculate_evm(signal, ideal_signal):
    """Calculate Error Vector Magnitude (EVM)"""
    error = signal - ideal_signal
    rms_error = np.sqrt(np.mean(np.abs(error) ** 2))
    rms_signal = np.sqrt(np.mean(np.abs(ideal_signal) ** 2))
    return (rms_error / rms_signal) * 100 if rms_signal != 0 else 0

def calculate_ber(snr_db, M):
    """Calculate Bit Error Rate (BER) for M-QAM"""
    snr = 10**(snr_db/10)
    ber = 4 * (1 - 1/np.sqrt(M)) * special.erfc(np.sqrt(3*snr/(2*(M-1)))) / np.log2(M)
    return ber

def update_waveforms(A, B):
    """Update waveforms based on slider values"""
    sine_wave = A * np.sin(2 * np.pi * frequency * t)
    cosine_wave = B * np.cos(2 * np.pi * frequency * t)
    resultant_waveform = sine_wave + cosine_wave

    line1.set_ydata(sine_wave)
    line2.set_ydata(cosine_wave)
    line3.set_ydata(resultant_waveform)

    highlighted_point.set_offsets([[B, A]])

    evm = calculate_evm(resultant_waveform, resultant_waveform)
    evm_text.set_text(f"EVM: {evm:.2f}%")

    amplitude = np.sqrt(A**2 + B**2)
    phase = np.arctan2(A, B) * 180 / np.pi
    amp_phase_text.set_text(f"Amplitude: {amplitude:.2f}\nPhase: {phase:.2f}°")

    snr_db = 20 * np.log10(amplitude / sNoise.val) if sNoise.val > 0 else float('inf')
    ber = calculate_ber(snr_db, M)
    ber_text.set_text(f"BER: {ber:.2e}")

    fig.canvas.draw_idle()

def update_plot(val):
    global A, B
    A = round(sAmp1.val, 1)
    B = round(sAmp2.val, 1)
    update_waveforms(A, B)

def on_pick(event):
    index = event.ind[0]
    I, Q = np.real(qam_signal)[index], np.imag(qam_signal)[index]
    sAmp2.set_val(I)
    sAmp1.set_val(Q)
    update_plot(None)

def hover(event):
    if event.inaxes == ax_const:
        cont, _ = scatter.contains(event)
        if cont:
            ax_const.set_title(f'{M}-QAM Constellation Diagram (Hovering)', color='black')
        else:
            ax_const.set_title(f'{M}-QAM Constellation Diagram', color='black')
        fig.canvas.draw_idle()

def animate(frame):
    noise_amplitude = sNoise.val
    noise_i = np.random.normal(0, noise_amplitude)
    noise_q = np.random.normal(0, noise_amplitude)
    noisy_I = B + noise_i
    noisy_Q = A + noise_q
    
    highlighted_point.set_offsets([[noisy_I, noisy_Q]])
    
    noisy_sine = A * np.sin(2 * np.pi * frequency * t) + noise_q
    noisy_cosine = B * np.cos(2 * np.pi * frequency * t) + noise_i
    noisy_resultant = noisy_sine + noisy_cosine
    
    line1.set_ydata(noisy_sine)
    line2.set_ydata(noisy_cosine)
    line3.set_ydata(noisy_resultant)
    
    ideal_signal = A * np.sin(2 * np.pi * frequency * t) + B * np.cos(2 * np.pi * frequency * t)
    evm = calculate_evm(noisy_resultant, ideal_signal)
    evm_text.set_text(f"EVM: {evm:.2f}%")
    
    amplitude = np.sqrt(noisy_I**2 + noisy_Q**2)
    phase = np.arctan2(noisy_Q, noisy_I) * 180 / np.pi
    amp_phase_text.set_text(f"Amplitude: {amplitude:.2f}\nPhase: {phase:.2f}°")
    
    snr_db = 20 * np.log10(amplitude / noise_amplitude) if noise_amplitude > 0 else float('inf')
    ber = calculate_ber(snr_db, M)
    ber_text.set_text(f"BER: {ber:.2e}")
    
    fig.canvas.draw_idle()

    return [highlighted_point, line1, line2, line3, evm_text, amp_phase_text, ber_text]

def change_modulation(label):
    global M, qam_signal, binary_values, scatter, A
    M = int(label.split('-')[0])
    
    if M == 2:  # BPSK
        I_values = np.array([-1, 1])
        Q_values = np.array([0])
    elif M == 4:  # QPSK
        I_values = Q_values = np.array([-1, 1])
        A = 0  # Set default sine amplitude to 0 for QPSK
        sAmp1.set_val(0)  # Update slider value
    else:  # 16-QAM
        I_values = Q_values = np.array([-3, -1, 1, 3])
    
    binary_values = [f"{i:0{int(np.log2(M))}b}" for i in range(M)]
    qam_signal, _ = qam_modulate(I_values, Q_values, binary_values)
    
    scatter.set_offsets(np.column_stack((np.real(qam_signal), np.imag(qam_signal))))
    
    for txt in ax_const.texts:
        txt.remove()
    for i, (x, y) in enumerate(zip(np.real(qam_signal), np.imag(qam_signal))):
        ax_const.text(x, y + 0.2, binary_values[i], ha='center', va='center')
    
    ax_const.set_title(f'{M}-QAM Constellation Diagram')
    update_plot(None)

def show_tutorial():
    tutorial_text = """
    QAM Modulation Tutorial:
    
    1. Constellation Diagram:
       - Each point represents a unique symbol
       - X-axis: In-phase (I) component
       - Y-axis: Quadrature (Q) component
    
    2. Waveforms:
       - Red: Sine wave (Q component)
       - Green: Cosine wave (I component)
       - Blue: Combined QAM signal
    
    3. Sliders:
       - Adjust amplitudes of I and Q components
       - Control noise level
    
    4. Metrics:
       - EVM: Error Vector Magnitude
       - BER: Bit Error Rate
    
    5. Interaction:
       - Click on constellation points
       - Hover over constellation diagram
       - Change modulation order
    
    Experiment with different settings to see how
    they affect the signal and error rates!
    """
    plt.figure(figsize=(10, 8))
    plt.text(0.05, 0.95, tutorial_text, fontsize=12, va='top')
    plt.axis('off')
    plt.title("QAM Modulation Tutorial")
    plt.show()

# Signal parameters
frequency = 1
sampling_rate = 1000
duration = 1
t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
t_degrees = 360 * t / duration

# Initial QAM setup
M = 16
I_values = Q_values = np.array([-3, -1, 1, 3])
binary_values = [f"{i:0{int(np.log2(M))}b}" for i in range(M)]
qam_signal, _ = qam_modulate(I_values, Q_values, binary_values)

# Create main figure and subplots
fig, (ax_const, ax_waves) = plt.subplots(1, 2, figsize=(15, 7))
plt.subplots_adjust(left=0.1, right=0.9, bottom=0.25, top=0.9)

fig.patch.set_facecolor('white')
ax_const.set_facecolor('white')
ax_waves.set_facecolor('white')

# Constellation diagram setup
scatter = ax_const.scatter(np.real(qam_signal), np.imag(qam_signal), color='blue', zorder=5, picker=True)
highlighted_point = ax_const.scatter([], [], marker='o', color='red', s=100, zorder=10)
for i, (x, y) in enumerate(zip(np.real(qam_signal), np.imag(qam_signal))):
    ax_const.text(x, y + 0.2, binary_values[i], ha='center', va='center')

ax_const.set_title(f'{M}-QAM Constellation Diagram')
ax_const.set_xlim(-5, 5)
ax_const.set_ylim(-5, 5)
ax_const.set_xticks(np.arange(-5, 6, 1))
ax_const.set_yticks(np.arange(-5, 6, 1))
ax_const.axhline(0, color='lightgray', linestyle='-')
ax_const.axvline(0, color='lightgray', linestyle='-')
ax_const.grid(True)
ax_const.set_xlabel('In-Phase, I (Cosine))')
ax_const.set_ylabel('Quadrature, Q (Sine)')

# Add circles to the Constellation diagram
circle_radii = [np.sqrt(2), np.sqrt(10), np.sqrt(18)]
for radius in circle_radii:
    circle = plt.Circle((0, 0), radius, fill=False, linestyle='--', color='lightgray')
    ax_const.add_artist(circle)
    ax_const.text(-5.2, radius, f'r = {radius:.2f}', 
                  color='black', ha='right', va='center')

# Add radial lines to the Constellation diagram
for point in qam_signal:
    angle = np.angle(point)
    ax_const.plot([0, 5*np.cos(angle)], [0, 5*np.sin(angle)], 
                  linestyle='--', color='lightgray', zorder=1)

# Waveform plot setup
line1, = ax_waves.plot(t_degrees, np.zeros_like(t), 'r', label='Sine (Q)')
line2, = ax_waves.plot(t_degrees, np.zeros_like(t), 'g', label='Cosine (I)')
line3, = ax_waves.plot(t_degrees, np.zeros_like(t), 'b', label='Combination')

ax_waves.set_title('Waveforms')
ax_waves.set_xlim(0, 360)
ax_waves.set_ylim(-5, 5)
ax_waves.set_xlabel('Angle')
ax_waves.set_xticks(np.arange(0, 360 + 90, 90))
ax_waves.set_xticklabels([f'{int(tick)}°' for tick in np.arange(0, 360 + 90, 90)])
ax_waves.axvline(180, color='grey', linestyle='--')
ax_waves.grid(which='both', linestyle='--')
ax_waves.set_yticks(np.arange(-5, 6, 1))
ax_waves.legend()

# Sliders
axAmp1 = plt.axes([0.1, 0.15, 0.3, 0.03])
sAmp1 = Slider(axAmp1, 'Sine Amplitude (Q)', -3, 3, valinit=1, valstep=0.1, valfmt='%1.1f')

axAmp2 = plt.axes([0.1, 0.1, 0.3, 0.03])
sAmp2 = Slider(axAmp2, 'Cosine Amplitude (I)', -3, 3, valinit=1, valstep=0.1, valfmt='%1.1f')

axNoise = plt.axes([0.55, 0.1, 0.35, 0.03])
sNoise = Slider(axNoise, 'Noise Level', 0, 1, valinit=0.05, valstep=0.01, valfmt='%1.2f')

# Text elements
evm_text = ax_waves.text(0.02, 0.95, f"EVM: {0:.2f}%", ha='left', va='top', transform=ax_waves.transAxes)
amp_phase_text = ax_waves.text(0.02, 0.85, f"Amplitude: {0:.2f}\nPhase: {0:.2f}°", ha='left', va='top', transform=ax_waves.transAxes)
ber_text = ax_waves.text(0.02, 0.75, f"BER: {0:.2e}", ha='left', va='top', transform=ax_waves.transAxes)

# Radio buttons for modulation selection (moved to bottom, horizontal orientation)
rax = plt.axes([0.3, 0.02, 0.4, 0.04])
radio = RadioButtons(rax, ('2-BPSK', '4-QPSK', '16-QAM'), active=2)

# Radio buttons for modulation selection (moved to bottom, horizontal orientation)
rax = plt.axes([0.3, 0.02, 0.4, 0.04])
radio = RadioButtons(rax, ('2-BPSK', '4-QPSK', '16-QAM'), active=2)

# Adjust radio button layout to be horizontal
radio_circles = [child for child in radio.ax.get_children() if isinstance(child, plt.Circle)]
radio_labels = radio.labels

for i, (circle, label) in enumerate(zip(radio_circles, radio_labels)):
    circle.set_radius(0.08)
    circle.center = (0.1 + i * 0.3, 0.5)
    label.set_position((circle.center[0] + 0.1, circle.center[1]))
    label.set_horizontalalignment('left')

# Tutorial button (moved to bottom, next to radio buttons)
tutorial_ax = plt.axes([0.72, 0.02, 0.1, 0.04])
tutorial_button = Button(tutorial_ax, 'Tutorial')
tutorial_button.on_clicked(lambda x: show_tutorial())

# Event connections
sAmp1.on_changed(update_plot)
sAmp2.on_changed(update_plot)
fig.canvas.mpl_connect('pick_event', on_pick)
fig.canvas.mpl_connect('motion_notify_event', hover)
radio.on_clicked(change_modulation)

# Global variables
A, B = 1, 1

# Animation
anim = FuncAnimation(fig, animate, frames=None, interval=50, blit=False, cache_frame_data=False)
anim.event_source.start()

# Initial plot update
update_plot(None)

plt.show()
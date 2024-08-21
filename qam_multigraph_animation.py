import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from matplotlib.animation import FuncAnimation

def qam_modulate(I_values, Q_values, binary_values):
    X, Y = np.meshgrid(I_values, Q_values)
    X = X.flatten()
    Y = Y.flatten()
    return X + 1j * Y

def calculate_evm(signal, ideal_signal):
    error = signal - ideal_signal
    rms_error = np.sqrt(np.mean(np.abs(error) ** 2))
    rms_signal = np.sqrt(np.mean(np.abs(ideal_signal) ** 2))
    if rms_signal != 0:
        evm = (rms_error / rms_signal) * 100
    else:
        evm = 0
    return evm

def update_waveforms(A, B):
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

    fig.canvas.draw_idle()

def update_plot(val):
    global A, B
    A = round(sAmp1.val, 1)  # Sine amplitude
    B = round(sAmp2.val, 1)  # Cosine amplitude
    update_waveforms(A, B)

def reset_sliders(event):
    sAmp1.reset()
    sAmp2.reset()
    sNoise.reset()
    update_plot(None)

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
            ax_const.set_title('16-QAM Constellation Diagram (Hovering)', color='red')
        else:
            ax_const.set_title('16-QAM Constellation Diagram', color='black')
        fig.canvas.draw_idle()

def toggle_noise(label):
    if noise_checkbox.get_status()[0]:
        anim.event_source.start()
    else:
        anim.event_source.stop()
        update_plot(None)

def animate(frame):
    if noise_checkbox.get_status()[0]:
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
        
        fig.canvas.draw_idle()
    
    return [highlighted_point, line1, line2, line3, evm_text, amp_phase_text]

# Define the parameters
frequency = 1
sampling_rate = 1000
duration = 1
t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)
t_degrees = 360 * t / duration

# I and Q values for 16-QAM constellation
I_values = np.array([-3, -1, 1, 3])
Q_values = np.array([-3, -1, 1, 3])
binary_values = [f"{i:04b}" for i in range(16)]

# Create 16-QAM constellation points
qam_signal = qam_modulate(I_values, Q_values, binary_values)

# Create the figure and axes
fig, (ax_const, ax_waves) = plt.subplots(1, 2, figsize=(12, 5))
plt.subplots_adjust(left=0.1, right=0.9, bottom=0.3, top=0.9)

# Set the background color explicitly
fig.patch.set_facecolor('white')
ax_const.set_facecolor('white')
ax_waves.set_facecolor('white')

# Configure the constellation diagram
scatter = ax_const.scatter(np.real(qam_signal), np.imag(qam_signal), color='blue', zorder=5, picker=True)
highlighted_point = ax_const.scatter([], [], marker='o', color='red', s=100, zorder=10)
for i, (x, y) in enumerate(zip(np.real(qam_signal), np.imag(qam_signal))):
    ax_const.text(x, y + 0.2, binary_values[i], ha='center', va='center')

# Add circles to the Constellation diagram
circle_radii = [np.sqrt(2), np.sqrt(10), np.sqrt(18)]
for radius in circle_radii:
    circle = plt.Circle((0, 0), radius, fill=False, linestyle='--', color='lightgray')
    ax_const.add_artist(circle)
    ax_const.text(0, radius + 0.2, f'r = {radius:.2f}', 
                  color='lightgray', ha='center', va='bottom')

# Add radial lines to the Constellation diagram
for point in qam_signal:
    angle = np.angle(point)
    ax_const.plot([0, 5*np.cos(angle)], [0, 5*np.sin(angle)], 
                  linestyle='--', color='lightgray', zorder=1)

ax_const.set_title('16-QAM Constellation Diagram')
ax_const.set_xlim(-5, 5)
ax_const.set_ylim(-5, 5)
ax_const.set_xticks(np.arange(-5, 6, 1))
ax_const.set_yticks(np.arange(-5, 6, 1))
ax_const.axhline(0, color='black', linestyle='--')
ax_const.axvline(0, color='black', linestyle='--')
ax_const.grid(True)

# Add labels for In-Phase (I) and Quadrature (Q)
ax_const.set_xlabel('In-Phase (I)')
ax_const.set_ylabel('Quadrature (Q)')

# Initialize lines for sine, cosine, and resultant waveform
line1, = ax_waves.plot(t_degrees, np.zeros_like(t), 'r', label='Sine (Q)')
line2, = ax_waves.plot(t_degrees, np.zeros_like(t), 'g', label='Cosine (I)')
line3, = ax_waves.plot(t_degrees, np.zeros_like(t), 'b', label='Combination')

# Configure the waveform plot
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

# Create horizontal sliders
axcolor = 'lightgoldenrodyellow'
axAmp1 = plt.axes([0.1, 0.2, 0.3, 0.03], facecolor=axcolor)
axAmp2 = plt.axes([0.55, 0.2, 0.3, 0.03], facecolor=axcolor)
axNoise = plt.axes([0.1, 0.15, 0.75, 0.03], facecolor=axcolor)
sAmp1 = Slider(axAmp1, 'Sine Amplitude', -3, 3, valinit=1, valstep=0.1, valfmt='%1.1f')
sAmp2 = Slider(axAmp2, 'Cosine Amplitude', -3, 3, valinit=1, valstep=0.1, valfmt='%1.1f')
sNoise = Slider(axNoise, 'Noise Level', 0, 1, valinit=0.05, valstep=0.01, valfmt='%1.2f')

# Create a reset button
resetax = plt.axes([0.8, 0.05, 0.1, 0.04])
reset_button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
reset_button.on_clicked(reset_sliders)

# Create a checkbox for noise
noise_ax = plt.axes([0.1, 0.05, 0.15, 0.05])
noise_checkbox = CheckButtons(noise_ax, ['Add Noise'], [True])
noise_checkbox.on_clicked(toggle_noise)

# Add EVM text
evm_text = ax_waves.text(0.02, 0.95, f"EVM: {0:.2f}%", ha='left', va='top', transform=ax_waves.transAxes)

# Add Amplitude and Phase text
amp_phase_text = ax_waves.text(0.02, 0.85, f"Amplitude: {0:.2f}\nPhase: {0:.2f}°", ha='left', va='top', transform=ax_waves.transAxes)

# Connect event handlers
sAmp1.on_changed(update_plot)
sAmp2.on_changed(update_plot)
fig.canvas.mpl_connect('pick_event', on_pick)
fig.canvas.mpl_connect('motion_notify_event', hover)

# Global variables for current amplitudes
A, B = 1, 1  # Initial values

# Create animation
anim = FuncAnimation(fig, animate, frames=None, interval=500, blit=False, cache_frame_data=False)
# Start with animation running (noise on)
anim.event_source.start()

# Initial plot update
update_plot(None)

# Display the plot
plt.show()
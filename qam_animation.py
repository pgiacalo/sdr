import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Define the parameters
frequency = 1  # Frequency of the waveforms in Hz
sampling_rate = 1000  # Sampling rate
duration = 1  # Duration in seconds to ensure one cycle

# Time vector for one cycle
t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)  # Time vector
t_degrees = 360 * t / duration  # Convert time to degrees

# Create the figure and axes
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
plt.subplots_adjust(left=0.25, bottom=0.1, top=0.9, hspace=0.5)

# Initialize lines for sine wave, cosine wave, and resultant waveform
line1, = ax1.plot(t_degrees, np.zeros_like(t), 'r')
line2, = ax2.plot(t_degrees, np.zeros_like(t), 'g')
line3, = ax3.plot(t_degrees, np.zeros_like(t), 'b')

# Set the axis labels and limits uniformly
ax1.set_title('Sine Wave (Q component)')
ax2.set_title('Cosine Wave (I component)')
ax3.set_title('Resultant Waveform')
for ax in [ax1, ax2, ax3]:
    ax.set_xlim(0, 360)
    ax.set_ylim(-4, 4)
    ax.set_xlabel('Time (degrees)')

# Set x-ticks to be in increments of 90 degrees and add a vertical line at 180 degrees
ticks = np.arange(0, 360 + 90, 90)
tick_labels = [f'{int(tick)}°' for tick in ticks]
for ax in [ax1, ax2, ax3]:
    ax.set_xticks(ticks)
    ax.set_xticklabels(tick_labels)
    ax.axvline(180, color='grey', linestyle='--', linewidth=0.5)  # Vertical line at 180 degrees

# Add horizontal grid lines at every integer value
for ax in [ax1, ax2, ax3]:
    ax.set_yticks(np.arange(-4, 5, 1))  # Horizontal lines at each integer from -4 to 4
    ax.grid(which='both', linestyle='--', linewidth=0.5, color='grey')

# Create sliders to the left of the graphs
axcolor = 'lightgoldenrodyellow'
axAmp1 = plt.axes([0.1, 0.05, 0.1, 0.03], facecolor=axcolor)
axAmp2 = plt.axes([0.1, 0.1, 0.1, 0.03], facecolor=axcolor)

sAmp1 = Slider(axAmp1, 'Amp Sine', -3, 3, valinit=0, valstep=0.1, valfmt='%1.1f')
sAmp2 = Slider(axAmp2, 'Amp Cosine', -3, 3, valinit=0, valstep=0.1, valfmt='%1.1f')

# Phase angle text display
info_text = ax3.text(0.05, 0.85, '', transform=ax3.transAxes)

# Update function
def update(val):
    A = round(sAmp1.val, 1)  # Round to nearest 0.1
    B = round(sAmp2.val, 1)  # Round to nearest 0.1
    
    # Generate the waveforms
    sine_wave = A * np.sin(2 * np.pi * frequency * t)
    cosine_wave = B * np.cos(2 * np.pi * frequency * t)
    resultant_waveform = sine_wave + cosine_wave
    
    # Update the lines
    line1.set_ydata(sine_wave)
    line2.set_ydata(cosine_wave)
    line3.set_ydata(resultant_waveform)
    
    # Compute amplitude and phase angle of the resultant waveform
    amplitude = np.sqrt(A**2 + B**2)
    phase_angle = np.arctan2(B, A) * 180 / np.pi  # Convert radians to degrees
    
    # Update text display
    info_text.set_text(f'Amplitude: {amplitude:.2f}, Phase Angle: {phase_angle:.2f}°')
    
    fig.canvas.draw_idle()

# Call update function on slider value change
sAmp1.on_changed(update)
sAmp2.on_changed(update)

# Initial plot update
update(None)

# Display the plot
plt.show()

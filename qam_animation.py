import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Define the parameters
frequency = 1  # Frequency of the waveforms in Hz
sampling_rate = 1000  # Sampling rate
duration = 2  # Duration in seconds to ensure two cycles

# Time vector for two cycles
t = np.linspace(0, duration, duration * sampling_rate)  # Time vector
t_degrees = 360 * t / duration  # Convert time to degrees

# Create the figure and axes
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
plt.subplots_adjust(left=0.1, bottom=0.35)

# Initialize lines for sine wave, cosine wave, and resultant waveform
line1, = ax1.plot(t_degrees, np.zeros_like(t), 'r')
line2, = ax2.plot(t_degrees, np.zeros_like(t), 'g')
line3, = ax3.plot(t_degrees, np.zeros_like(t), 'b')

# Set the axis labels and limits
ax1.set_title('Sine Wave (Q component)')
ax2.set_title('Cosine Wave (I component)')
ax3.set_title('Resultant Waveform')
ax1.set_xlim(0, 720)
ax2.set_xlim(0, 720)
ax3.set_xlim(0, 720)
ax1.set_ylim(-2, 2)
ax2.set_ylim(-2, 2)
ax3.set_ylim(-3, 3)
ax1.set_xlabel('Time (degrees)')
ax2.set_xlabel('Time (degrees)')
ax3.set_xlabel('Time (degrees)')

# Set x-ticks to be in increments of 90 degrees
ticks = np.arange(0, 720 + 90, 90)
tick_labels = [f'{int(tick)}°' for tick in ticks]
ax1.set_xticks(ticks)
ax1.set_xticklabels(tick_labels)
ax2.set_xticks(ticks)
ax2.set_xticklabels(tick_labels)
ax3.set_xticks(ticks)
ax3.set_xticklabels(tick_labels)

# Create sliders
axcolor = 'lightgoldenrodyellow'
axAmp1 = plt.axes([0.1, 0.2, 0.8, 0.03], facecolor=axcolor)
axAmp2 = plt.axes([0.1, 0.25, 0.8, 0.03], facecolor=axcolor)

sAmp1 = Slider(axAmp1, 'Amp Sine', -2.0, 2.0, valinit=1.0)
sAmp2 = Slider(axAmp2, 'Amp Cosine', -2.0, 2.0, valinit=1.0)

# Half-cycle points
half_cycle_points = [180, 540]  # degrees corresponding to half-cycles

# Phase angle text display
phase_text = ax3.text(0.05, 0.85, '', transform=ax3.transAxes)

# Update function
def update(val):
    A = sAmp1.val
    B = sAmp2.val
    
    # Generate the waveforms
    sine_wave = A * np.sin(2 * np.pi * frequency * t)
    cosine_wave = B * np.cos(2 * np.pi * frequency * t)
    resultant_waveform = sine_wave + cosine_wave
    
    # Update the lines
    line1.set_ydata(sine_wave)
    line2.set_ydata(cosine_wave)
    line3.set_ydata(resultant_waveform)
    
    # Clear and plot half-cycle markers
    for ax in [ax1, ax2, ax3]:
        # Clear previous half-cycle markers
        for line in ax.lines[1:]:
            line.remove()
        # Plot new half-cycle markers
        for hcp in half_cycle_points:
            ax.axvline(hcp, color='k', linestyle='--', linewidth=0.5)
    
    # Calculate and display the phase angle
    phase_angle = np.arctan2(B, A) * 180 / np.pi  # Convert radians to degrees
    phase_text.set_text(f'Phase Angle: {phase_angle:.2f}°')
    
    fig.canvas.draw_idle()

# Call update function on slider value change
sAmp1.on_changed(update)
sAmp2.on_changed(update)

# Initial plot update
update(None)

# Display the plot
plt.show()

# In Quadrature Amplitude Modulation (QAM), the digital input signal is multiplied by 
# the sine and cosine waveforms. This multiplication is key to how QAM encodes data 
# onto the carrier signal.

# How QAM Works:
# 1. Digital Signal Preparation:
#    - The digital data intended for transmission is first processed into two separate streams: one for the In-phase (I)
#      component and one for the Quadrature (Q) component. These streams represent digital values that determine the
#      amplitude levels of the respective I and Q signals.

# 2. Modulation Process:
#    - Each stream (I and Q) modulates a carrier waveform: the I component modulates a cosine wave (cos(ωt)), and the
#      Q component modulates a sine wave (sin(ωt)). The term "quadrature" refers to the fact that these two carrier signals
#      are 90 degrees out of phase with each other.
#    - The modulation is achieved by multiplying the digital signal values (amplitude information) from each stream with
#      their respective carrier waveforms. This multiplication adjusts the amplitude of the sine and cosine waves
#      according to the digital values.

# 3. Combination of I and Q Components:
#    - After the modulation step, the I and Q components are summed (added together) to form the final QAM signal. This
#      summing results in a signal where both amplitude and phase vary, allowing it to carry more information per symbol
#      compared to simpler modulation schemes like QPSK.

# Mathematical Representation:
# The final QAM signal can be mathematically represented as:
# S(t) = I(t) * cos(ωt) + Q(t) * sin(ωt)
# where:
#   S(t) is the QAM signal.
#   I(t) is the in-phase component (modulating the cosine wave).
#   Q(t) is the quadrature component (modulating the sine wave).
#   ωt represents the angular frequency of the carrier wave.

# Summary:
# The digital inputs (I and Q components) in QAM are multiplied by their respective carrier waveforms to modulate the amplitude
# of these waves. The resulting modulated signals are then added together to produce the composite QAM signal that is transmitted.
# This process allows QAM to effectively utilize both amplitude and phase variations to encode data, leading to higher data rates
# compared to other modulation schemes.

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

# Create the figure and axes for the waveforms
fig, axes = plt.subplots(3, 1, figsize=(10, 8), gridspec_kw={'width_ratios': [1]})
plt.subplots_adjust(left=0.3, bottom=0.1, top=0.9, hspace=0.5)

# Initialize lines for sine wave, cosine wave, and resultant waveform
line1, = axes[0].plot(t_degrees, np.zeros_like(t), 'r')
line2, = axes[1].plot(t_degrees, np.zeros_like(t), 'g')
line3, = axes[2].plot(t_degrees, np.zeros_like(t), 'b')

# Set the axis labels and limits uniformly
axes[0].set_title('Sine Wave (Q component)')
axes[1].set_title('Cosine Wave (I component)')
axes[2].set_title('Resultant Waveform')
for ax in axes:
    ax.set_xlim(0, 360)
    ax.set_ylim(-5, 5)
    ax.set_xlabel('Time (degrees)')

# Set x-ticks to be in increments of 90 degrees and add a vertical line at 180 degrees
ticks = np.arange(0, 360 + 90, 90)
tick_labels = [f'{int(tick)}°' for tick in ticks]
for ax in axes:
    ax.set_xticks(ticks)
    ax.set_xticklabels(tick_labels)
    ax.axvline(180, color='grey', linestyle='--', linewidth=0.5)

# Add horizontal grid lines at every integer value
for ax in axes:
    ax.set_yticks(np.arange(-5, 6, 1))
    ax.grid(which='both', linestyle='--', linewidth=0.5, color='grey')

# Create vertical sliders next to each graph
axcolor = 'lightgoldenrodyellow'
axAmp1 = plt.axes([0.1, 0.7, 0.02, 0.2], facecolor=axcolor)  # Positioned correctly for sine
axAmp2 = plt.axes([0.1, 0.4, 0.02, 0.2], facecolor=axcolor)  # Positioned correctly for cosine

sAmp1 = Slider(axAmp1, 'Sine Amplitude', -3, 3, valinit=0, valstep=0.1, valfmt='%1.1f', orientation='vertical')
sAmp2 = Slider(axAmp2, 'Cosine Amplitude', -3, 3, valinit=0, valstep=0.1, valfmt='%1.1f', orientation='vertical')

# Phase angle text display
info_text = axes[2].text(0.05, 0.85, '', transform=axes[2].transAxes)

# Update function
def update(val):
    A = round(sAmp1.val, 1)  # Sine amplitude
    B = round(sAmp2.val, 1)  # Cosine amplitude
    
    # Generate the waveforms
    sine_wave = A * np.sin(2 * np.pi * frequency * t)
    cosine_wave = B * np.cos(2 * np.pi * frequency * t)
    resultant_waveform = sine_wave + cosine_wave
    
    # Update the lines
    line1.set_ydata(sine_wave)
    line2.set_ydata(cosine_wave)
    line3.set_ydata(resultant_waveform)
    
    # Calculate amplitude and phase angle
    amplitude = np.sqrt(A**2 + B**2)
    phase_angle = np.arctan2(A, B) * 180 / np.pi  # Corrected to atan2(A, B)
    
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

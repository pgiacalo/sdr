import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Define the parameters
frequency = 1  # Frequency of the waveforms in Hz
sampling_rate = 1000  # Sampling rate
duration = 1  # Duration in seconds to ensure one cycle
t = np.linspace(0, duration, int(duration * sampling_rate), endpoint=False)  # Time vector
t_degrees = 360 * t / duration  # Convert time to degrees

# I and Q values for 16-QAM constellation
I_values = np.array([-3, -1, 1, 3])
Q_values = np.array([-3, -1, 1, 3])
binary_values = [f"{i:04b}" for i in range(16)]  # Binary labels for the constellation points

# Create 16-QAM constellation points
X, Y = np.meshgrid(I_values, Q_values)
X = X.flatten()
Y = Y.flatten()

# Create the figure and axes for the waveforms and constellation diagram
fig, axes = plt.subplots(4, 2, figsize=(12, 10), gridspec_kw={'width_ratios': [1, 2], 'height_ratios': [1, 1, 1, 1]})
plt.subplots_adjust(left=0.3, bottom=0.1, top=0.9, hspace=0.5)

# Configure the constellation diagram in the upper left
ax_const = axes[0, 0]
scatter = ax_const.scatter(X, Y, color='blue', zorder=5)  # Static constellation points
highlighted_point = ax_const.scatter([], [], color='red', s=100, zorder=10)  # Moving red dot
for i, (x, y) in enumerate(zip(X, Y)):
    ax_const.text(x, y + 0.2, binary_values[i], ha='center', va='center')
ax_const.set_title('16-QAM Constellation Diagram')
ax_const.set_xlim(-4, 4)
ax_const.set_ylim(-4, 4)
ax_const.set_xticks(np.arange(-4, 5, 1))
ax_const.set_yticks(np.arange(-4, 5, 1))
ax_const.axhline(0, color='black', linestyle='--')
ax_const.axvline(0, color='black', linestyle='--')
ax_const.grid(True)

# Initialize lines for sine wave, cosine wave, and resultant waveform
line1, = axes[0, 1].plot(t_degrees, np.zeros_like(t), 'r')
line2, = axes[1, 1].plot(t_degrees, np.zeros_like(t), 'g')
line3, = axes[2, 1].plot(t_degrees, np.zeros_like(t), 'b')

# Set the axis labels and limits uniformly for waveforms
titles = ['Sine Wave (Q component)', 'Cosine Wave (I component)', 'Resultant Waveform']
for ax, title in zip(axes[:3, 1], titles):
    ax.set_title(title)
    ax.set_xlim(0, 360)
    ax.set_ylim(-4, 4)
    ax.set_xlabel('Time (degrees)')
    ax.set_xticks(np.arange(0, 360 + 90, 90))
    ax.set_xticklabels([f'{int(tick)}°' for tick in np.arange(0, 360 + 90, 90)])
    ax.axvline(180, color='grey', linestyle='--')
    ax.grid(which='both', linestyle='--')
    ax.set_yticks(np.arange(-4, 5, 1))  # Match y-axis ticks with the constellation diagram

# Create vertical sliders next to the sine and cosine graphs
axcolor = 'lightgoldenrodyellow'
axAmp1 = plt.axes([0.1, 0.7, 0.02, 0.2], facecolor=axcolor)
axAmp2 = plt.axes([0.1, 0.4, 0.02, 0.2], facecolor=axcolor)

sAmp1 = Slider(axAmp1, 'Sine Amplitude', -3, 3, valinit=0, valstep=0.1, valfmt='%1.1f', orientation='vertical')
sAmp2 = Slider(axAmp2, 'Cosine Amplitude', -3, 3, valinit=0, valstep=0.1, valfmt='%1.1f', orientation='vertical')

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
    
    # Update the red dot on the constellation diagram
    highlighted_point.set_offsets([[B, A]])
    
    fig.canvas.draw_idle()

# Call update function on slider value change
sAmp1.on_changed(update)
sAmp2.on_changed(update)

# Initial plot update
update(None)

# Display the plot
plt.show()

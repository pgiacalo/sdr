import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define the I and Q values for 16-QAM
I_values_new = [-3, -1, 1, 3, -3, -1, 1, 3, -3, -1, 1, 3, -3, -1, 1, 3]
Q_values_new = [-3, -3, -3, -3, -1, -1, -1, -1,  1,  1,  1,  1,  3,  3, 3,  3]

# Decimal values from 0 to 15
decimal_values = list(range(16))

# Prompt user for the carrier frequency, constellation point, and noise inclusion
carrier_frequency = float(input("Enter the carrier frequency (Hz): "))
x_input, y_input = map(int, input("Enter the constellation point as x,y (e.g., 3,-1): ").split(','))
include_noise = input("Include noise in the animation? (yes/no): ").strip().lower() == 'yes'

# Calculate the initial phase angle (before noise)
phase_angle = np.arctan2(y_input, x_input)
phase_angle_deg = np.degrees(phase_angle)
if phase_angle_deg < 0:
    phase_angle_deg += 360

# Set up the figure and the axis
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Draw the initial constellation diagram on the left subplot (ax1)
scatter = ax1.scatter(I_values_new, Q_values_new, c='blue')
highlighted_point = ax1.scatter([], [], c='red')  # Highlighted point placeholder, bright red

# Annotate each point with its decimal value, and highlight the chosen point in green
for i, (x, y) in enumerate(zip(I_values_new, Q_values_new)):
    color = 'green' if (x == x_input and y == y_input) else 'blue'
    ax1.text(x, y, str(decimal_values[i]), fontsize=12, ha='center', va='center', color='white',
             bbox=dict(facecolor=color, alpha=0.5))  # Green box for the selected point

# Draw and label amplitude circles
circle_radii = [np.sqrt(2), np.sqrt(10), np.sqrt(18)]
for radius in circle_radii:
    circle = plt.Circle((0, 0), radius, fill=False, color='gray', linestyle='--')
    ax1.add_artist(circle)
    if radius == np.sqrt(18):
        ax1.text(0, radius, '√18', fontsize=10, ha='center', va='bottom', color='black')
    elif radius == np.sqrt(10):
        ax1.text(0, radius, '√10', fontsize=10, ha='center', va='bottom', color='black')
    elif radius == np.sqrt(2):
        ax1.text(0, radius, '√2', fontsize=10, ha='center', va='bottom', color='black')

# Draw radial lines for the phase angles through each point
max_radius = np.sqrt(18)
angles = np.arctan2(Q_values_new, I_values_new)
unique_angles = np.unique(angles)
for angle in unique_angles:
    x = [0, max_radius * np.cos(angle)]
    y = [0, max_radius * np.sin(angle)]
    ax1.plot(x, y, color='gray', linestyle='--', linewidth=1, zorder=1)

# Adjust title placement and axis limits
ax1.set_title('16-QAM Constellation Diagram', fontsize=16, y=1.05)
ax1.set_xlabel('In-phase (I)')
ax1.set_ylabel('Quadrature (Q)')
ax1.grid(True)
ax1.set_xlim(-4.5, 4.5)
ax1.set_ylim(-4.5, 4.5)
ax1.axhline(0, color='black', linewidth=0.5)
ax1.axvline(0, color='black', linewidth=0.5)
ax1.set_aspect('equal', adjustable='box')

# Set up the waveform plot on the right subplot (ax2)
line, = ax2.plot([], [], lw=2)

# Set up the axis limits and labels
ax2.set_xlim(0, 1)
ax2.set_ylim(-np.sqrt(18) - 1, np.sqrt(18) + 1)
ax2.set_title(f'Waveform for Constellation Point ({x_input},{y_input})')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Amplitude')

# Add tick marks and labels for sqrt(2), sqrt(10), sqrt(18), and their negatives
y_ticks = [-np.sqrt(18), -np.sqrt(10), -np.sqrt(2), 0, np.sqrt(2), np.sqrt(10), np.sqrt(18)]
y_tick_labels = ['-√18', '-√10', '-√2', '0', '√2', '√10', '√18']
ax2.set_yticks(y_ticks)
ax2.set_yticklabels(y_tick_labels)

# Draw light gray dashed lines for these tick marks
for y in y_ticks:
    ax2.axhline(y, color='lightgray', linestyle='--')

# Generate time array
t = np.linspace(0, 1, 1000)  # 1 second of time

# Animation update function
def update(frame):
    # Introduce a small amount of Gaussian noise if the user chose to include noise
    noise_std = 0.1 if include_noise else 0
    I_noisy = x_input + np.random.normal(0, noise_std)
    Q_noisy = y_input + np.random.normal(0, noise_std)
    
    # Update the highlighted point on the constellation diagram
    highlighted_point.set_offsets([[I_noisy, Q_noisy]])

    # Calculate the new waveform with noise
    amplitude = np.sqrt(I_noisy**2 + Q_noisy**2)
    phase_angle_noisy = np.arctan2(Q_noisy, I_noisy)
    phase_angle_deg_noisy = np.degrees(phase_angle_noisy)
    if phase_angle_deg_noisy < 0:
        phase_angle_deg_noisy += 360

    waveform = amplitude * np.cos(2 * np.pi * carrier_frequency * t + np.radians(phase_angle_deg_noisy))
    
    # Update the waveform plot
    line.set_data(t, waveform)
    
    # Clear previous text annotations
    for text in ax2.texts:
        text.remove()

    # Update the note with the phase angle before noise is applied
    note_text = (f'Carrier Frequency: {carrier_frequency} Hz\n'
                 f'Phase Angle (before noise): {phase_angle_deg:.2f}°')
    ax2.text(0.95, 0.95, note_text, transform=ax2.transAxes,
             fontsize=12, verticalalignment='top', horizontalalignment='right',
             bbox=dict(facecolor='white', alpha=0.5))
    
    return line, highlighted_point

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=range(100), blit=True, interval=1000, repeat=False)

plt.tight_layout()
plt.show()

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define the I and Q values for 16-QAM
I_values_new = [-3, -1, 1, 3, -3, -1, 1, 3, -3, -1, 1, 3, -3, -1, 1, 3]
Q_values_new = [-3, -3, -3, -3, -1, -1, -1, -1,  1,  1,  1,  1,  3,  3, 3,  3]

# Decimal values from 0 to 15
decimal_values = list(range(16))

# Convert decimal values to binary strings (4 bits)
binary_values = [f'{val:04b}' for val in decimal_values]

# Prompt user for the carrier frequency and noise inclusion
carrier_frequency = float(input("Enter the carrier frequency (Hz): "))

# Updated prompt handling for noise inclusion
include_noise = input("Include noise in the animation? (yes/no): ").strip().lower() in ['y', 'yes']

# Set up the figure and the axis
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Draw the initial constellation diagram on the left subplot (ax1)
scatter = ax1.scatter(I_values_new, Q_values_new, c='blue')
highlighted_point = ax1.scatter([], [], c='red', zorder=5)  # Bring the red dot to the front with a high zorder
selected_point = None  # To keep track of the selected point

# Annotate each point with its decimal value and binary pattern
annotations = []
for i, (x, y) in enumerate(zip(I_values_new, Q_values_new)):
    # Decimal value annotation
    annotation = ax1.text(x, y, str(decimal_values[i]), fontsize=12, ha='center', va='center', color='white',
                          bbox=dict(facecolor='blue', alpha=0.5))  # Blue box for each point
    annotations.append(annotation)
    
    # Binary pattern annotation (displayed just below the decimal value)
    ax1.text(x, y - 0.5, binary_values[i], fontsize=10, ha='center', va='center', color='black')

# Draw and label amplitude circles
circle_radii = [np.sqrt(2), np.sqrt(10), np.sqrt(18)]
for radius in circle_radii:
    circle = plt.Circle((0, 0), radius, fill=False, color='gray', linestyle='--', zorder=1)
    ax1.add_artist(circle)
    if radius == np.sqrt(18):
        ax1.text(0, radius, '√18', fontsize=10, ha='center', va='bottom', color='black', zorder=2)
    elif radius == np.sqrt(10):
        ax1.text(0, radius, '√10', fontsize=10, ha='center', va='bottom', color='black', zorder=2)
    elif radius == np.sqrt(2):
        ax1.text(0, radius, '√2', fontsize=10, ha='center', va='bottom', color='black', zorder=2)

# Draw radial lines for the phase angles through each point
max_radius = np.sqrt(18)
angles = np.arctan2(Q_values_new, I_values_new)
unique_angles = np.unique(angles)
for angle in unique_angles:
    x = [0, max_radius * np.cos(angle)]
    y = [0, max_radius * np.sin(angle)]
    ax1.plot(x, y, color='gray', linestyle='--', linewidth=1, zorder=1)

# Adjust title placement and axis limits
ax1.set_title('16-QAM Constellation Diagram (Click a Point)', fontsize=16, y=1.05)
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

# Initialize variables to store the current I and Q values
current_I = None
current_Q = None
current_phase_angle_deg = None

# Generate time array
t = np.linspace(0, 1, 1000)  # 1 second of time

# Animation update function
def update(frame):
    if current_I is not None and current_Q is not None:
        # Introduce a small amount of Gaussian noise
        noise_std = 0.1 if include_noise else 0
        I_noisy = current_I + np.random.normal(0, noise_std)
        Q_noisy = current_Q + np.random.normal(0, noise_std)
        
        # Update the highlighted point on the constellation diagram
        highlighted_point.set_offsets([[I_noisy, Q_noisy]])

        # Calculate the new waveform with noise
        amplitude = np.sqrt(I_noisy**2 + Q_noisy**2)
        waveform = amplitude * np.cos(2 * np.pi * carrier_frequency * t + np.radians(current_phase_angle_deg))
        
        # Update the waveform plot
        line.set_data(t, waveform)

        # Update the note with the phase angle before noise is applied
        note_text = (f'Carrier Frequency: {carrier_frequency} Hz\n'
                     f'Phase Angle (before noise): {current_phase_angle_deg:.2f}°')
        if len(ax2.texts) > 0:
            ax2.texts[0].set_text(note_text)
        else:
            ax2.text(0.95, 0.95, note_text, transform=ax2.transAxes,
                     fontsize=12, verticalalignment='top', horizontalalignment='right',
                     bbox=dict(facecolor='white', alpha=0.5))
        
        # Update the title of the waveform plot
        ax2.set_title(f'Waveform for Constellation Point ({current_I},{current_Q})')
        
    return line, highlighted_point

# Function to handle mouse clicks
def on_click(event):
    global current_I, current_Q, current_phase_angle_deg, selected_point

    # Check if the click was inside the constellation diagram
    if event.inaxes == ax1:
        # Find the closest constellation point to the click
        click_x = event.xdata
        click_y = event.ydata
        min_dist = float('inf')
        for i, (x, y) in enumerate(zip(I_values_new, Q_values_new)):
            dist = np.sqrt((click_x - x) ** 2 + (click_y - y) ** 2)
            if dist < min_dist:
                min_dist = dist
                current_I = x
                current_Q = y
                selected_point = i

        # Update the phase angle (before noise) based on the selected point
        current_phase_angle_deg = np.degrees(np.arctan2(current_Q, current_I))
        if current_phase_angle_deg < 0:
            current_phase_angle_deg += 360

        # Highlight the selected point with a green box
        for i, annotation in enumerate(annotations):
            if i == selected_point:
                annotation.set_bbox(dict(facecolor='green', alpha=0.5))
            else:
                annotation.set_bbox(dict(facecolor='blue', alpha=0.5))

        # Update the title and note immediately after clicking
        ax2.set_title(f'Waveform for Constellation Point ({current_I},{current_Q})')
        note_text = (f'Carrier Frequency: {carrier_frequency} Hz\n'
                     f'Phase Angle (before noise): {current_phase_angle_deg:.2f}°')
        if len(ax2.texts) > 0:
            ax2.texts[0].set_text(note_text)
        else:
            ax2.text(0.95, 0.95, note_text, transform=ax2.transAxes,
                     fontsize=12, verticalalignment='top', horizontalalignment='right',
                     bbox=dict(facecolor='white', alpha=0.5))

# Connect the click event to the on_click function
fig.canvas.mpl_connect('button_press_event', on_click)

# Create the animation to run indefinitely
ani = animation.FuncAnimation(fig, update, frames=lambda: iter(int, 1), interval=1000, repeat=False)

plt.tight_layout()
plt.show()

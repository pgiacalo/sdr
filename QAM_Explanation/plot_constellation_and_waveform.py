import numpy as np
import matplotlib.pyplot as plt

# Define the I and Q values for 16-QAM
I_values_new = [-3, -1, 1, 3, -3, -1, 1, 3, -3, -1, 1, 3, -3, -1, 1, 3]
Q_values_new = [-3, -3, -3, -3, -1, -1, -1, -1,  1,  1,  1,  1,  3,  3, 3,  3]

# Decimal values from 0 to 15
decimal_values = list(range(16))

# Prompt user for the carrier frequency and constellation point
carrier_frequency = float(input("Enter the carrier frequency (Hz): "))
x_input, y_input = map(int, input("Enter the constellation point as x,y (e.g., 3,-1): ").split(','))

# Create a figure with two subplots side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Plot the 16-QAM constellation diagram on the left subplot (ax1)
for i, (x, y) in enumerate(zip(I_values_new, Q_values_new)):
    color = 'green' if (x == x_input and y == y_input) else 'blue'
    ax1.scatter(x, y, c=color)
    ax1.text(x, y, str(decimal_values[i]), fontsize=12, ha='center', va='center', color='white', bbox=dict(facecolor=color, alpha=0.5))

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

# Find the phase angle corresponding to the point
if (x_input in I_values_new and y_input in Q_values_new):
    phase_angle = np.arctan2(y_input, x_input)
    
    # Ensure phase angle is positive
    phase_angle_deg = np.degrees(phase_angle)
    if phase_angle_deg < 0:
        phase_angle_deg += 360
    
    # Generate the waveform corresponding to the phase angle
    t = np.linspace(0, 1, 1000)  # 1 second of time
    amplitude = np.sqrt(x_input**2 + y_input**2)
    
    waveform = amplitude * np.cos(2 * np.pi * carrier_frequency * t + np.radians(phase_angle_deg))
    
    # Plot the waveform on the right subplot (ax2)
    ax2.plot(t, waveform)
    ax2.set_title(f'Waveform for Constellation Point ({x_input},{y_input})')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Amplitude')
    
    # Add tick marks and labels for sqrt(2), sqrt(10), sqrt(18), and their negatives
    y_ticks = [-np.sqrt(18), -np.sqrt(10), -np.sqrt(2), 0, np.sqrt(2), np.sqrt(10), np.sqrt(18)]
    y_tick_labels = ['-√18', '-√10', '-√2', '0', '√2', '√10', '√18']
    ax2.set_yticks(y_ticks)
    ax2.set_yticklabels(y_tick_labels)
    
    # Draw light gray dashed lines for these tick marks
    ax2.axhline(np.sqrt(2), color='lightgray', linestyle='--')
    ax2.axhline(np.sqrt(10), color='lightgray', linestyle='--')
    ax2.axhline(np.sqrt(18), color='lightgray', linestyle='--')
    ax2.axhline(-np.sqrt(2), color='lightgray', linestyle='--')
    ax2.axhline(-np.sqrt(10), color='lightgray', linestyle='--')
    ax2.axhline(-np.sqrt(18), color='lightgray', linestyle='--')
    ax2.axhline(0, color='black', linestyle='-', linewidth=1)
    
    # Add a note with the carrier frequency and phase angle
    note_text = (f'Carrier Frequency: {carrier_frequency} Hz\n'
                 f'Phase Angle: {phase_angle_deg:.2f}°')
    ax2.text(0.95, 0.95, note_text, transform=ax2.transAxes,
             fontsize=12, verticalalignment='top', horizontalalignment='right',
             bbox=dict(facecolor='white', alpha=0.5))
else:
    ax2.text(0.5, 0.5, 'Invalid point', fontsize=20, ha='center', va='center', color='red')

# Display both plots
plt.tight_layout()
plt.show()

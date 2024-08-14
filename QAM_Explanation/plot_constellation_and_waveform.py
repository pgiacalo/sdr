import numpy as np
import matplotlib.pyplot as plt

# Define the I and Q values for 16-QAM
I_values_new = [-3, -1, 1, 3, -3, -1, 1, 3, -3, -1, 1, 3, -3, -1, 1, 3]
Q_values_new = [-3, -3, -3, -3, -1, -1, -1, -1,  1,  1,  1,  1,  3,  3, 3,  3]

# Decimal values from 0 to 15
decimal_values = list(range(16))

# Create a figure with two subplots side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Plot the 16-QAM constellation diagram on the left subplot (ax1)
ax1.scatter(I_values_new, Q_values_new, c='blue')

# Annotate each point with its decimal value
for i, (x, y) in enumerate(zip(I_values_new, Q_values_new)):
    ax1.text(x, y, str(decimal_values[i]), fontsize=12, ha='center', va='center', color='white', bbox=dict(facecolor='blue', alpha=0.5))

# Draw and label amplitude circles
circle_radii = [np.sqrt(2), np.sqrt(10), np.sqrt(18)]  # Correctly use sqrt(18)
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

# Prompt user for the carrier frequency and constellation point
carrier_frequency = float(input("Enter the carrier frequency (Hz): "))
x_input, y_input = map(int, input("Enter the constellation point as x,y (e.g., 3,-1): ").split(','))

# Find the phase angle corresponding to the point
if (x_input in I_values_new and y_input in Q_values_new):
    phase_angle = np.arctan2(y_input, x_input)
    
    # Generate the waveform corresponding to the phase angle
    t = np.linspace(0, 1, 1000)  # 1 second of time
    amplitude = np.sqrt(x_input**2 + y_input**2)
    
    # Format amplitude as a square root if it matches certain values
    amplitude_squared = int(amplitude**2)
    if amplitude_squared in [2, 10, 18]:
        amplitude_sqrt = f'√{amplitude_squared}'
    else:
        amplitude_sqrt = f'{amplitude:.2f}'
    
    waveform = amplitude * np.cos(2 * np.pi * carrier_frequency * t + phase_angle)
    
    # Plot the waveform on the right subplot (ax2)
    ax2.plot(t, waveform)
    ax2.set_title(f'Waveform for Constellation Point ({x_input},{y_input})')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Amplitude')
    
    # Mark the amplitude axis at sqrt(2), sqrt(10), and sqrt(18)
    ax2.axhline(np.sqrt(2), color='red', linestyle='--', label='√2')
    ax2.axhline(np.sqrt(10), color='green', linestyle='--', label='√10')
    ax2.axhline(np.sqrt(18), color='blue', linestyle='--', label='√18')
    ax2.axhline(-np.sqrt(2), color='red', linestyle='--')
    ax2.axhline(-np.sqrt(10), color='green', linestyle='--')
    ax2.axhline(-np.sqrt(18), color='blue', linestyle='--')
    ax2.legend()

    # Add a note with the carrier frequency, amplitude, and phase angle
    note_text = (f'Carrier Frequency: {carrier_frequency} Hz\n'
                 f'Amplitude: {amplitude_sqrt}\n'
                 f'Phase Angle: {np.degrees(phase_angle):.2f}°')
    ax2.text(0.95, 0.95, note_text, transform=ax2.transAxes,
             fontsize=12, verticalalignment='top', horizontalalignment='right',
             bbox=dict(facecolor='white', alpha=0.5))
else:
    ax2.text(0.5, 0.5, 'Invalid point', fontsize=20, ha='center', va='center', color='red')

# Display both plots
plt.tight_layout()
plt.show()

import numpy as np
import matplotlib.pyplot as plt

# Create the figure and axis
fig, ax = plt.subplots(figsize=(12, 8))

# Generate x values for one complete cycle
x = np.linspace(0, 2*np.pi, 1000)

# Define the phase angles in radians
phases = [np.pi/4, 3*np.pi/4, 5*np.pi/4, 7*np.pi/4]  # 45°, 135°, 225°, 315°

# Plot each cosine wave
for i, phase in enumerate(phases):
    y = np.cos(x + phase)  # Note the '+' here instead of '-'
    ax.plot(x, y, label=f'{int(np.degrees(phase))}°')

# Customize the plot
ax.set_title('Cosine Waves with Different Phase Angles')
ax.set_xlabel('Angle (radians)')
ax.set_ylabel('Amplitude')
ax.set_xlim(0, 2*np.pi)
ax.set_ylim(-1.5, 1.5)
ax.grid(True)
ax.legend()

# Add vertical lines at key points
ax.axvline(x=0, color='k', linestyle='--', alpha=0.5)
ax.axvline(x=np.pi, color='k', linestyle='--', alpha=0.5)
ax.axvline(x=2*np.pi, color='k', linestyle='--', alpha=0.5)

# Add horizontal line at y=0
ax.axhline(y=0, color='k', linestyle='-', alpha=0.5)

# Add text labels for key points
ax.text(0, -1.6, '0', ha='center')
ax.text(np.pi, -1.6, 'π', ha='center')
ax.text(2*np.pi, -1.6, '2π', ha='center')

plt.tight_layout()
plt.show()
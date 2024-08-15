'''
Code that plots the 16-QAM Constellation Diagram with labels for the 3 Amplitude circles

Symbol Map = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
Constellation Points = [-3.0-3.0j, -1.0-3.0j, 1.0-3.0j, 3.0-3.0j, -3.0-1.0j, -1.0-1.0j, 1.0-1.0j, 3.0-1.0j, -3.0+1.0j, -1.0+1.0j, 1.0+1.0j, 3.0+1.0j, -3.0+3.0j, -1.0+3.0j, 1.0+3.0j, 3.0+3.0j]

'''

import numpy as np
import matplotlib.pyplot as plt

# Define the I and Q values for 16-QAM
I_values_new = [-3, -1, 1, 3, -3, -1, 1, 3, -3, -1, 1, 3, -3, -1, 1, 3]
Q_values_new = [-3, -3, -3, -3, -1, -1, -1, -1,  1,  1,  1,  1,  3,  3, 3,  3]

# Decimal values from 0 to 15
decimal_values = list(range(16))

# Plotting the revised constellation diagram with adjusted title placement
plt.figure(figsize=(8, 8))
plt.scatter(I_values_new, Q_values_new, c='blue')

# Annotate each point with its decimal value
for i, (x, y) in enumerate(zip(I_values_new, Q_values_new)):
    plt.text(x, y, str(decimal_values[i]), fontsize=12, ha='center', va='center', color='white', bbox=dict(facecolor='blue', alpha=0.5))

# Draw and label amplitude circles
circle_radii = [np.sqrt(2), np.sqrt(10), np.sqrt(18)]
for radius in circle_radii:
    circle = plt.Circle((0, 0), radius, fill=False, color='gray', linestyle='--')
    plt.gca().add_artist(circle)
    if radius == np.sqrt(18):
        plt.text(0, radius, '√18', fontsize=10, ha='center', va='bottom', color='black')
    else:
        plt.text(0, radius, f'√{int(radius**2)}', fontsize=10, ha='center', va='bottom', color='black')

# Draw phase lines
max_radius = np.sqrt(18)  # Maximum radius of the outer circle
angles = np.arctan2(Q_values_new, I_values_new)
unique_angles = np.unique(angles)
for angle in unique_angles:
    x = [0, max_radius * np.cos(angle)]
    y = [0, max_radius * np.sin(angle)]
    plt.plot(x, y, color='gray', linestyle='--', linewidth=1, zorder=1)

# Adjusted title placement and axis limits
plt.title('16-QAM Constellation Diagram', fontsize=16, y=1.1)
plt.xlabel('In-phase (I)')
plt.ylabel('Quadrature (Q)')
plt.grid(True)
plt.xlim(-4.5, 4.5)
plt.ylim(-4.5, 4.5)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()

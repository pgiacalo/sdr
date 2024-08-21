import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons

# Define the constellation points and corresponding binary values for BPSK, 4-QAM, and 16-QAM
constellations = {
    'BPSK': {
        'I_values': [-1, 1],
        'Q_values': [0, 0],
        'symbols': [0, 1],
        'binary_values': ['0', '1'],
        'title': 'BPSK Constellation Diagram'
    },
    '4-QAM': {
        'I_values': [-1, 1, -1, 1],
        'Q_values': [-1, -1, 1, 1],
        'symbols': [0, 1, 2, 3],
        'binary_values': ['00', '01', '10', '11'],
        'title': '4-QAM Constellation Diagram'
    },
    '16-QAM': {
        'I_values': [-3, -1, 1, 3, -3, -1, 1, 3, -3, -1, 1, 3, -3, -1, 1, 3],
        'Q_values': [-3, -3, -3, -3, -1, -1, -1, -1, 1, 1, 1, 1, 3, 3, 3, 3],
        'symbols': list(range(16)),
        'binary_values': [format(i, '04b') for i in range(16)],
        'title': '16-QAM Constellation Diagram'
    }
}

# Plot the constellation diagram based on the selected modulation scheme
def plot_constellation(modulation_scheme):
    ax.clear()
    constellation = constellations[modulation_scheme]
    I_values = constellation['I_values']
    Q_values = constellation['Q_values']
    symbols = constellation['symbols']
    binary_values = constellation['binary_values']

    # Plot the points
    ax.scatter(I_values, Q_values, c='blue')

    # Plot the radial lines and circles
    for i, (x, y) in enumerate(zip(I_values, Q_values)):
        radius = np.sqrt(x**2 + y**2)
        circle = plt.Circle((0, 0), radius, color='gray', fill=False, linestyle='--')
        ax.add_artist(circle)
        ax.plot([0, x], [0, y], color='gray', linestyle='--')

        # Plot the decimal value inside the blue box
        ax.text(x, y, str(symbols[i]), fontsize=10, ha='center', va='center', color='white', bbox=dict(facecolor='blue', alpha=0.5))
        # Plot the binary value below the blue box
        ax.text(x, y - 0.5, binary_values[i], fontsize=10, ha='center', va='center', color='black')

    ax.set_title(constellation['title'], fontsize=16, y=1.05)
    ax.set_xlabel('In-phase (I)')
    ax.set_ylabel('Quadrature (Q)')
    ax.grid(True)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_aspect('equal', adjustable='box')

    # Adjust the axis limits depending on the modulation scheme
    max_val = max(max(abs(np.array(I_values))), max(abs(np.array(Q_values)))) + 1
    ax.set_xlim(-max_val, max_val)
    ax.set_ylim(-max_val, max_val)
    
    # Set axis ticks to show only integer values
    ax.set_xticks(np.arange(-max_val + 1, max_val, 1))
    ax.set_yticks(np.arange(-max_val + 1, max_val, 1))

    plt.draw()

# Create the plot and radio buttons
fig, ax = plt.subplots(figsize=(8, 8))
plt.subplots_adjust(left=0.3)

# Initial plot for 16-QAM
plot_constellation('16-QAM')

# Create radio buttons for modulation scheme selection
axcolor = 'lightgoldenrodyellow'
rax = plt.axes([0.05, 0.4, 0.2, 0.4], facecolor=axcolor)
radio = RadioButtons(rax, ('BPSK', '4-QAM', '16-QAM'))

# Set 16-QAM as the initially active radio button
radio.set_active(2)

# Update plot based on selected modulation scheme
radio.on_clicked(plot_constellation)

plt.show()

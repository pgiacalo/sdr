'''
This code provides both educational insights and visualizations, making it useful for understanding 
the differences between common 16-QAM encoding schemes.

Summary of the Full Code:
User Prompt: The user is prompted to select one of four different 16-QAM encoding standards: 
    Gray-coded, 
    Natural Binary Coding (NBC), 
    Set-Partitioning, or 
    LTE

Summary Information: After the user makes a selection, the code prints out a summary describing 
the chosen encoding scheme, its advantages, and typical use cases.

Constellation Diagram Generation: Based on the user's selection, the appropriate constellation diagram 
is generated and displayed, complete with annotations for bit values and decimal values.
'''

import numpy as np
import matplotlib.pyplot as plt

def generate_constellation_diagram(I_values, Q_values, bit_values, decimal_values, title):
    # Plot the constellation diagram
    plt.figure(figsize=(8, 8))
    plt.scatter(I_values, Q_values, c='blue')

    # Annotate each point with its decimal value and bit value
    for i, (x, y) in enumerate(zip(I_values, Q_values)):
        plt.text(x, y, f'{decimal_values[i]}\n{bit_values[i]}', fontsize=12, ha='center', va='center', color='white', bbox=dict(facecolor='blue', alpha=0.5))

    # Add amplitude circles
    circle_radii = [np.sqrt(2), np.sqrt(10), np.sqrt(18)]
    for radius in circle_radii:
        circle = plt.Circle((0, 0), radius, fill=False, color='gray', linestyle='--')
        plt.gca().add_artist(circle)

    # Add phase lines
    max_radius = np.sqrt(18)
    angles = np.arctan2(Q_values, I_values)
    unique_angles = np.unique(angles)
    for angle in unique_angles:
        x = [0, max_radius * np.cos(angle)]
        y = [0, max_radius * np.sin(angle)]
        plt.plot(x, y, color='gray', linestyle='--', linewidth=1, zorder=1)

    # Set plot parameters
    plt.title(title, fontsize=16, y=1.05)
    plt.xlabel('In-phase (I)')
    plt.ylabel('Quadrature (Q)')
    plt.xlim(-4.5, 4.5)
    plt.ylim(-4.5, 4.5)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True)
    plt.show()

def print_summary(choice):
    if choice == '1':
        summary = (
            "Gray-coded 16-QAM:\n"
            "---------------------\n"
            "Gray coding is the most common 16-QAM encoding scheme.\n"
            "It minimizes bit errors by ensuring that adjacent constellation points\n"
            "differ by only one bit. This is particularly beneficial in noisy environments,\n"
            "where small errors are less likely to cause significant data corruption.\n"
            "Gray-coded 16-QAM is widely used in digital communication standards like Wi-Fi\n"
            "(IEEE 802.11) and DSL (ITU-T G.992.1).\n"
        )
    elif choice == '2':
        summary = (
            "Natural Binary Coding (NBC) 16-QAM:\n"
            "-------------------------------------\n"
            "Natural binary coding maps bit sequences to constellation points in a simple\n"
            "binary counting sequence. Unlike Gray coding, adjacent points might differ by\n"
            "more than one bit, which increases the likelihood of errors in noisy environments.\n"
            "NBC is less common in practice due to this higher error susceptibility.\n"
        )
    elif choice == '3':
        summary = (
            "Set-Partitioning 16-QAM:\n"
            "--------------------------\n"
            "Set-partitioning divides the constellation points into subsets based on their\n"
            "distance from the origin. It maximizes the distance between subsets to improve\n"
            "error performance. This technique is often used in conjunction with Trellis\n"
            "Coded Modulation (TCM) to enhance robustness against errors. Set-partitioning\n"
            "is particularly beneficial in systems that require high reliability.\n"
        )
    elif choice == '4':
        summary = (
            "LTE Gray-Coded 16-QAM:\n"
            "-------------------------\n"
            "LTE uses a form of Gray-coded 16-QAM optimized for mobile communication.\n"
            "This encoding balances robustness with efficiency, making it ideal for\n"
            "environments with varying signal quality. Adaptive modulation and coding\n"
            "(AMC) in LTE allows the system to switch between different modulation\n"
            "schemes based on current channel conditions, ensuring reliable communication.\n"
        )
    else:
        summary = "Invalid choice."
    
    print(summary)

def main():
    # Prompt user to select the standard
    print("Choose a 16-QAM standard:")
    print("1: Gray-coded 16-QAM")
    print("2: Natural Binary Coding (NBC) 16-QAM")
    print("3: Set-Partitioning 16-QAM")
    print("4: LTE 16-QAM")
    choice = input("Enter the number of your choice: ").strip()

    if choice == '1':
        # Gray-coded 16-QAM
        bit_values = [
            '0100', '0101', '0111', '0110',
            '0000', '0001', '0011', '0010',
            '1000', '1001', '1011', '1010',
            '1100', '1101', '1111', '1110'
        ]
        decimal_values = [int(bv, 2) for bv in bit_values]
        I_values = [-3, -1, 1, 3, -3, -1, 1, 3, -3, -1, 1, 3, -3, -1, 1, 3]
        Q_values = [-3, -3, -3, -3, -1, -1, -1, -1,  1,  1,  1,  1,  3,  3, 3,  3]
        title = "Gray-Coded 16-QAM Constellation Diagram"
    
    elif choice == '2':
        # Natural Binary Coding (NBC) 16-QAM
        bit_values = [
            '0000', '0001', '0010', '0011',
            '0100', '0101', '0110', '0111',
            '1000', '1001', '1010', '1011',
            '1100', '1101', '1110', '1111'
        ]
        decimal_values = [int(bv, 2) for bv in bit_values]
        I_values = [-3, -1, 1, 3, -3, -1, 1, 3, -3, -1, 1, 3, -3, -1, 1, 3]
        Q_values = [-3, -3, -3, -3, -1, -1, -1, -1,  1,  1,  1,  1,  3,  3, 3,  3]
        title = "Natural Binary Coding (NBC) 16-QAM Constellation Diagram"
    
    elif choice == '3':
        # Set-Partitioning 16-QAM (example mapping, not unique)
        bit_values = [
            '0000', '0001', '0011', '0010',
            '0100', '0101', '0111', '0110',
            '1000', '1001', '1011', '1010',
            '1100', '1101', '1111', '1110'
        ]
        decimal_values = [int(bv, 2) for bv in bit_values]
        I_values = [-3, -1, 1, 3, -3, -1, 1, 3, -3, -1, 1, 3, -3, -1, 1, 3]
        Q_values = [-3, -3, -3, -3, -1, -1, -1, -1,  1,  1,  1,  1,  3,  3, 3,  3]
        title = "Set-Partitioning 16-QAM Constellation Diagram"
    
    elif choice == '4':
        # LTE Gray-coded 16-QAM
        bit_values = [
            '0100', '0101', '0111', '0110',
            '0000', '0001', '0011', '0010',
            '1000', '1001', '1011', '1010',
            '1100', '1101', '1111', '1110'
        ]
        decimal_values = [int(bv, 2) for bv in bit_values]
        I_values = [-3, -1, 1, 3, -3, -1, 1, 3, -3, -1, 1, 3, -3, -1, 1, 3]
        Q_values = [-3, -3, -3, -3, -1, -1, -1, -1,  1,  1,  1,  1,  3,  3, 3,  3]
        title = "LTE Gray-Coded 16-QAM Constellation Diagram"
    
    else:
        print("Invalid choice.")
        return

    # Print a summary of the chosen 16-QAM encoding scheme
    print_summary(choice)

    # Generate the chosen constellation diagram
    generate_constellation_diagram(I_values, Q_values, bit_values, decimal_values, title)

if __name__ == "__main__":
    main()

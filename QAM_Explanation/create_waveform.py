import numpy as np

# Define the amplitude multipliers for I and Q channels
I_amplitudes = np.arange(-1.5, 2.0, 0.5)  # -1.5 to +1.5 stepping by +0.5
Q_amplitudes = np.arange(1.5, -2.0, -0.5)  # 1.5 to -1.5 stepping by -0.5

# Define parameters for timing and frequency
sample_rate = 200000  # samples per second, 5 microseconds per sample
samples_per_step = 1  # each step lasts 5 microseconds
duration_ms = (len(I_amplitudes) * 5) / 1000  # total duration in ms based on number of steps

# Calculate the total number of samples
total_samples = int(sample_rate * (duration_ms / 1000))  # Convert ms to seconds for total duration

# Initialize arrays for I and Q values
I_values = np.repeat(I_amplitudes, samples_per_step)
Q_values = np.repeat(Q_amplitudes, samples_per_step)

# Ensure that the number of samples matches the expected total samples
# If not, adjust the array sizes (This step may not be necessary but ensures consistency)
I_values = np.tile(I_values, (total_samples // len(I_values) + 1))[:total_samples]
Q_values = np.tile(Q_values, (total_samples // len(Q_values) + 1))[:total_samples]

# Save the I and Q values to CSV files
np.savetxt('I_channel_values.csv', I_values, delimiter=',', fmt='%.1f')
np.savetxt('Q_channel_values.csv', Q_values, delimiter=',', fmt='%.1f')

print("I and Q channel values have been saved to 'I_channel_values.csv' and 'Q_channel_values.csv'.")

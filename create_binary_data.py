# Example ASCII data string representing 16-QAM symbols (sequence of values 0-15, 4 bits per symbol)
ascii_data = "0000000100100011010001010110011110001001101010111100110111101111"

# Convert the ASCII binary string into a binary file
byte_data = int(ascii_data, 2).to_bytes((len(ascii_data) + 7) // 8, byteorder='big')

# Write the bytes object to a binary file
with open("qam_symbols.bin", "wb") as f:
    f.write(byte_data)


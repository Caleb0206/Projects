def print_hex_encoding(file_path, file_path2):
    with open(file_path, 'rb') as file:
        # Read the entire file content
        content = file.read()

        # Convert the content to hexadecimal format
        hex_encoded = []
        hex_encoded.append(f"{byte:02X}" for byte in content)
        # Print the hexadecimal encoding
    with open(file_path2, 'rb') as file2:
        # Read the entire file content
        content2 = file2.read()

        # Convert the content to hexadecimal format
        hex_encoded2 = []
        hex_encoded2.append(f"{byte2:02X}" for byte2 in content2)
        # Print the hexadecimal encoding
    for index, char in enumerate(hex_encoded):
        if hex_encoded[index] != hex_encoded2[index]:
            print(hex_encoded[index], hex_encoded2[index], index)

if __name__ == '__main__':
    print("liuh")
    print_hex_encoding("file_WAP_out_compressed.txt", "file_WAP_compressed_soln.txt")
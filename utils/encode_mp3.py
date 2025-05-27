import base64


def encode_mp3_to_base64(file_path, output_path):
    """
    Encodes an MP3 file to Base64 and writes the result to a text file.

    Args:
        file_path (str): Path to the input MP3 file.
        output_path (str): Path to the output text file.
    """
    with open(file_path, "rb") as mp3_file:
        encoded_bytes = base64.b64encode(mp3_file.read())
        encoded_str = encoded_bytes.decode("utf-8")

    with open(output_path, "w") as output_file:
        output_file.write(encoded_str)


# Example usage
if __name__ == "__main__":
    mp3_path = "ChestPain.mp3"  # Replace with your MP3 file path
    output_txt = "ChestPain.txt"  # Output text file path
    encode_mp3_to_base64(mp3_path, output_txt)
    print(f"Encoded MP3 written to {output_txt}")

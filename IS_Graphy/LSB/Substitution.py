from PIL import Image
import os

# Convert string to binary
def to_bin(data):
    return ''.join(format(ord(c), '08b') for c in data)

# Convert binary to string
def bin_to_text(binary_data):
    chars = [chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8)]
    return ''.join(chars)

# Encode message into image
def encode_lsb_sub():
    # Hardcoded message
    message = "This is a secret message from Debayan 👨‍💻"

    # Input and output image paths
    image_path = r"D:\Debayan\yhpargonagets\IS_Graphy\apple.png"
    output_path = r"D:\Debayan\yhpargonagets\IS_Graphy\LSB\apple_encoded.png"

    # Load image and ensure RGB
    img = Image.open(image_path).convert("RGB")
    encoded = img.copy()
    width, height = img.size

    # Convert message to binary and add delimiter
    binary_msg = to_bin(message + "####")
    msg_index = 0
    msg_len = len(binary_msg)

    for y in range(height):
        for x in range(width):
            if msg_index >= msg_len:
                break
            r, g, b = encoded.getpixel((x, y))

            if msg_index < msg_len:
                r = int(format(r, '08b')[:-1] + binary_msg[msg_index], 2)
                msg_index += 1
            if msg_index < msg_len:
                g = int(format(g, '08b')[:-1] + binary_msg[msg_index], 2)
                msg_index += 1
            if msg_index < msg_len:
                b = int(format(b, '08b')[:-1] + binary_msg[msg_index], 2)
                msg_index += 1

            encoded.putpixel((x, y), (r, g, b))

        if msg_index >= msg_len:
            break

    encoded.save(output_path, "PNG")
    print(f"✅ Message encoded and saved at: {output_path}")

# Decode message from image
def decode_lsb_sub():
    encoded_path = r"D:\Debayan\yhpargonagets\IS_Graphy\LSB\apple_encoded.png"
    img = Image.open(encoded_path)
    binary_data = ""

    for y in range(img.height):
        for x in range(img.width):
            r, g, b = img.getpixel((x, y))
            binary_data += format(r, '08b')[-1]
            binary_data += format(g, '08b')[-1]
            binary_data += format(b, '08b')[-1]

    message = bin_to_text(binary_data)
    final_message = message.split("####")[0]
    print(f"🔍 Decoded message: {final_message}")
if __name__ == "__main__":
    if not os.path.exists(r"D:\Debayan\yhpargonagets\IS_Graphy\LSB\apple_encoded.png"):
        encode_lsb_sub()
    decode_lsb_sub()            
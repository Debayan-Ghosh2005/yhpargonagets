from PIL import Image

def decode_udh(image_path):
    img = Image.open(image_path)
    binary_data = ""

    # Read the least significant bits from RGB channels
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = img.getpixel((x, y))
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)

    # Group into 8-bit chunks
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]

    # Convert binary to ASCII, stop at null character
    message = ""
    for char in chars:
        decoded_char = chr(int(char, 2))
        if decoded_char == chr(0):  # Null terminator used in encoding
            break
        message += decoded_char

    print("[✓] Decoded message from UDH stego image:", message)

# 🔍 Path to UDH-encoded image
stego_image_path = r"C:\cod\yhpargonagets\IS_Graphy\UDH\apple_stego_udh.png"

# 🔓 Run the decoder
decode_udh(stego_image_path)

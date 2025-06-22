from PIL import Image

def decode_image(image_path):
    img = Image.open(image_path)
    binary_data = ""

    for y in range(img.height):
        for x in range(img.width):
            r, g, b = img.getpixel((x, y))
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)

    # Split binary string into 8-bit chunks
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]

    # Convert to characters until null character is found
    message = ""
    for char in chars:
        decoded_char = chr(int(char, 2))
        if decoded_char == chr(0):  # End of message
            break
        message += decoded_char

    print("[✓] Decoded message:", message)

# Path to the stego image
stego_image_path = r"C:\cod\yhpargonagets\IS_Graphy\F5\apple_stego.png"

# Run the decoder
decode_image(stego_image_path)

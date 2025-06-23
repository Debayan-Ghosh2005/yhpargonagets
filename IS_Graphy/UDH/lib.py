from PIL import Image
import os

def encode_udh(image_path, message, output_path):
    # Open the original image
    img = Image.open(image_path)
    encoded = img.copy()
    width, height = img.size

    # Append null character to signal end of message
    message += chr(0)

    # Convert the message to binary string
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    data_index = 0

    # Loop over pixels
    for y in range(height):
        for x in range(width):
            if data_index >= len(binary_message):
                break

            r, g, b = img.getpixel((x, y))

            # Encode up to 3 bits per pixel (1 in R, 1 in G, 1 in B)
            if data_index < len(binary_message):
                r = (r & ~1) | int(binary_message[data_index])
                data_index += 1
            if data_index < len(binary_message):
                g = (g & ~1) | int(binary_message[data_index])
                data_index += 1
            if data_index < len(binary_message):
                b = (b & ~1) | int(binary_message[data_index])
                data_index += 1

            encoded.putpixel((x, y), (r, g, b))

        if data_index >= len(binary_message):
            break

    # Save the encoded image
    encoded.save(output_path)
    print(f"[✓] Message encoded using UDH and saved to: {output_path}")

# --- File Paths ---
input_image_path = r"C:\cod\yhpargonagets\IS_Graphy\apple.jpg"
output_dir = r"C:\cod\yhpargonagets\IS_Graphy\UDH"
os.makedirs(output_dir, exist_ok=True)
output_image_path = os.path.join(output_dir, "apple_stego_udh.png")

# --- Secret Message ---
secret_message = "kitty kitty"

# --- Run Encoding ---
encode_udh(input_image_path, secret_message, output_image_path)

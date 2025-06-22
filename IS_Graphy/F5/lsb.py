from PIL import Image
import os

# LSB encode function
def encode_image(image_path, message, output_path):
    img = Image.open(image_path)
    encoded = img.copy()
    width, height = img.size
    message += chr(0)  # Add end of message delimiter

    data_index = 0
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    for y in range(height):
        for x in range(width):
            if data_index >= len(binary_message):
                break
            r, g, b = img.getpixel((x, y))
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

    encoded.save(output_path)
    print(f"[✓] Message encoded and saved to: {output_path}")

# Paths
input_image_path = r"C:\cod\yhpargonagets\IS_Graphy\apple.jpg"
output_dir = r"C:\cod\yhpargonagets\IS_Graphy\F5"
os.makedirs(output_dir, exist_ok=True)
output_image_path = os.path.join(output_dir, "apple_stego.png")

# Message
secret_message = "kitty kitty"

# Encode
encode_image(input_image_path, secret_message, output_image_path)

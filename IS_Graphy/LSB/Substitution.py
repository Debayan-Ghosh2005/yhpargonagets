from PIL import Image
import os

def to_bin(data):
    return ''.join(format(ord(i), '08b') for i in data)

def encode_lsb_sub(message):
    # Input image path
    image_path = r"D:\Debayan\yhpargonagets\IS_Graphy\apple.png"
    img = Image.open(image_path).convert("RGB")

    # Save encoded image in same folder with _encoded.png suffix
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    folder = os.path.dirname(image_path)
    output_path = os.path.join(folder, f"{base_name}_encoded.png")

    # Prepare message
    msg = to_bin(message + "####")
    encoded = img.copy()
    w, h = img.size
    idx = 0

    # Embed message bits into image
    for y in range(h):
        for x in range(w):
            if idx >= len(msg):
                break
            r, g, b = encoded.getpixel((x, y))
            if idx < len(msg):
                r = int(format(r, '08b')[:-1] + msg[idx], 2)
                idx += 1
            if idx < len(msg):
                g = int(format(g, '08b')[:-1] + msg[idx], 2)
                idx += 1
            if idx < len(msg):
                b = int(format(b, '08b')[:-1] + msg[idx], 2)
                idx += 1
            encoded.putpixel((x, y), (r, g, b))

    # Save encoded image
    try:
        encoded.save(output_path, "PNG")
        print(f"✅ Message encoded and saved as: {output_path}")
    except Exception as e:
        print(f"❌ Error saving image: {e}")

def decode_lsb_sub():
    encoded_path = r"D:\Debayan\yhpargonagets\IS_Graphy\apple_encoded.png"
    if not os.path.exists(encoded_path):
        print("❌ Encoded image not found.")
        return

    img = Image.open(encoded_path)
    binary = ""

    for y in range(img.height):
        for x in range(img.width):
            r, g, b = img.getpixel((x, y))
            binary += format(r, '08b')[-1]
            binary += format(g, '08b')[-1]
            binary += format(b, '08b')[-1]

    chars = [chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)]
    message = ''.join(chars).split("####")[0]
    print(f"🔍 Decoded message: {message}")

from PIL import Image

def decode_red_channel():
    input_path = r"D:\Debayan\yhpargonagets\IS_Graphy\LSB\basic_encoded.png"
    img = Image.open(input_path)
    pixels = img.load()

    bits = ''
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            bits += str(r & 1)

    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    msg = ''
    for b in chars:
        if int(b, 2) == 0: break  # Null terminator
        msg += chr(int(b, 2))

    print("[+] Decoded from red channel:", msg)

decode_red_channel()

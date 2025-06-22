from PIL import Image

def to_binary(msg):
    return ''.join(format(ord(c), '08b') for c in msg)

def encode_red_channel():
    input_path = r"IS_Graphy\apple.png"
    output_path = r"D:\Debayan\yhpargonagets\IS_Graphy\LSB\basic_encoded.png"
    message = "my name is debayan" + chr(0)  # Null terminator

    img = Image.open(input_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    pixels = img.load()

    bin_msg = to_binary(message)
    idx = 0
    for y in range(img.height):
        for x in range(img.width):
            if idx >= len(bin_msg): break
            r, g, b = pixels[x, y]
            r = (r & ~1) | int(bin_msg[idx])
            pixels[x, y] = (r, g, b)
            idx += 1
        if idx >= len(bin_msg): break

    img.save(output_path)
    print("[+] Red channel encoding done:", output_path)

encode_red_channel()

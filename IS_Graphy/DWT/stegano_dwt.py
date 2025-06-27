import numpy as np
from PIL import Image
import os

class Steganography:
    def __init__(self):
        self.delimiter = '1111111111111110'

    def load_image(self, path="/home/suboptimal/Steganography/yhpargonagets/IS_Graphy/DWT/apple.png"):
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} not found")
        return np.array(Image.open(path).convert('L'), dtype=np.int32)

    def save_image(self, image, path="apple_stego.png"):
        path = os.path.splitext(path)[0] + '.png'
        Image.fromarray(np.clip(image, 0, 255).astype(np.uint8)).save(path)
        return path

    def text_to_binary(self, text):
        length_bin = format(len(text), '032b')
        data_bin = ''.join(format(ord(c), '08b') for c in text)
        return length_bin + data_bin + self.delimiter

    def binary_to_text(self, binary):
        length = int(binary[:32], 2)
        return ''.join(chr(int(binary[i:i+8], 2)) for i in range(32, 32 + length * 8, 8))

    def embed(self, message, output_path="apple_stego.png"):
        img = self.load_image()
        data = self.text_to_binary(message)
        flat = img.flatten()
        if len(data) > len(flat):
            raise ValueError("Message too long for the image")
        for i, bit in enumerate(data):
            flat[i] = (flat[i] & ~1) | int(bit)
        return self.save_image(flat.reshape(img.shape), output_path)

    def extract(self):
        img = self.load_image("apple_stego.png").flatten()
        bits = ''.join(str(p & 1) for p in img)
        end = bits.find(self.delimiter)
        return self.binary_to_text(bits[:end]) if end != -1 else "[ERROR] Delimiter not found"

def switch_case():
    steg = Steganography()
    print("\n--- Steganography on apple.png ---")
    print("1. Embed a message")
    print("2. Extract a message")
    choice = input("Enter choice (1 or 2): ")

    if choice == '1':
        msg = input("Enter the message to embed: ")
        try:
            out = steg.embed(msg)
            print(f"[SUCCESS] Message embedded in {out}")
        except Exception as e:
            print(f"[ERROR] {e}")

    elif choice == '2':
        try:
            msg = steg.extract()
            print(f"[MESSAGE EXTRACTED] {msg}")
        except Exception as e:
            print(f"[ERROR] {e}")
    else:
        print("[ERROR] Invalid choice")

if __name__ == "__main__":
    switch_case()

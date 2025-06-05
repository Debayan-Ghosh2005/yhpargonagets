import os
import json

LOG_FILE = "stego_log.json"

# ---------- Encoding/Decoding Core ----------
def text_to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text)

def binary_to_whitespace(binary):
    return ''.join(' ' if bit == '0' else '\t' for bit in binary)

def whitespace_to_binary(whitespace):
    return ''.join('0' if ch == ' ' else '1' for ch in whitespace)

def binary_to_text(binary):
    chars = []
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            chars.append(chr(int(byte, 2)))
    return ''.join(chars)

def encode_message(cover, secret):
    binary = text_to_binary(secret)
    hidden = binary_to_whitespace(binary)
    return cover + hidden

def decode_message(stego_text):
    hidden_part = ''.join(ch for ch in stego_text if ch in (' ', '\t'))
    binary = whitespace_to_binary(hidden_part)
    return binary_to_text(binary)

# ---------- Logging Utilities ----------
def load_log():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, 'r') as f:
        return json.load(f)

def save_log(logs):
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)

def add_to_log(cover, secret, stego):
    logs = load_log()
    logs.append({
        "cover": cover,
        "secret": secret,
        "stego": stego
    })
    save_log(logs)

def get_hidden_by_cover(cover):
    logs = load_log()
    for entry in logs:
        if entry['cover'] == cover:
            return entry['secret']
    return None

# ---------- Main Interface ----------
def main():
    print("📦 Whitespace Steganography Logger")
    print("1. Encode and Save")
    print("2. Decode from Stego Message")
    print("3. Retrieve Hidden Message by Cover Text")
    choice = input("Choose option (1/2/3): ").strip()

    if choice == "1":
        cover = input("Enter the visible (cover) message: ")
        secret = input("Enter the secret message to hide: ")
        stego = encode_message(cover, secret)
        add_to_log(cover, secret, stego)
        print("\n✅ Encoded message (copy this for decode):")
        print(repr(stego))

    elif choice == "2":
        stego_input = input("📥 Paste the full encoded message (with whitespace):\n")
        secret = decode_message(stego_input)
        print("\n🔓 Decoded Secret Message:")
        print(secret)

    elif choice == "3":
        cover = input("Enter the original visible cover message: ")
        hidden = get_hidden_by_cover(cover)
        if hidden:
            print("\n📂 Retrieved Hidden Message:")
            print(hidden)
        else:
            print("❌ No matching message found.")

    else:
        print("❌ Invalid choice.")

# Run it
if __name__ == "__main__":
    main()

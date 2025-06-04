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

# 🔧 Interface
print("📦 Whitespace Steganography")
choice = input("Choose mode (encode/decode): ").strip().lower()

if choice == "encode":
    cover_msg = input("Enter the visible (cover) message: ")
    secret_msg = input("Enter the secret message to hide: ")
    stego = encode_message(cover_msg, secret_msg)
    print("\n✅ Encoded message with hidden secret:")
    print(repr(stego))  # show hidden chars safely
    print("\n⚠️ Copy and paste this entire string to decode later.")

elif choice == "decode":
    print("📥 Paste the full encoded message (including whitespace):")
    stego_input = input()
    secret = decode_message(stego_input)
    print("\n🔓 Decoded Secret Message:")
    print(secret)

else:
    print("❌ Invalid option. Choose either 'encode' or 'decode'.")

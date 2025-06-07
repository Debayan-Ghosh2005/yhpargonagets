import os
import json

LOG_FILE = "format_log2.json"

def save_log(log_data):
    with open(LOG_FILE, "w") as f:
        json.dump(log_data, f, indent=4)

def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

def text_to_bits(text):
    return ''.join(format(ord(char), '08b') for char in text)

def bits_to_text(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(b, 2)) for b in chars if len(b) == 8)

# --- Encoding using double/single space
def encode_formatting(cover_text, secret_msg):
    bits = text_to_bits(secret_msg)
    words = cover_text.split(' ')
    if len(words) < len(bits) + 1:
        raise ValueError("Not enough words in cover text to hide the secret.")

    encoded_text = ""
    log = {}

    for i in range(len(bits)):
        space = "  " if bits[i] == '1' else " "
        encoded_text += words[i] + space
        log[i] = {
            "word": words[i],
            "bit": bits[i],
            "space_type": "double" if bits[i] == '1' else "single"
        }

    encoded_text += ' '.join(words[len(bits):])
    return encoded_text.strip(), log

# --- Decode from formatting (double/single space)
def decode_formatting(encoded_text):
    # detect spaces between words
    parts = encoded_text.split(' ')
    bits = []
    i = 0
    while i < len(parts) - 1:
        if parts[i] == '':
            bits.append('1')
            i += 2  # double space detected
        else:
            bits.append('0')
            i += 1  # single space
    try:
        secret = bits_to_text(''.join(bits))
    except:
        secret = ""
    return secret

def main():
    print("=== Formatting Steganography ===")
    logs = load_log()

    while True:
        print("\nOptions: encode / decode / retrieve / exit")
        choice = input("Enter choice: ").strip().lower()

        if choice == "encode":
            cover = input("\nEnter cover text:\n")
            secret = input("Enter secret message:\n")
            try:
                encoded_text, log = encode_formatting(cover, secret)
                print("\nEncoded text:")
                print(encoded_text)
                msg_id = str(len(logs) + 1)
                logs[msg_id] = {
                    "encoded_text": encoded_text,
                    "log": log,
                    "secret_msg": secret
                }
                save_log(logs)
                print(f"Message saved with ID: {msg_id}")
            except Exception as e:
                print("Error:", e)

        elif choice == "decode":
            msg_id = input("Enter message ID to decode: ").strip()
            if msg_id in logs:
                encoded = logs[msg_id]["encoded_text"]
                decoded = decode_formatting(encoded)
                print("Decoded secret message:", decoded)
            else:
                print("Message ID not found.")

        elif choice == "retrieve":
            print("Available message IDs:", ', '.join(logs.keys()))
            ids = input("Enter message IDs (space separated): ").split()
            combined_bits = ""
            for mid in ids:
                if mid in logs:
                    encoded = logs[mid]["encoded_text"]
                    parts = encoded.split(' ')
                    i = 0
                    while i < len(parts) - 1:
                        if parts[i] == '':
                            combined_bits += '1'
                            i += 2
                        else:
                            combined_bits += '0'
                            i += 1
                else:
                    print(f"ID {mid} not found.")
            try:
                secret = bits_to_text(combined_bits)
                print("Combined secret message:")
                print(secret)
            except:
                print("Could not decode combined bits.")

        elif choice == "exit":
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()

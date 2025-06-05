import json
import os

LOG_FILE = "syn_stego_log.json"

def save_log(data):
    with open(LOG_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}

def text_to_bits(text):
    return ''.join(format(ord(c), '08b') for c in text)

def bits_to_text(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(b, 2)) for b in chars if len(b) == 8)

def build_synonym_dict():
    print("Build synonym dictionary.")
    print("Enter words and their synonyms that will encode bit 1 when used.")
    print("For example: 'quick fast' means 'quick' original encodes 0, 'fast' encodes 1")
    print("Type 'done' when finished.\n")

    syn_dict = {}
    while True:
        line = input("Enter word and its synonym separated by space (or 'done'): ").strip()
        if line.lower() == 'done':
            break
        parts = line.split()
        if len(parts) != 2:
            print("Invalid input, enter exactly two words.")
            continue
        original, synonym = parts
        syn_dict[original.lower()] = synonym.lower()
    return syn_dict

def encode(cover_text, secret_msg, synonym_dict):
    secret_bits = text_to_bits(secret_msg)
    words = cover_text.split()
    encoded_words = []
    bit_index = 0
    log = {}

    for w in words:
        lw = w.lower()
        if lw in synonym_dict and bit_index < len(secret_bits):
            bit = secret_bits[bit_index]
            if bit == '1':
                encoded_word = synonym_dict[lw]
            else:
                encoded_word = w
            log[str(len(encoded_words))] = {
                "original": w,
                "encoded": encoded_word,
                "bit": bit
            }
            encoded_words.append(encoded_word)
            bit_index += 1
        else:
            encoded_words.append(w)

    encoded_text = ' '.join(encoded_words)
    return encoded_text, log

def decode(encoded_text, synonym_dict):
    reverse_syn_dict = {v: k for k, v in synonym_dict.items()}
    words = encoded_text.split()
    bits = []
    for w in words:
        lw = w.lower()
        if lw in synonym_dict:
            bits.append('0')
        elif lw in reverse_syn_dict:
            bits.append('1')
        else:
            continue
    try:
        secret = bits_to_text(''.join(bits))
    except Exception:
        secret = ""
    return secret

def main():
    print("=== Synonym Steganography ===\n")
    synonym_dict = build_synonym_dict()
    logs = load_log()

    while True:
        print("\nOptions: encode / decode / retrieve / exit")
        choice = input("Enter choice: ").strip().lower()
        if choice == "encode":
            cover_text = input("Enter cover text:\n")
            secret_msg = input("Enter secret message (text):\n")
            encoded_text, log = encode(cover_text, secret_msg, synonym_dict)
            print("\nEncoded Text:")
            print(encoded_text)

            msg_id = str(len(logs) + 1)
            logs[msg_id] = {
                "encoded_text": encoded_text,
                "log": log,
                "secret_msg": secret_msg
            }
            save_log(logs)
            print(f"Log saved with message ID: {msg_id}")

        elif choice == "decode":
            msg_id = input("Enter message ID to decode: ").strip()
            if msg_id in logs:
                encoded_text = logs[msg_id]["encoded_text"]
                decoded_msg = decode(encoded_text, synonym_dict)
                print(f"Decoded secret message from ID {msg_id}: {decoded_msg}")
            else:
                print("Message ID not found.")

        elif choice == "retrieve":
            print("Available message IDs:", ', '.join(logs.keys()))
            msg_ids = input("Enter message IDs separated by space to retrieve hidden messages:\n").split()
            combined_bits = ""
            reverse_syn_dict = {v: k for k, v in synonym_dict.items()}
            for mid in msg_ids:
                if mid in logs:
                    encoded_text = logs[mid]["encoded_text"]
                    words = encoded_text.split()
                    for w in words:
                        lw = w.lower()
                        if lw in synonym_dict:
                            combined_bits += '0'
                        elif lw in reverse_syn_dict:
                            combined_bits += '1'
                else:
                    print(f"Message ID {mid} not found.")
            try:
                combined_secret = bits_to_text(combined_bits)
                print("Combined decoded secret message:")
                print(combined_secret)
            except Exception:
                print("Could not decode combined secret message properly.")

        elif choice == "exit":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please enter encode, decode, retrieve, or exit.")

if __name__ == "__main__":
    main()

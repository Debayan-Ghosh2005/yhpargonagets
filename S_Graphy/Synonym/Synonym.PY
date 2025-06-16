import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
import os
import random
import nltk
from nltk.corpus import wordnet

# Ensure wordnet is downloaded
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

# === CONFIGURATION ===
LOG_FILE = "syn_stego_log.json"

# === AUTO-GENERATE SYNONYM MAP ===
def generate_synonyms(words, limit=8):
    syn_map = {}
    for word in words:
        synonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                name = lemma.name().replace('_', ' ').lower()
                if name != word:
                    synonyms.add(name)
        synonyms = list(synonyms)
        if word not in synonyms:
            synonyms.insert(0, word)
        random.shuffle(synonyms)
        syn_map[word] = list(set(synonyms))[:limit]
    return syn_map

SYNONYM_MAP = generate_synonyms([
    "happy", "sad", "fast", "slow", "big", "small", "smart", "angry"
])

# === BUILD MAPPINGS ===
BIT_TO_WORD = {word: {} for word in SYNONYM_MAP}
WORD_TO_BIT = {}

for word, synonyms in SYNONYM_MAP.items():
    random.shuffle(synonyms)  # Add randomness to synonym ordering
    bits_required = len(bin(len(synonyms) - 1)[2:])
    for i, syn in enumerate(synonyms):
        bit_str = format(i, f'0{bits_required}b')
        BIT_TO_WORD[word][bit_str] = syn
        WORD_TO_BIT[syn.lower()] = bit_str

# === CONVERT MESSAGE ===
def text_to_bin(message):
    if all(c in '01' for c in message.strip()):
        return message + 'done'
    else:
        message += "done"
        return ''.join(format(ord(c), '08b') for c in message)

def bin_to_text(bitstream):
    chars = [chr(int(bitstream[i:i+8], 2)) for i in range(0, len(bitstream), 8)]
    full_msg = ''.join(chars)
    return full_msg.split("done")[0] if "done" in full_msg else "[!] Termination keyword not found"

# === LOGGING ===
def save_log(data):
    with open(LOG_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def retrieve_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            return json.load(f)
    return {"status": "No log found"}

# === ENCODER ===
def encode_synonym_stego(cover_text, secret_msg):
    bin_msg = text_to_bin(secret_msg)
    words = cover_text.split()
    i = 0
    stego_words = []

    for word in words:
        lower = word.lower()
        if lower in SYNONYM_MAP:
            syn_count = len(SYNONYM_MAP[lower])
            bit_len = len(bin(syn_count - 1)[2:])
            if i + bit_len <= len(bin_msg):
                chunk = bin_msg[i:i + bit_len]
                syn = BIT_TO_WORD[lower].get(chunk, word)
                stego_words.append(syn)
                i += bit_len
            else:
                stego_words.append(random.choice(SYNONYM_MAP[lower]))
        else:
            stego_words.append(word)

    if i < len(bin_msg):
        print(f"[!] Only {i} of {len(bin_msg)} bits encoded. Add more synonym-eligible words in your text.")

    stego_text = ' '.join(stego_words)
    save_log({
        "original_text": cover_text,
        "secret_message": secret_msg,
        "stego_text": stego_text,
        "binary_encoded": bin_msg,
        "bits_encoded": i
    })
    return stego_text

# === DECODER ===
def decode_synonym_stego(stego_text):
    words = stego_text.split()
    bitstream = ''

    for word in words:
        bit = WORD_TO_BIT.get(word.lower())
        if bit:
            bitstream += bit

    return bin_to_text(bitstream)

# === GUI ===
def encode_action():
    cover = entry_cover.get("1.0", "end-1c")
    secret = entry_secret.get("1.0", "end-1c")
    if not cover or not secret:
        messagebox.showerror("Missing input", "Cover text and secret message are required.")
        return
    stego = encode_synonym_stego(cover, secret)
    output_box.delete("1.0", "end")
    output_box.insert("1.0", stego)

def decode_action():
    stego = entry_cover.get("1.0", "end-1c")
    if not stego:
        messagebox.showerror("Missing input", "Please paste stego text to decode.")
        return
    decoded = decode_synonym_stego(stego)
    output_box.delete("1.0", "end")
    output_box.insert("1.0", decoded)

def view_log():
    log = retrieve_log()
    output_box.delete("1.0", "end")
    output_box.insert("1.0", json.dumps(log, indent=4))

# === GUI WINDOW ===
root = tk.Tk()
root.title("\U0001F512 Synonym Steganography")
root.geometry("700x600")

tk.Label(root, text="Cover/Stego Text:", font=('Arial', 12)).pack()
entry_cover = scrolledtext.ScrolledText(root, height=5, wrap=tk.WORD)
entry_cover.pack(padx=10, pady=5)

tk.Label(root, text="Secret Message (text or binary):", font=('Arial', 12)).pack()
entry_secret = scrolledtext.ScrolledText(root, height=2, wrap=tk.WORD)
entry_secret.pack(padx=10, pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="\U0001F510 Encode", command=encode_action, width=15).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="\U0001F513 Decode", command=decode_action, width=15).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="\U0001F4DC View Log", command=view_log, width=15).grid(row=0, column=2, padx=10)

tk.Label(root, text="Output:", font=('Arial', 12)).pack()
output_box = scrolledtext.ScrolledText(root, height=10, wrap=tk.WORD)
output_box.pack(padx=10, pady=5)

root.mainloop()

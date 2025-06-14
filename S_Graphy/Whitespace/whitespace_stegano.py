<<<<<<< HEAD
import tkinter as tk
from tkinter import scrolledtext, messagebox

# --- Steganography core functions ---
=======
import os
import json

LOG_FILE = "stego_log.json"

# ---------- Encoding/Decoding Core ----------
>>>>>>> a00588b67eeb4421657e50048f418d17e2fd32f0
def text_to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text)

def binary_to_whitespace(binary):
    return ''.join(' ' if bit == '0' else '\t' for bit in binary)

def whitespace_to_binary(whitespace):
    return ''.join('0' if ch == ' ' else '1' for ch in whitespace)

def binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)

def encode_message(cover, secret):
    binary = text_to_binary(secret)
    hidden = binary_to_whitespace(binary)
    return cover + "\n[hidden]\n" + hidden + "\n[end]"

def decode_message(stego_text):
    if "[hidden]" not in stego_text or "[end]" not in stego_text:
        return "❌ Missing [hidden] or [end] marker."

<<<<<<< HEAD
    try:
        hidden_part = stego_text.split("[hidden]", 1)[1].split("[end]", 1)[0]
        whitespace_only = ''.join(ch for ch in hidden_part if ch in (' ', '\t'))

        if not whitespace_only:
            return "⚠️ No space/tab hidden message found."

        binary = whitespace_to_binary(whitespace_only)
        if len(binary) % 8 != 0:
            return f"⚠️ Corrupted message: binary length not multiple of 8."

        return binary_to_text(binary)
    except Exception as e:
        return f"❌ Error during decoding: {e}"

# --- GUI Logic ---
def show_main_menu():
    clear_window()

    tk.Label(root, text="Whitespace Steganography", font=("Arial", 18, "bold")).pack(pady=20)
    tk.Button(root, text="Encode Message", width=30, height=2, command=show_encode_screen).pack(pady=10)
    tk.Button(root, text="Decode Message", width=30, height=2, command=show_decode_screen).pack(pady=10)

def show_encode_screen():
    clear_window()

    tk.Label(root, text="Encode Message", font=("Arial", 16, "bold")).pack(pady=10)

    tk.Label(root, text="Cover Text:").pack()
    global cover_entry
    cover_entry = tk.Entry(root, width=80)
    cover_entry.pack()

    tk.Label(root, text="Secret Message:").pack(pady=(10, 0))
    global secret_entry
    secret_entry = tk.Entry(root, width=80)
    secret_entry.pack()

    tk.Button(root, text="Encode", command=perform_encoding).pack(pady=10)

    global output_text
    output_text = scrolledtext.ScrolledText(root, width=72, height=10, wrap=tk.WORD)
    output_text.pack()

    tk.Button(root, text="Copy Encoded Message", command=copy_to_clipboard).pack(pady=5)
    tk.Button(root, text="⬅ Back", command=show_main_menu).pack(pady=(10, 0))

def show_decode_screen():
    clear_window()

    tk.Label(root, text="Decode Message", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(root, text="Paste the encoded message (with [hidden] ... [end])").pack()

    global output_text
    output_text = scrolledtext.ScrolledText(root, width=72, height=12, wrap=tk.WORD)
    output_text.pack()

    tk.Button(root, text="Decode", command=perform_decoding).pack(pady=10)
    tk.Button(root, text="⬅ Back", command=show_main_menu).pack()

def perform_encoding():
    cover = cover_entry.get()
    secret = secret_entry.get()
    if not cover or not secret:
        messagebox.showwarning("Missing Input", "Enter both cover and secret messages.")
        return
    stego = encode_message(cover, secret)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, stego)

def perform_decoding():
    stego = output_text.get(1.0, tk.END)
    result = decode_message(stego)
    messagebox.showinfo("Decoded Message", result)

def copy_to_clipboard():
    text = output_text.get(1.0, tk.END)
    if not text.strip():
        messagebox.showwarning("Empty", "Nothing to copy.")
        return
    root.clipboard_clear()
    root.clipboard_append(text)
    messagebox.showinfo("Copied", "Encoded message copied to clipboard.")

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# --- GUI Setup ---
root = tk.Tk()
root.title("Whitespace Steganography")
root.geometry("650x500")
root.resizable(False, False)

show_main_menu()
root.mainloop()
=======
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
>>>>>>> a00588b67eeb4421657e50048f418d17e2fd32f0

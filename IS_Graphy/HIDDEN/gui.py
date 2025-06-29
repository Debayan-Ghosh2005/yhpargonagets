import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont
import pytesseract
import os

# Set your Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# --- Encode function ---
def hide_message():
    filepath = filedialog.askopenfilename(title="Select Image")
    if not filepath:
        return
    message = entry_message.get()
    if not message:
        messagebox.showwarning("Empty Message", "Please enter a message to hide.")
        return

    image = Image.open(filepath).convert("RGBA")
    txt_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()

    draw.text((50, 50), message, font=font, fill=(255, 255, 255, 100))  # Visible but subtle

    result = Image.alpha_composite(image, txt_layer)

    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    if save_path:
        result.save(save_path)
        messagebox.showinfo("Success", f"Message hidden and saved to:\n{save_path}")

# --- Decode function ---
def extract_message():
    filepath = filedialog.askopenfilename(title="Select Encoded Image")
    if not filepath:
        return

    image = Image.open(filepath).convert("RGBA")
    width, height = image.size
    extracted = Image.new("RGBA", (width, height))

    for x in range(width):
        for y in range(height):
            r, g, b, a = image.getpixel((x, y))
            if 90 <= a <= 120:
                extracted.putpixel((x, y), (255, 255, 255, 255))
            else:
                extracted.putpixel((x, y), (0, 0, 0, 255))

    gray = extracted.convert("L")
    gray.save("extracted_hidden_text.png")

    text = pytesseract.image_to_string(gray, config='--psm 6').strip()
    entry_decoded.delete(0, tk.END)
    entry_decoded.insert(0, text)

# --- GUI Setup ---
root = tk.Tk()
root.title("Steganography Encoder & Decoder")
root.geometry("500x300")
root.resizable(False, False)

tk.Label(root, text="Message to Hide:", font=("Arial", 12)).pack(pady=5)
entry_message = tk.Entry(root, width=50)
entry_message.pack(pady=5)

tk.Button(root, text="🔐 Encode Image", command=hide_message, width=20).pack(pady=10)
tk.Button(root, text="🔓 Decode Message", command=extract_message, width=20).pack(pady=10)

tk.Label(root, text="Decoded Message:", font=("Arial", 12)).pack(pady=5)
entry_decoded = tk.Entry(root, width=50)
entry_decoded.pack(pady=5)

root.mainloop()

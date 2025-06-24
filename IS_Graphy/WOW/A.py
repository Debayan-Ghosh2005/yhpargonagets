import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import imageio.v3 as iio
from skimage import img_as_float
from scipy.signal import convolve2d
import os

# ---------- WOW COST FUNCTION ----------
def compute_rho_WOW(image):
    filters = [
        np.array([[1, -1]]),
        np.array([[1], [-1]]),
        np.array([[1, 0], [0, -1]])
    ]
    rho = np.zeros_like(image)
    for filt in filters:
        residual = convolve2d(image, filt, mode='same', boundary='symm')
        abs_res = np.abs(residual)
        rho += 1.0 / (abs_res + 1e-5)
    return rho / np.max(rho)

# ---------- EMBEDDING & EXTRACTION ----------
def embed_message_uint8(image_uint8, message, costs):
    flat_img = image_uint8.flatten()
    flat_costs = costs.flatten()

    message_length = len(message)
    length_bits = f'{message_length:016b}'
    message_bits = length_bits + ''.join(f'{ord(c):08b}' for c in message)

    sorted_indices = np.argsort(flat_costs)

    for i, bit in enumerate(message_bits):
        idx = sorted_indices[i]
        pixel = flat_img[idx]
        if (pixel & 1) != int(bit):
            flat_img[idx] ^= 1  # Flip LSB

    return flat_img.reshape(image_uint8.shape), sorted_indices

def extract_message_uint8(image_uint8, sorted_indices):
    flat_img = image_uint8.flatten()

    # Get length first (16 bits)
    bits = ''
    for i in range(16):
        idx = sorted_indices[i]
        bits += str(flat_img[idx] & 1)
    message_length = int(bits, 2)

    # Extract message
    bits = ''
    for i in range(16, 16 + message_length * 8):
        idx = sorted_indices[i]
        bits += str(flat_img[idx] & 1)

    chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
    return ''.join(chars)

# ---------- GUI ----------
class StegoGUI:
    def __init__(self, master):
        self.master = master
        master.title("WOW Steganography (RGB + Auto-Length + External Stego)")
        master.geometry("650x480")
        self.image = None
        self.gray_image = None
        self.costs = None
        self.gray_uint8 = None

        tk.Label(master, text="WOW Steganography GUI", font=("Arial", 16)).pack(pady=10)

        self.load_button = tk.Button(master, text="Load Cover Image (RGB or Gray)", command=self.load_image)
        self.load_button.pack(pady=5)

        self.message_entry = tk.Entry(master, width=50)
        self.message_entry.pack(pady=5)
        self.message_entry.insert(0, "Enter your secret message here")

        self.embed_button = tk.Button(master, text="Embed and Save Stego Image", command=self.embed)
        self.embed_button.pack(pady=5)

        tk.Label(master, text="------------------------------").pack(pady=5)

        self.load_stego_button = tk.Button(master, text="Load Existing Stego Image", command=self.load_stego_and_extract)
        self.load_stego_button.pack(pady=5)

        self.output_label = tk.Label(master, text="", font=("Arial", 12))
        self.output_label.pack(pady=10)

    def load_image(self):
        file_path = filedialog.askopenfilename(title="Select Cover Image")
        if file_path:
            image = iio.imread(file_path)
            if image.ndim == 3 and image.shape[2] == 3:
                gray = np.dot(image[..., :3], [0.299, 0.587, 0.114])
            else:
                gray = image if image.ndim == 2 else image[:, :, 0]
            gray_float = img_as_float(gray)
            self.gray_image = gray_float
            self.gray_uint8 = (gray_float * 255).astype(np.uint8)
            self.costs = compute_rho_WOW(gray_float)
            messagebox.showinfo("Success", "Cover image loaded and WOW cost map calculated.")

    def embed(self):
        if self.gray_image is None:
            messagebox.showerror("Error", "Load a cover image first.")
            return

        message = self.message_entry.get()
        if not message:
            messagebox.showerror("Error", "Enter a secret message.")
            return

        try:
            stego_uint8, sorted_indices = embed_message_uint8(self.gray_uint8.copy(), message, self.costs)
            output_dir = os.path.dirname(__file__)
            iio.imwrite(f"{output_dir}/stego_image.png", stego_uint8)
            np.save(f"{output_dir}/stego_order.npy", sorted_indices)
            messagebox.showinfo("Success", "Message embedded and saved as stego_image.png + stego_order.npy.")
        except Exception as e:
            messagebox.showerror("Embedding Failed", str(e))

    def load_stego_and_extract(self):
        file_path = filedialog.askopenfilename(title="Select Stego Image")
        if file_path:
            try:
                stego_uint8 = iio.imread(file_path, mode='L')
                sorted_indices_path = filedialog.askopenfilename(title="Select Matching stego_order.npy")
                if not sorted_indices_path.endswith(".npy"):
                    raise ValueError("You must select a valid .npy file.")
                sorted_indices = np.load(sorted_indices_path)
                message = extract_message_uint8(stego_uint8, sorted_indices)
                self.output_label.config(text=f"Recovered Message: {message}")
            except Exception as e:
                messagebox.showerror("Error", f"Extraction failed: {str(e)}")

# ---------- RUN ----------
if __name__ == "__main__":
    root = tk.Tk()
    gui = StegoGUI(root)
    root.mainloop()

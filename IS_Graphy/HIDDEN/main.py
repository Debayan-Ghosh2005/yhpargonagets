from PIL import Image, ImageDraw, ImageFont
import pytesseract
import numpy as np
import os

# === Tesseract OCR Path ===
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# === Path Setup ===
BASE_DIR = r"C:\Users\nirno\Codes\yhpargonagets\IS_Graphy"
INPUT_IMAGE = os.path.join(BASE_DIR, "apple.png")  # or use apple.png for final version
HIDDEN_DIR = os.path.join(BASE_DIR, "HIDDEN")
OUTPUT_IMAGE = os.path.join(HIDDEN_DIR, "a.png")
DEBUG_IMAGE = os.path.join(HIDDEN_DIR, "extracted_hidden_text.png")
CROPPED_IMAGE = os.path.join(HIDDEN_DIR, "cropped_text_region.png")
HELPER_MASK = os.path.join(HIDDEN_DIR, "hidden_mask.npy")

def hide_message(input_path, output_path, message):
    image = Image.open(input_path).convert("RGBA")
    txt_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    # Font
    try:
        font = ImageFont.truetype("arialbd.ttf", 50)
    except:
        font = ImageFont.load_default()

    x, y = 50, 50
    draw.text((x, y), message, font=font, fill=(255, 255, 255, 255))  # Full white text

    # Save mask where text was drawn
    mask = np.array(txt_layer)[:, :, 3] > 200  # alpha > 200 indicates text
    np.save(HELPER_MASK, mask)

    # Merge and save
    result = Image.alpha_composite(image, txt_layer)
    os.makedirs(HIDDEN_DIR, exist_ok=True)
    result.save(output_path)
    print(f"[✅] Message hidden in: {output_path}")
    print(f"[📁] Mask saved in: {HELPER_MASK}")

def extract_hidden_message(image_path, mask_path):
    image = Image.open(image_path).convert("RGBA")
    rgba = np.array(image)
    mask = np.load(mask_path)

    # Apply mask to extract only where text was hidden
    extracted = np.zeros_like(rgba)
    extracted[mask] = [255, 255, 255, 255]  # Text in white
    extracted[~mask] = [0, 0, 0, 255]       # Background in black

    # Convert to PIL and grayscale
    extracted_image = Image.fromarray(extracted, 'RGBA')
    gray = extracted_image.convert("L")
    thresholded = gray.point(lambda p: 255 if p > 100 else 0)

    # Save debug images
    thresholded.save(DEBUG_IMAGE)
    thresholded.save(CROPPED_IMAGE)

    print("[💾] Extracted text image saved.")
    text = pytesseract.image_to_string(thresholded, config='--psm 7')
    print("Decoded message:", text.strip())

# === 🧪 Run the pipeline ===
message_to_hide = "TEST HIDDEN 123"
hide_message(INPUT_IMAGE, OUTPUT_IMAGE, message_to_hide)
extract_hidden_message(OUTPUT_IMAGE, HELPER_MASK)

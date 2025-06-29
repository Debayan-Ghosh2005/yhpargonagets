from PIL import Image
import pytesseract

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_hidden_message(image_path):
    image = Image.open(image_path).convert("RGBA")
    width, height = image.size
    extracted_layer = Image.new("RGBA", (width, height))

    for x in range(width):
        for y in range(height):
            r, g, b, a = image.getpixel((x, y))
            if 90 <= a <= 120:  # Match the alpha used
                extracted_layer.putpixel((x, y), (255, 255, 255, 255))
            else:
                extracted_layer.putpixel((x, y), (0, 0, 0, 255))

    gray = extracted_layer.convert("L")
    gray.save("extracted_hidden_text.png")  # Optional debug image
    print("[💾] Extracted image saved.")

    text = pytesseract.image_to_string(gray, config='--psm 6')
    print("Decoded message:", text.strip())

# Run
extract_hidden_message(r"D:\Debayan\yhpargonagets\IS_Graphy\HIDDEN\A.png")

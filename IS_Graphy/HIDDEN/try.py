from PIL import Image, ImageDraw, ImageFont
import pytesseract

# Path to your working Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Create a simple image with visible text
img = Image.new("RGB", (300, 100), color=(0, 0, 0))
draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype("arial.ttf", 30)
except:
    font = ImageFont.load_default()

draw.text((10, 25), "Hello OCR", fill=(255, 255, 255), font=font)
img.save("ocr_test.png")
img.show()

# OCR test
text = pytesseract.image_to_string(img)
print("Extracted text:", repr(text))

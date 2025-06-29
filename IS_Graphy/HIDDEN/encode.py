from PIL import Image, ImageDraw, ImageFont
import os

def hide_message(input_path, output_path, message):
    image = Image.open(input_path).convert("RGBA")
    txt_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    try:
        font = ImageFont.truetype("arial.ttf", 24)  # Big for visibility
    except:
        font = ImageFont.load_default()

    x, y = 50, 50
    draw.text((x, y), message, font=font, fill=(255, 255, 255, 100))  # Alpha = 100 (visible)

    result = Image.alpha_composite(image, txt_layer)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    result.save(output_path)
    print(f"[✅] Message hidden in: {output_path}")

# Example usage
input_image = r"D:\Debayan\yhpargonagets\IS_Graphy\apple.png"
output_image = r"D:\Debayan\yhpargonagets\IS_Graphy\HIDDEN\A.png"
hide_message(input_image, output_image, "TEST HIDDEN 123")

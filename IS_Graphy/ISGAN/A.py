from PIL import Image, ImageDraw, ImageFont
import os

def hide_message(input_path, output_path, message):
    # Load the original image
    image = Image.open(input_path).convert("RGBA")

    # Create a transparent layer same size as the original
    txt_layer = Image.new("RGBA", image.size, (255,255,255,0))
    draw = ImageDraw.Draw(txt_layer)

    # Choose a font and size
    try:
        font = ImageFont.truetype("arial.ttf", 1)  # Small invisible font
    except:
        font = ImageFont.load_default()

    # Position to hide the message (e.g., bottom-right)
    x, y = image.size[0] - 100, image.size[1] - 30

    # Draw the text in nearly invisible color (alpha = 1)
    draw.text((x, y), message, font=font, fill=(0, 0, 0, 1))

    # Combine image and transparent message layer
    hidden_image = Image.alpha_composite(image, txt_layer)

    # Save final image
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    hidden_image.save(output_path, format="PNG")
    print(f"Message hidden and saved to: {output_path}")

# Example usage
input_image_path = r"D:\Debayan\yhpargonagets\IS_Graphy\apple.png"
output_image_path = r"D:\Debayan\yhpargonagets\IS_Graphy\HIDDEN\A.png"  # Must be .png not .py
message = "hey how are you"

hide_message(input_image_path, output_image_path, message)

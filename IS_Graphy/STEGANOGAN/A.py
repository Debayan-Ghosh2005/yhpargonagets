from steganogan import SteganoGAN
#from steganogan.utils import load_image, save_image
from PIL import Image
import torch

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load pretrained model (you can also train your own)
steganogan = SteganoGAN.load(architecture='dense')

# Paths
cover_image_path = 'cover.png'   # Replace with your image
output_image_path = 'stego.png'
message_to_hide = 'This is a secret message.'

# Encode message
steganogan.encode(cover_image_path, output_image_path, message_to_hide)

print(f"Message embedded and saved to: {output_image_path}")

# Decode message
stego_image_loaded = load_image(output_image_path)
extracted_message = steganogan.decode(stego_image_loaded)

print(f"Extracted message: {extracted_message}")

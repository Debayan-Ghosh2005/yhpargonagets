import numpy as np
import cv2
import os

def integer_haar_forward(img):
    """Integer Haar Wavelet Forward Transform with perfect reconstruction"""
    # Store original dimensions
    h, w = img.shape
    original_shape = (h, w)
    
    # Ensure even dimensions by padding if necessary
    h_padded = h if h % 2 == 0 else h + 1
    w_padded = w if w % 2 == 0 else w + 1
    
    if h != h_padded or w != w_padded:
        img_padded = np.pad(img, ((0, h_padded - h), (0, w_padded - w)), mode='edge')
    else:
        img_padded = img.copy()
    
    img_padded = img_padded.astype(np.int32)
    
    # Row processing
    s_rows = (img_padded[:, 0::2] + img_padded[:, 1::2]) // 2
    d_rows = img_padded[:, 0::2] - img_padded[:, 1::2]
    
    # Column processing
    LL = (s_rows[0::2] + s_rows[1::2]) // 2
    LH = s_rows[0::2] - s_rows[1::2]
    HL = (d_rows[0::2] + d_rows[1::2]) // 2
    HH = d_rows[0::2] - d_rows[1::2]
    
    return LL, (LH, HL, HH), original_shape

def integer_haar_inverse(LL, bands, original_shape):
    """Integer Haar Wavelet Inverse Transform with perfect reconstruction"""
    LH, HL, HH = bands
    h, w = LL.shape
    
    # Column inverse
    s_rows_top = LL + (LH + 1) // 2
    s_rows_bottom = s_rows_top - LH
    d_rows_top = HL + (HH + 1) // 2
    d_rows_bottom = d_rows_top - HH
    
    # Reconstruct row arrays
    s_rows = np.zeros((2*h, w), dtype=np.int32)
    s_rows[0::2] = s_rows_top
    s_rows[1::2] = s_rows_bottom
    
    d_rows = np.zeros((2*h, w), dtype=np.int32)
    d_rows[0::2] = d_rows_top
    d_rows[1::2] = d_rows_bottom
    
    # Row inverse
    img_left = s_rows + (d_rows + 1) // 2
    img_right = img_left - d_rows
    
    # Reconstruct full image - NO CLIPPING TO UINT8 HERE
    img = np.zeros((2*h, 2*w), dtype=np.int32)
    img[:, 0::2] = img_left
    img[:, 1::2] = img_right
    
    # Crop to original dimensions
    return img[:original_shape[0], :original_shape[1]]

class RobustIWTSteganography:
    def __init__(self):
        """Initialize robust IWT steganography"""
        self.message_delimiter = "###END###"
    
    def text_to_binary(self, text):
        """Convert text to binary with length prefix"""
        # Add delimiter to mark end
        text += self.message_delimiter
        
        # Encode message length (32 bits)
        length_bits = format(len(text), '032b')
        
        # Convert text to binary
        content_bits = ''.join(format(ord(char), '08b') for char in text)
        
        return length_bits + content_bits
    
    def binary_to_text(self, binary):
        """Convert binary to text with length prefix"""
        if len(binary) < 32:
            return ""
            
        # Extract message length (first 32 bits)
        length = int(binary[:32], 2)
        binary = binary[32:]
        
        # Extract only the required bits
        if len(binary) > length * 8:
            binary = binary[:length*8]
        
        # Convert to text
        text = ""
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                text += chr(int(byte, 2))
        
        # Remove delimiter
        if text.endswith(self.message_delimiter):
            return text[:-len(self.message_delimiter)]
        return text
    
    def embed_message(self, image_path, message, output_path=None):
        """Embed secret message with robust IWT"""
        # Load image
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError(f"Image not found: {image_path}")
        
        # Convert message to binary with length prefix
        msg_binary = self.text_to_binary(message)
        msg_length = len(msg_binary)
        
        # Apply Integer Haar Transform
        cA, (cH, cV, cD), original_shape = integer_haar_forward(img)
        
        # Store original shapes for reshaping later
        orig_shapes = {
            'cD': cD.shape,
            'cV': cV.shape,
            'cH': cH.shape,
            'cA': cA.shape
        }
        
        # Flatten coefficients
        coeffs = [cD.ravel(), cV.ravel(), cH.ravel(), cA.ravel()]
        total_capacity = sum(len(c) for c in coeffs)
        
        if msg_length > total_capacity:
            raise ValueError(f"Message too large. Max: {total_capacity} bits")
        
        # Embed message in coefficients
        msg_index = 0
        for coeff_array in coeffs:
            for i in range(len(coeff_array)):
                if msg_index >= msg_length:
                    break
                # Embed by modifying LSB
                coeff_array[i] = (coeff_array[i] & ~1) | int(msg_binary[msg_index])
                msg_index += 1
            if msg_index >= msg_length:
                break
        
        # Reshape coefficients - FIXED: reshape each array individually
        cD_new = coeffs[0].reshape(orig_shapes['cD'])
        cV_new = coeffs[1].reshape(orig_shapes['cV'])
        cH_new = coeffs[2].reshape(orig_shapes['cH'])
        cA_new = coeffs[3].reshape(orig_shapes['cA'])
        
        # Inverse transform - FIXED: pass original shape
        stego_img = integer_haar_inverse(cA_new, (cH_new, cV_new, cD_new), original_shape)
        
        # Save and return (convert to uint8 only when saving)
        if output_path:
            # Clip to valid range and convert to uint8 for saving
            stego_img_uint8 = np.clip(stego_img, 0, 255).astype(np.uint8)
            cv2.imwrite(output_path, stego_img_uint8)
        return stego_img
    
    def extract_message(self, stego_image_path):
        """Extract hidden message from stego image"""
        # Load stego image
        stego_img = cv2.imread(stego_image_path, cv2.IMREAD_GRAYSCALE)
        if stego_img is None:
            raise ValueError(f"Image not found: {stego_image_path}")
        
        # Apply Integer Haar Transform
        cA, (cH, cV, cD), _ = integer_haar_forward(stego_img.astype(np.int32))
        
        # Extract bits from coefficients in the same order as embedding
        coeffs = [cD.ravel(), cV.ravel(), cH.ravel(), cA.ravel()]
        extracted_bits = []
        
        for coeff_array in coeffs:
            for coeff in coeff_array:
                extracted_bits.append(str(coeff & 1))
        
        binary_str = ''.join(extracted_bits)
        
        # Convert to text using length prefix
        return self.binary_to_text(binary_str)
    
    def calculate_psnr(self, original_path, stego_path):
        """Calculate PSNR between original and stego images"""
        original = cv2.imread(original_path, cv2.IMREAD_GRAYSCALE)
        stego = cv2.imread(stego_path, cv2.IMREAD_GRAYSCALE)
        
        if original is None or stego is None:
            raise ValueError("Could not load one or both images")
        
        if original.shape != stego.shape:
            stego = cv2.resize(stego, (original.shape[1], original.shape[0]))
        
        mse = np.mean((original.astype(float) - stego.astype(float)) ** 2)
        if mse == 0:
            return float('inf')
        
        max_pixel = 255.0
        psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
        return psnr

# Example usage
def main():
    stego_system = RobustIWTSteganography()
    
    cover_image = "apple.jpg"
    stego_image = "apple_stego.png"  # Use PNG for lossless compression
    secret_message = "Hello this is Subhradeep Kar"
    
    try:
        print("Embedding message...")
        stego_img = stego_system.embed_message(cover_image, secret_message, stego_image)
        print("Message embedded successfully!")
        
        print("Extracting message...")
        extracted = stego_system.extract_message(stego_image)
        print(f"Extracted message: {extracted}")
        
        psnr = stego_system.calculate_psnr(cover_image, stego_image)
        print(f"PSNR: {psnr:.2f} dB")
        
        if extracted == secret_message:
            print("✓ Message extraction successful - 100% accuracy!")
        else:
            print("✗ Message extraction failed")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

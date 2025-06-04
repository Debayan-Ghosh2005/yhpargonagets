"""
3DES Encryption/Decryption
Triple DES (3DES) is a symmetric encryption algorithm. Unlike ECC which is public-key, 3DES uses the same key for encryption and decryption. It applies the DES cipher three times to each block of data.
Encrypt with Key1
Decrypt with Key2
Encrypt with Key3
(This is called Encrypt-Decrypt-Encrypt, or EDE mode)
It increases the security of original DES.
"""

# === 3DES (Triple DES) Encryption and Decryption Example ===
# Install pycryptodome: pip install pycryptodome

from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# 1. --- MESSAGE TO ENCRYPT ---
message = b"This is a secret message!"
# Must be bytes. If using string, convert using .encode()

# 2. --- GENERATE A RANDOM 24-BYTE (192-BIT) KEY ---
# Triple DES uses 3 keys of 8 bytes each → total 24 bytes
key = DES3.adjust_key_parity(get_random_bytes(24))
# DES keys must have "odd parity" in each byte. adjust_key_parity ensures that.

# 3. --- GENERATE A RANDOM 8-BYTE IV (Initialization Vector) ---
iv = get_random_bytes(8)
# IV adds randomness so same message encrypted multiple times gives different ciphertext.

# 4. --- CREATE CIPHER OBJECT FOR ENCRYPTION ---
cipher_encrypt = DES3.new(key, DES3.MODE_CBC, iv)
# We use CBC (Cipher Block Chaining) mode here.

# 5. --- ENCRYPT THE MESSAGE ---
# We must pad the message to multiple of 8 bytes (DES block size)
ciphertext = cipher_encrypt.encrypt(pad(message, DES3.block_size))

print("Original Message:", message)
print("Encrypted (hex):", ciphertext.hex())
print("Key (hex):", key.hex())
print("IV (hex):", iv.hex())

# === Now Decrypt the Message ===

# 6. --- CREATE CIPHER OBJECT FOR DECRYPTION (must use same key & IV) ---
cipher_decrypt = DES3.new(key, DES3.MODE_CBC, iv)

# 7. --- DECRYPT AND UNPAD THE MESSAGE ---
decrypted = unpad(cipher_decrypt.decrypt(ciphertext), DES3.block_size)

print("Decrypted Message:", decrypted)

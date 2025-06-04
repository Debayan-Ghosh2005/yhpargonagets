"""
Blowfish
Glossary of Terms
Blowfish: A symmetric block cipher that works on 64‐bit blocks (8 bytes at a time) with a key up to 448 bits long.
Feistel Cipher: A design where each round splits the 64‐bit input into two 32‐bit halves (L and R), applies a special “F‐function” to one half, then XORs with the other half, and swaps them. After all rounds, the halves are recombined.
S-Box (Substitution Box): A lookup table (256 entries of 32 bits) that makes encryption non‐linear (harder to break).
P‐Array (Permutation Array): A series of 18 32‐bit subkeys used in each round.
CBC (Cipher Block Chaining) Mode: As with AES, encrypt each block after XORing it with the previous ciphertext block (or IV for the first block).
Padding: Because Blowfish’s block size is 8 bytes, messages not a multiple of 8 need padding (PKCS#7 padding works similarly—add N bytes of value N).
"""

# === Blowfish Encryption and Decryption Example ===
# Install pycryptodome before running: pip install pycryptodome

from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# 1. --- KEY GENERATION ---
# Blowfish keys can be anywhere from 32 bits (4 bytes) up to 448 bits (56 bytes).
# Here we choose a 128-bit key (16 bytes) for simplicity.
key = get_random_bytes(16)  # 16 bytes = 128 bits

# 2. --- DEFINE BLOCK SIZE AND IV ---
# Blowfish.block_size is 8 bytes (64 bits).
bs = Blowfish.block_size  # bs = 8 in this case
# We also need an 8-byte IV for CBC mode.
iv = get_random_bytes(bs)

# 3. --- CREATE CIPHER OBJECT FOR ENCRYPTION (CBC MODE) ---
cipher_encrypt = Blowfish.new(key, Blowfish.MODE_CBC, iv)

# 4. --- PREPARE PLAINTEXT AND PAD IT ---
plaintext = b"Top secret info!"
# Pad plaintext to a multiple of 8 bytes with PKCS#7 padding.
padded_plaintext = pad(plaintext, bs)

# 5. --- ENCRYPT THE PADDED PLAINTEXT ---
ciphertext = cipher_encrypt.encrypt(padded_plaintext)
print("Blowfish ciphertext (hex):", ciphertext.hex())

# 6. --- CREATE CIPHER OBJECT FOR DECRYPTION ---
cipher_decrypt = Blowfish.new(key, Blowfish.MODE_CBC, iv)

# 7. --- DECRYPT THE CIPHERTEXT ---
decrypted_padded = cipher_decrypt.decrypt(ciphertext)

# 8. --- REMOVE PADDING TO GET ORIGINAL PLAINTEXT ---
decrypted = unpad(decrypted_padded, bs)
print("Blowfish decrypted plaintext:", decrypted.decode())

# ===== Summary =====
# 1. We chose a random 128-bit key and 8-byte IV.
# 2. Blowfish operates on 8-byte blocks, so we padded our message to a multiple of 8.
# 3. In CBC mode, each plaintext block is XORed with the previous ciphertext block (or IV) before encryption.
# 4. To decrypt, we reverse the process and then remove padding.

# IMPORTANT NOTES FOR REAL USAGE:
# - Because the block size is only 8 bytes, encrypting large streams of data under one key risks “birthday attacks” 
#   (once you encrypt ~2^32 blocks ≈ 34 GB, you might see block collisions). 
# - In modern practice, AES (with 128-bit blocks) is preferred over Blowfish for most new systems.

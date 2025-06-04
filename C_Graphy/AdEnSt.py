"""
AES (Advanced Encryption Standard)
Glossary of Terms
AES: A “secret‐key” cipher (same key to lock and unlock) that works on 128‐bit data blocks.
Block cipher: Encrypts fixed‐size chunks (blocks) of data (here, 16 bytes per block).
Key: A secret string of bytes that you and your friend both know—used to lock (encrypt) and unlock (decrypt) messages.
IV (Initialization Vector): A random “starter” value that guarantees two identical messages encrypted with the same key still yield different encrypted outputs.
Plaintext: The original human‐readable message (e.g., "Hello!") before encryption.
Ciphertext: The “scrambled” version of the plaintext, unreadable without the key.
Padding: When your message isn’t a multiple of 16 bytes, we add extra bytes so it fits perfectly into 16‐byte blocks (PKCS#7 is one popular padding method).
CBC (Cipher Block Chaining): A mode where each plaintext block is XORed (combined) with the previous ciphertext block (or the IV for the first block) before applying AES. This links (“chains”) blocks together, making patterns harder to detect.
"""

# === AES Encryption and Decryption Example ===
# Install pycryptodome before running: pip install pycryptodome

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# 1. --- KEY AND IV GENERATION ---
# A "key" is a secret that both the sender and receiver share.
# Here we choose a 256-bit key (32 bytes). You could also use 16 bytes (128-bit) or 24 bytes (192-bit).
key = get_random_bytes(32)
# We also choose a random “IV” (Initialization Vector). Because AES works on 16-byte blocks,
# the IV must also be 16 bytes long.
iv = get_random_bytes(16)

# 2. --- CREATE CIPHER OBJECT FOR ENCRYPTION ---
# AES.new(key, mode, IV) sets up AES in “CBC” mode (Cipher Block Chaining).
#   - key: the secret key
#   - AES.MODE_CBC: we choose CBC mode
#   - iv: the random 16-byte initialization vector
cipher_encrypt = AES.new(key, AES.MODE_CBC, iv)

# 3. --- PREPARE PLAINTEXT AND PAD IT ---
# “Plaintext” is the normal message we want to keep secret.
plaintext = b"Attack at dawn!"  # b"" means “this is a bytes object” in Python.

# AES works on blocks of exactly 16 bytes. If the message isn’t a multiple of 16 bytes,
# we need to “pad” it so that its length becomes a multiple of 16. PKCS#7 padding
# appends a certain number of bytes, each containing the value of how many padding bytes we added.
padded_plaintext = pad(plaintext, AES.block_size)
# After padding:
#   If plaintext was 14 bytes (like "Attack at dawn!"), AES.block_size is 16, so we add 2 bytes of padding.
#   Each padding byte has value 0x02 (decimal 2). So padded_plaintext ends up 16 bytes long.

# 4. --- ENCRYPT THE PADDED PLAINTEXT ---
# The “encrypt” method takes the padded plaintext and returns the ciphertext (scrambled bytes).
ciphertext = cipher_encrypt.encrypt(padded_plaintext)
print("Ciphertext (hex):", ciphertext.hex())
# We use .hex() to show the ciphertext as a readable string of hex digits.

# 5. --- CREATE CIPHER OBJECT FOR DECRYPTION ---
# To decrypt, we need the same key and IV. We set up a new AES object in CBC mode with the same key & IV.
cipher_decrypt = AES.new(key, AES.MODE_CBC, iv)

# 6. --- DECRYPT THE CIPHERTEXT ---
decrypted_padded = cipher_decrypt.decrypt(ciphertext)
# Now “decrypted_padded” still has the PKCS#7 padding in it.

# 7. --- REMOVE PADDING TO RECOVER ORIGINAL PLAINTEXT ---
# unpad() removes the PKCS#7 padding and returns the original plaintext.
decrypted = unpad(decrypted_padded, AES.block_size)
print("Decrypted plaintext:", decrypted.decode())
# .decode() converts bytes back to a human‐readable string.

# ===== Summary =====
# 1. We generated a random 256-bit key and 16-byte IV.
# 2. We padded our plaintext so its length is a multiple of 16 bytes.
# 3. We used AES in CBC mode to encrypt the padded plaintext → ciphertext.
# 4. We re-created the AES cipher with the same key & IV to decrypt the ciphertext.
# 5. We removed padding to get back the original message.

# IMPORTANT NOTES FOR REAL USAGE:
# - Always send the IV in plaintext along with the ciphertext (so the receiver knows what IV was used). 
#   The IV is not secret—only the key is secret.
# - Never reuse the same (key, IV) pair to encrypt two different messages, or an attacker could detect patterns.
# - Use authenticated encryption (e.g., AES-GCM) in real systems to protect both confidentiality and integrity.

"""
RSA (Rivest–Shamir–Adleman)
Glossary of Terms
RSA: A way to lock/unlock messages with a pair of keys—one public, one private. People worldwide can encrypt a message with your public key, but only you (with the private key) can decrypt it.
Public Key: A key you share freely; anyone can use it to encrypt a message destined for you.
Private Key: Your secret key—only you should know this. Used to decrypt messages encrypted with your public key.
Encryption: The act of hiding (scrambling) a message so no one can read it without the correct key.
Decryption: The act of unscrambling a message back to readable form.
OAEP (Optimal Asymmetric Encryption Padding): A padding scheme that secures RSA against certain “chosen ciphertext” attacks. It mixes the message with random bits before encrypting.
Ciphertext: The scrambled output after encryption—appears as random bytes without the private key.
Exponent (e, d): RSA uses two numbers:
e (public exponent): Part of the public key—used to encrypt.
d (private exponent): Part of the private key—used to decrypt.
Modulus (n): A large number (product of two primes p and q) that helps define the RSA math. Included in both public & private keys.
"""

# === RSA Encryption and Decryption Example ===
# Install pycryptodome before running: pip install pycryptodome

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# 1. --- GENERATE RSA KEY PAIR ---
# RSA.generate(2048) creates a new RSA key (public + private) that’s 2048 bits long.
#   - 2048 bits is considered secure in 2025. (You could choose 3072 or 4096 bits for more security.)
rsa_key = RSA.generate(2048)

# Extract the private key (contains the “d” exponent) and the public key (contains “e”).
private_key = rsa_key           # This holds both p, q, d, etc.
public_key = rsa_key.publickey()  # We extract just (n, e).

# 2. --- SHOW KEY PROPERTIES (FOR LEARNING PURPOSES) ---
print("Public key modulus (n) size in bits:", public_key.size_in_bits())
# public_key.size_in_bits() tells us how long the modulus n is (e.g., 2048 bits).

# 3. --- PREPARE MESSAGE TO ENCRYPT ---
message = b"Hello, RSA!"
# Plaintext must be bytes.

# 4. --- ENCRYPT WITH PUBLIC KEY (RSA + OAEP PADDING) ---
# PKCS1_OAEP.new(public_key) sets up the RSA cipher with OAEP padding.
cipher_encrypt = PKCS1_OAEP.new(public_key)

# .encrypt(plaintext) returns ciphertext (scrambled bytes).
ciphertext = cipher_encrypt.encrypt(message)
print("Ciphertext (hex):", ciphertext.hex())
# hex() shows ciphertext as a string of hexadecimal digits.

# 5. --- DECRYPT WITH PRIVATE KEY ---
cipher_decrypt = PKCS1_OAEP.new(private_key)
# We decrypt using the same OAEP scheme.
decrypted_message = cipher_decrypt.decrypt(ciphertext)

# 6. --- SHOW DECRYPTED PLAINTEXT ---
print("Decrypted message:", decrypted_message.decode())
# .decode() turns bytes back into a readable string.

# ===== Summary =====
# 1. Generate a 2048-bit RSA key pair (public + private).
# 2. Use the PUBLIC key + OAEP padding to encrypt a short message into ciphertext.
# 3. Use the PRIVATE key + OAEP padding to decrypt ciphertext back into the original message.
# 4. Always keep the private key secret. The public key can be shared with anyone who wants to send you encrypted messages.

# IMPORTANT NOTES FOR REAL USAGE:
# - RSA is slow for large data. In practice, you encrypt a random “session key” (e.g., a 256-bit AES key) with RSA,
#   then you use that session key to encrypt the actual large message using a fast symmetric cipher (like AES). 
#   This is called a “hybrid” scheme.
# - Always use OAEP (or a similarly secure padding) with RSA. Never use “textbook RSA” without padding.

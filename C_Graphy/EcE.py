"""
===============================================================================
  Elliptic Curve Cryptography (ECC) –– Combined Example
===============================================================================

This file is split into two main sections:

1. ECDH (Elliptic Curve Diffie-Hellman) Key Exchange using the `cryptography` library.
2. ECDSA (Elliptic Curve Digital Signature Algorithm) Sign + Verify using PyCryptodome.

Glossary (all terms in **bold** appear later in the code with exactly that name):
-------------------------------------------------------------------------------
- **Elliptic Curve Cryptography (ECC)**: 
    A “public‐key” system that uses points on a special mathematical curve
    (y² = x³ + a·x + b mod p). Compared to RSA, ECC gives equally strong security
    with much smaller keys.

- **Curve (e.g., “SECP256R1” / “P-256”)**: 
    A specific equation of the form y² = x³ + a·x + b over a finite field (mod p).
    “P-256” (also called “SECP256R1”) is the most common 128-bit security curve.

- **Private Key (d)**: 
    A random, large integer chosen by you and kept secret. In ECC, this is usually
    a number between 1 and (curve_order – 1).

- **Public Key (Q = d·G)**: 
    The result of “point-multiplying” a fixed **generator point** G (on the curve) by
    your private integer d. Everyone can see Q, but they cannot recover d from Q
    without solving the hard Elliptic Curve Discrete Log Problem (ECDLP).

- **Point Multiplication (d·G)**: 
    You start with G (a well-known point on the curve). Then you “add” G to itself
    d times, using elliptic-curve addition rules. This yields another point Q. 
    Going backward (recovering d from Q given G) is computationally infeasible.

- **ECDH (Elliptic Curve Diffie-Hellman)**:
    A protocol for **two parties** (Alice & Bob) to agree on a single shared secret
    (a sequence of bytes) without ever sending their private keys over the network.
    Each side multiplies the other’s public point by its own private integer → same
    shared point. Then both hash that shared point to get a symmetric key.

- **ECDSA (Elliptic Curve Digital Signature Algorithm)**:
    A method that lets one party (the signer) create a short “digital signature”
    on a message. Anyone with the signer’s public key can verify authenticity and
    integrity. If the signature verifies, it means the message came from that
    private-key holder and has not been tampered with.

-------------------------------------------------------------------------------
Section 1: ECDH Key Exchange with `cryptography`
-------------------------------------------------------------------------------
"""

# Install instructions (run once in your shell/PowerShell/Terminal):
#     pip install cryptography

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

# ------------------------------------------------------------------------------
# 1. ALICE GENERATES HER ECC KEY PAIR (Curve: SECP256R1 / P-256)
# ------------------------------------------------------------------------------
# - The private key (a random integer d_A) is stored inside alice_private_key.
# - The corresponding public key Q_A = d_A · G (a point on the curve) is obtained via .public_key().
alice_private_key = ec.generate_private_key(ec.SECP256R1())
alice_public_key = alice_private_key.public_key()

# ------------------------------------------------------------------------------
# 2. BOB GENERATES HIS ECC KEY PAIR (Same Curve: P-256)
# ------------------------------------------------------------------------------
bob_private_key = ec.generate_private_key(ec.SECP256R1())
bob_public_key = bob_private_key.public_key()

# ------------------------------------------------------------------------------
# 3. ALICE COMPUTES THE SHARED SECRET
# ------------------------------------------------------------------------------
# - ECDH: Alice takes her private integer d_A and multiplies it by Bob’s public point Q_B.
#   In code, that is: alice_private_key.exchange(ec.ECDH(), bob_public_key).
# - The result is “raw_shared_bytes_A” (the x-coordinate of the shared point, in bytes).
raw_shared_bytes_A = alice_private_key.exchange(ec.ECDH(), bob_public_key)

# ------------------------------------------------------------------------------
# 4. BOB COMPUTES THE SHARED SECRET
# ------------------------------------------------------------------------------
# - Bob takes his private integer d_B and multiplies it by Alice’s public point Q_A.
# - He also ends up with the very same byte string (raw_shared_bytes_B).
raw_shared_bytes_B = bob_private_key.exchange(ec.ECDH(), alice_public_key)

# ------------------------------------------------------------------------------
# 5. VERIFY BOTH RAW SHARED SECRETS MATCH
# ------------------------------------------------------------------------------
assert raw_shared_bytes_A == raw_shared_bytes_B, "ECDH mismatch! They must be identical."

# ------------------------------------------------------------------------------
# 6. DERIVE A 256-BIT SYMMETRIC KEY VIA HKDF (Recommended KDF) – instead of raw SHA-256
# ------------------------------------------------------------------------------
# Why a KDF? 
#   - Raw shared ECDH bytes are not “uniformly random” enough to serve directly as an AES key.
#   - HKDF (HMAC-based KDF) expands & “extracts” them into a fully uniform 256-bit key.
#
# Both sides must agree on:
#   - A hash function (here SHA-256).
#   - A salt (optional; can be None for a simpler example).
#   - An “info” string (contextual data; can be b'handshake data' or similar).
#
# Alice’s derived key:
hkdf_alice = HKDF(
    algorithm=hashes.SHA256(),
    length=32,             # → 32 bytes = 256 bits
    salt=None,             # For a stronger real-world system, use a random salt (shared/known).
    info=b'handshake data',# Optional “info” context; both sides must use the same info.
)
aes_key_alice = hkdf_alice.derive(raw_shared_bytes_A)

# Bob’s derived key (must use the exact same HKDF parameters):
hkdf_bob = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'handshake data',
)
aes_key_bob = hkdf_bob.derive(raw_shared_bytes_B)

# ------------------------------------------------------------------------------
# 7. CHECK THAT BOTH DERIVED AES KEYS ARE IDENTICAL
# ------------------------------------------------------------------------------
print("AES Key (Alice) =", aes_key_alice.hex())
print("AES Key (Bob)   =", aes_key_bob.hex())
print("Keys Match?     →", aes_key_alice == aes_key_bob)


"""
===============================================================================
Section 2: ECDSA (Signing + Verification) with PyCryptodome
===============================================================================
"""

# Install instructions (run once in your shell/PowerShell/Terminal):
#     pip install pycryptodome

from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256

# ------------------------------------------------------------------------------
# 1. SIGNER (Alice, say) GENERATES AN ECC KEY PAIR FOR SIGNING
# ------------------------------------------------------------------------------
# - This private key (signer_key.d) will be used for generating a digital signature.
# - The public key (signer_key.public_key()) is shared with anyone who wants to verify.
signer_key = ECC.generate(curve="P-256")
signer_public_key = signer_key.public_key()

# ------------------------------------------------------------------------------
# 2. PREPARE A MESSAGE TO SIGN
# ------------------------------------------------------------------------------
message = b"Hello, this is a message to sign with ECDSA."
# We always hash the message before signing (SHA-256 produces a 32-byte digest).
hash_obj = SHA256.new(message)

# ------------------------------------------------------------------------------
# 3. CREATE ECDSA SIGNER OBJECT (DSS) – specifying “fips-186-3”
# ------------------------------------------------------------------------------
# - DSS.new(...) wraps the ECC private key into an ECDSA signer following FIPS 186-3.
signer = DSS.new(signer_key, "fips-186-3")

# ------------------------------------------------------------------------------
# 4. PRODUCE THE DIGITAL SIGNATURE
# ------------------------------------------------------------------------------
# - signer.sign(hash_obj) runs the ECDSA algorithm on the hash.
# - The returned “signature” is a byte string (usually around 64-72 bytes for P-256).
signature = signer.sign(hash_obj)
print("\nECDSA Signature (hex):", signature.hex())

# ------------------------------------------------------------------------------
# 5. VERIFIER (Bob, say) RE-COMPUTES THE HASH OF THE MESSAGE
# ------------------------------------------------------------------------------
verify_hash = SHA256.new(message)

# ------------------------------------------------------------------------------
# 6. VERIFY THE SIGNATURE
# ------------------------------------------------------------------------------
# - DSS.new(signer_public_key, "fips-186-3") wraps the public point into a verifier.
verifier = DSS.new(signer_public_key, "fips-186-3")

try:
    verifier.verify(verify_hash, signature)
    print("Signature is valid! ✔ The message is authentic and untampered.")
except ValueError:
    print("Signature is invalid! ✖ The message may have been tampered or forged.")


"""
===============================================================================
  Explanation / Summary of What Just Happened
===============================================================================

● ECDH (Elliptic Curve Diffie-Hellman):
  1. Both Alice and Bob independently generate an ECC key pair (private d, public Q).
  2. Alice computes raw_shared_bytes_A = d_A × Q_B.
  3. Bob computes raw_shared_bytes_B = d_B × Q_A.
  4. Because the math is commutative on an elliptic curve, raw_shared_bytes_A == raw_shared_bytes_B.
  5. They both run the same HKDF (SHA-256) on that raw shared point → get the exact same 256-bit key.
  6. Now they can use that 256-bit key for AES, ChaCha20, HMAC, etc., knowing only they share it.

  ● Why not use SHA-256(raw_shared_bytes) directly?
    → In practice, it’s safer to use a proper KDF (e.g., HKDF) to “stretch” and uniformly randomize.
    → That way, any small biases in the raw shared bytes are “washed out,” and you can also derive
      multiple keys or add domain separation via the “info” parameter.

● ECDSA (Elliptic Curve Digital Signature Algorithm):
  1. The signer (Alice) has a private ECC key pair (d, Q).
  2. She hashes the message (SHA-256) → a 32-byte digest.
  3. She uses `DSS.new(private_key, "fips-186-3")` to get an ECDSA signer.
  4. Signing that hash yields a “signature” byte string.
  5. Anyone (Bob) with her public key (Q) can:
     - Recompute SHA-256(message).
     - Use `DSS.new(public_key, "fips-186-3")` to verify(signature).
     - If it passes, the message is guaranteed to come from the holder of that private key
       and has not been changed.

===============================================================================
Important Real-World Notes:
-------------------------------------------------------------------------------
1. Never use raw ECDH bytes as an AES key—always pass them through a secure KDF 
   (HKDF, X9.63-KDF, or similar).
2. When signing, consider using Deterministic ECDSA (RFC 6979) to avoid leaking
   private-key bits through poor randomness.
3. Always validate incoming ECC public keys (i.e., check they lie on the curve and 
   are not the point at infinity) before using them in ECDH or ECDSA verification.
4. Keep your private keys in a secure hardware module (HSM) or at minimum, a 
   password-encrypted file on disk.
===============================================================================
"""

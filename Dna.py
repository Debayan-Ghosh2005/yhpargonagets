# Define the corrected DNA encoding and 
# decoding dictionaries with unique mappings
encodingDict = {
    'A': 'AAA', 'B': 'AAC', 'C': 'AAG', 'D': 'AAT',
    'E': 'ACA', 'F': 'ACC', 'G': 'ACG', 'H': 'ACT',
    'I': 'AGA', 'J': 'AGC', 'K': 'AGG', 'L': 'AGT',
    'M': 'ATA', 'N': 'ATC', 'O': 'ATG', 'P': 'ATT',
    'Q': 'CAA', 'R': 'CAC', 'S': 'CAG', 'T': 'CAT',
    'U': 'CCA', 'V': 'CCC', 'W': 'CCG', 'X': 'CCT',
    'Y': 'CGA', 'Z': 'CGC', ' ': 'CGG'
}

decodingDict = {v: k for k, v in encodingDict.items()}

# Function to encrypt a message using DNA encoding
def encrypt(message):
    encrypted = ''
    for char in message:
        if char in encodingDict:
            encrypted += encodingDict[char]
        else:
            # If character is not in encodingDict
            # Placeholder for unknown characters
            encrypted += 'XXX'  
    return encrypted

# Function to decrypt a DNA-encoded message
def decrypt(encrypted):
    decrypted = ''

    # Read in chunks of 3
    for i in range(0, len(encrypted), 3):  
        triplet = encrypted[i:i+3]
        if triplet in decodingDict:
            decrypted += decodingDict[triplet]
        else:
            # Placeholder for unknown sequences
            decrypted += '?'  
    return decrypted
    
if __name__ == "__main__":
    message = "HELLO WORLD"
    print("Original Message:", message)
    
    # Encryption
    encryptedMessage = encrypt(message)
    print("Encrypted Message:", encryptedMessage)
    
    # Decryption
    decryptedMessage = decrypt(encryptedMessage)
    print("Decrypted Message:", decryptedMessage)
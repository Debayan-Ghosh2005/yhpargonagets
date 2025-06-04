# DNA Encoding and Decoding Dictionaries
# DNA steganography is the technique of hiding secret messages by encoding them within synthetic DNA sequences, making the message invisible or disguised within biological data.

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

# Encrypt a message using DNA encoding
def encrypt(message):
    encrypted = ''
    for char in message.upper():
        if char in encodingDict:
            encrypted += encodingDict[char]
        else:
            encrypted += 'XXX'  # Unknown character placeholder
    return encrypted

# Decrypt a DNA-encoded message
def decrypt(encrypted):
    decrypted = ''
    for i in range(0, len(encrypted), 3):
        triplet = encrypted[i:i+3]
        if triplet in decodingDict:
            decrypted += decodingDict[triplet]
        else:
            decrypted += '?'  # Unknown sequence placeholder
    return decrypted

if __name__ == "__main__":
    message = input("Enter the message to encode (A-Z, space only): ")
    
    encryptedMessage = encrypt(message)
    print("Encrypted Message:", encryptedMessage)

    decryptedMessage = decrypt(encryptedMessage)
    print("Decrypted Message:", decryptedMessage)
    
"""    OUTPUT EXAMPLE-
Enter the message to encode (A-Z, space only): HELLO WORLD
Encrypted Message: ACTACAAGTAGTAGGCCGATGATCACAGTAGA
Decrypted Message: HELLO WORLD """

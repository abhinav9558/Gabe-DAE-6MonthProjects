from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Generate a 128-bit AES encryption key (16 bytes).
# AES also supports 192-bit and 256-bit keys (24 and 32 bytes respectively).
key = get_random_bytes(16)

# Initialize the AES cipher in EAX mode, which provides both confidentiality and integrity.
cipher = AES.new(key, AES.MODE_EAX)

# Define the plaintext to be encrypted (must be in bytes).
plaintext = b"Hello world!"

# Encrypt the plaintext and generate an authentication tag.
ciphertext, tag = cipher.encrypt_and_digest(plaintext)

# Output encrypted values for reference.
print("Original Unencrypted Message: ", plaintext)
print("Encrypted message (ciphertext):", ciphertext)
print("Authentication tag:", tag)
print("Nonce:", cipher.nonce)

# --- Decryption Phase ---

# Reinitialize the cipher using the same key and nonce used during encryption.
cipher_dec = AES.new(key, AES.MODE_EAX, nonce=cipher.nonce)

# Decrypt the ciphertext and verify its integrity using the authentication tag.
decrypted = cipher_dec.decrypt_and_verify(ciphertext, tag)

# Output the decrypted plaintext.
print("Decrypted message (plaintext):", decrypted.decode())


import hashlib  # Standard Python library for hashing functions

# Define the input data to be hashed.
# This can be any string — e.g., a password, file contents, or message.
input_data = "FTPadmin123"

# Convert the input string to bytes.
# Hashing functions require byte input, not plain strings.
encoded_data = input_data.encode()

# Create a SHA-256 hash object and update it with the byte-encoded input.
# The hashing algorithm processes the data internally.
hash_object = hashlib.sha256(encoded_data)

# Retrieve the final hash value as a hexadecimal string.
# The hexdigest() method returns the result in readable format (64 characters for SHA-256).
hashed_output = hash_object.hexdigest()

# Output the resulting hash.
# This value is deterministic: the same input will always produce the same hash.
print("Original input:", input_data)
print("SHA-256 hash:  ", hashed_output)


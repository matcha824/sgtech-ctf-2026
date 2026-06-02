#!/usr/bin/env python3
"""
Key in C Minor - Solution Script (C-style implementation)
Brute-forces the first 28 bits of the AES-128 key using nested loops similar to C.
"""

import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Challenge data from challenge.json
encrypted_flag_hex = "cc818157d555903066386d07b7db51d842a05de9e8e432facc31822319d7813d"
iv_hex = "abababababababab0101010101010101"

# Known flag prefix for validation
flag_prefix = b"sgctf{"

# Known last 100 bits as hex (from challenge.json)
# This is bytes 3-15 of the key (with byte 3 having the bottom 4 bits)
# Pad with leading zero since 100 bits = 12.5 bytes = 25 hex chars (odd)
known_bytes = bytes.fromhex("0" + "b3c4d5e6f7890abcdef123456")

def hex_to_bytes(hex_str):
    """Convert hex string to bytes."""
    return bytes.fromhex(hex_str)

def pkcs7_unpad(data):
    """Remove PKCS7 padding."""
    if len(data) == 0:
        return data
    
    pad_len = data[-1]
    
    # Validate padding
    if pad_len == 0 or pad_len > 16:
        return data  # Invalid padding, return as-is
    
    # Check that all padding bytes are correct
    for i in range(len(data) - pad_len, len(data)):
        if data[i] != pad_len:
            return data  # Invalid padding, return as-is
    
    return data[:-pad_len]

def decrypt_and_check(key, iv, ciphertext):
    """
    Decrypt the ciphertext with the given key and check if it starts with the flag prefix.
    """
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext)
        plaintext = pkcs7_unpad(plaintext)
        
        if plaintext.startswith(flag_prefix):
            print(f"Key (hex): {key.hex()}")
            try:
                print(f"Decrypted flag: {plaintext.decode()}")
            except UnicodeDecodeError:
                print(f"Decrypted flag (hex): {plaintext.hex()}")
            return True
    except Exception as e:
        pass
    
    return False

def main():
    # Parse challenge data
    iv = hex_to_bytes(iv_hex)
    ciphertext = hex_to_bytes(encrypted_flag_hex)
    
    # DEBUG: Test with the known key first
    # The actual key is: 67ab1a2b3c4d5e6f7890abcdef123456
    # First 28 bits: byte0=0x67, byte1=0xab, byte2=0x1a, byte3_top=0x2
    print("DEBUG: Testing with known key...")
    test_key = bytearray(16)
    test_key[0] = 0x67
    test_key[1] = 0xab
    test_key[2] = 0x1a
    test_key[3] = (0x2 << 4) | (known_bytes[0] & 0x0F)
    for i in range(12):
        test_key[4 + i] = known_bytes[1 + i]
    
    print(f"DEBUG: Test key (hex): {bytes(test_key).hex()}")
    print(f"DEBUG: Expected key (hex): 67ab1a2b3c4d5e6f7890abcdef123456")
    
    # Test decryption with the known key
    if decrypt_and_check(bytes(test_key), iv, ciphertext):
        print("DEBUG: Successfully decrypted with known key!")
    else:
        print("DEBUG: Failed to decrypt with known key\n")
    
    print("Starting brute force of first 28 bits...")
    print(f"Total combinations: 2^28 = {1 << 28}")
    print("This may take a while...\n")
    
    # Doubly-nested loop to iterate through all 28-bit combinations
    # We iterate byte by byte for the first 3 bytes, then bit by bit for the last 4 bits
    count = 0
    
    for b0 in range(256):           # Byte 0: bits 0-7
        for b1 in range(256):       # Byte 1: bits 8-15
            for b2 in range(256):   # Byte 2: bits 16-23
                for b3_top in range(16):  # Top 4 bits of byte 3: bits 24-27
                    
                    count += 1
                    if count % 10000000 == 0:
                        progress = (count / (1 << 28)) * 100
                        print(f"Progress: {count} / 268435456 ({progress:.2f}%)")
                    
                    # Construct the full key
                    key = bytearray(16)
                    key[0] = b0
                    key[1] = b1
                    key[2] = b2
                    key[3] = (b3_top << 4) | (known_bytes[0] & 0x0F)  # Top 4 bits from brute force, bottom 4 bits from known
                    
                    # Copy the remaining known bytes
                    for i in range(12):
                        key[4 + i] = known_bytes[1 + i]
                    
                    # Decrypt and check
                    if decrypt_and_check(bytes(key), iv, ciphertext):
                        return
    
    print("Key not found!")

if __name__ == "__main__":
    main()

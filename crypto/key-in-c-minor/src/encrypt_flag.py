#!/usr/bin/env python3
"""
@Key in C Minor - Challenge Generator
Encrypts a flag with a constant 128-bit AES key and provides the last 100 bits of the key.
"""

import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

def encrypt_flag(flag: bytes, key: bytes):
    iv = bytes.fromhex("abababababababab0101010101010101")
    
    # Pad the flag to block size
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(flag) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    
    return iv, encrypted

def get_last_100_bits(key: bytes):
    key_int = int.from_bytes(key, byteorder='big')
    
    last_100_bits = key_int & ((1 << 100) - 1)
    
    binary_str = bin(last_100_bits)[2:].zfill(100)
    
    hex_str = format(last_100_bits, '025x')  # 100 bits = 12.5 bytes = 25 hex chars
    
    return binary_str, hex_str

def main():
    # Configuration
    FLAG = b"sgctf{g0tTa_brUt3_f4St}"
    # Constant AES key (128 bits = 16 bytes) - starts with 0000
    KEY = bytes.fromhex("67ab1a2b3c4d5e6f7890abcdef123456")
    
    # Encrypt flag
    iv, encrypted = encrypt_flag(FLAG, KEY)
    print(f"IV (hex): {iv.hex()}")
    print(f"Encrypted flag (hex): {encrypted.hex()}")
    print(f"Encrypted flag length: {len(encrypted)} bytes")
    
    # Extract last 100 bits of the key
    binary_str, hex_str = get_last_100_bits(KEY)
    print(f"Last 100 bits (binary): {binary_str}")
    print(f"Last 100 bits (hex): {hex_str}")
    
    # Save challenge data
    challenge_data = {
        "encrypted_flag": encrypted.hex(),
        "iv": iv.hex(),
        "last_100_bits_binary": binary_str,
        "last_100_bits_hex": hex_str
    }
    
    with open("challenge_data.json", "w") as f:
        json.dump(challenge_data, f, indent=2)
    
    print()
    print("Challenge data saved to challenge_data.json")

if __name__ == "__main__":
    main()

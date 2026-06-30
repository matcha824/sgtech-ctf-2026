#!/usr/bin/env python3
"""
Script to generate the encrypted flag for disassembly.c
This script implements the same encryption as the C program
"""

def encrypt(data):
    """Encrypt data using the same algorithm as disassembly.c"""
    result = bytearray(data)
    
    # Step 1: XOR every byte with 0x42
    for i in range(len(result)):
        result[i] ^= 0x42
    
    # Step 2: Subtract 0x10 from every byte with wrapping
    for i in range(len(result)):
        result[i] = (result[i] - 0x10) & 0xFF
    
    return bytes(result)

def main():
    flag = "sgctf{r3v3rS1ng_tH3_3nCrYpTi0n}"
    
    # Encrypt the flag
    encrypted = encrypt(flag.encode())
    
    # Print the encrypted flag as a C byte array
    print("Encrypted flag as C byte array:")
    print("unsigned char encryptedFlag[] = {")
    hex_values = [f"0x{b:02x}" for b in encrypted]
    for i in range(0, len(hex_values), 8):
        line = hex_values[i:i+8]
        print("    " + ", ".join(line) + ",")
    print("};")
    print(f"int encryptedFlagLen = {len(encrypted)};")
    
    print(f"\nEncrypted flag length: {len(encrypted)} bytes")
    print(f"Original flag: {flag}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

def decrypt(data):
    result = bytearray(data)
    
    # Reverse Step 2: Add 0x10 to every byte with wrapping
    for i in range(len(result)):
        result[i] = (result[i] + 0x10) & 0xFF
    
    # Reverse Step 1: XOR every byte with 0x42 (XOR is its own inverse)
    for i in range(len(result)):
        result[i] ^= 0x42
    
    return bytes(result)

def main():
    # Encrypted flag from disassembly
    encrypted_flag = bytes([
        0x21, 0x15, 0x11, 0x26, 0x14, 0x29, 0x20, 0x61,
        0x24, 0x61, 0x20, 0x01, 0x63, 0x1c, 0x15, 0x0d,
        0x26, 0xfa, 0x61, 0x0d, 0x61, 0x1c, 0xf1, 0x20,
        0x0b, 0x22, 0x06, 0x1b, 0x62, 0x1c, 0x2f,
    ])
    
    decrypted = decrypt(encrypted_flag)
    
    print(f"Decrypted flag: {decrypted.decode('utf-8')}")

if __name__ == "__main__":
    main()

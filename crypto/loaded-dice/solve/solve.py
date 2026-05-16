import random


def decrypt_flag():
    # Use the exact same seed from the vulnerable script
    random.seed(1337)

    with open("../flag.enc", "r") as f:
        encrypted_hex = f.read().strip()

    encrypted_bytes = bytes.fromhex(encrypted_hex)
    decrypted_flag = ""
    for byte in encrypted_bytes:
        random_byte = random.randint(0, 255)
        decrypted_flag += chr(byte ^ random_byte)

    print(f"Recovered Flag: {decrypted_flag}")


if __name__ == "__main__":
    decrypt_flag()

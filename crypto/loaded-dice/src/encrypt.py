import random


def encrypt_flag():
    # The house always sets the dice to the same starting position...
    random.seed(1337)

    with open("flag.txt", "r") as f:
        flag = f.read().strip()

    encrypted = []
    for char in flag:
        random_byte = random.randint(0, 255)
        encrypted.append(ord(char) ^ random_byte)

    with open("flag.enc", "w") as f:
        f.write(bytes(encrypted).hex())


if __name__ == "__main__":
    encrypt_flag()

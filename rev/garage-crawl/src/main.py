import os
import pathlib
import hashlib
import time
import sys


class SecureRand:
    _A = 1103515245
    _C = 12345
    _M = 1 << 31

    def __init__(self, seed: int):
        self.state = seed & 0xFFFFFFFF

    def next_int(self) -> int:
        self.state = (self._A * self.state + self._C) % self._M
        return (self.state >> 16) & 0x7FFF

    def next_bytes(self, n: int) -> bytes:
        return bytes(self.next_int() & 0xFF for _ in range(n))


def derive_ticket_code(entry_timestamp: int) -> str:
    rng = SecureRand(entry_timestamp)
    token = rng.next_bytes(16)
    digest = hashlib.md5(token).hexdigest()
    return digest[:16]


def format_barcode(seed: int) -> str:
    h = f"{seed:08X}"
    groups = f"{h[0:4]}-{h[4:8]}"
    checksum = sum(int(c, 16) for c in h) % 16
    check_char = format(checksum, "X")
    return f"{groups}#{check_char}"


BANNER_TEMPLATE = """
GARAGE ENTRY TICKET
Barcode:    {barcode}
"""


def main():
    secret = int.from_bytes(b"1n5an31y_H4rd_70_R34D_S3CR37")
    barcode = format_barcode(secret)
    correct_code = derive_ticket_code(secret)

    print(
        BANNER_TEMPLATE.format(
            barcode=barcode,
        )
    )

    for _ in range(5):
        print("What is your code?")
        guess = input()
        if guess.lower() == correct_code.lower():
            print("The gate is now open")
            print(f"Flag: sgctf{{{correct_code}}}")
            break


if __name__ == "__main__":
    main()

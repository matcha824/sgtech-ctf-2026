#!/bin/python

# python -m pip install pycryptodome

import random
from pathlib import Path
from Crypto.Util import number


SEED = random.Random(42)


def _seeded_randfunc(n):
	"""
	Generate deterministic random bytes for reproducible prime generation.
	"""
	return SEED.getrandbits(n * 8).to_bytes(n, "big")


def main():
	"""
	Generate a weak RSA challenge.

	The script:
	1. Reads the flag from solve/flag.txt.
	2. Converts the flag into an integer.
	3. Generates a deterministic 1024-bit prime number.
	4. Creates a weak RSA modulus where q = 2.
	5. Encrypts the encoded flag using RSA.
	6. Saves N, e, and c to chall-file.txt in the challenge root directory.
	"""
	base_dir = Path(__file__).resolve().parent.parent

	flag_file_path = base_dir / "solve" / "flag.txt"
	with open(flag_file_path, "r") as f:
		flag = f.read().strip()

	# Convert the flag text into an integer so it can be encrypted with RSA.
	encoded_flag = int(flag.encode().hex(), 16)

	# Generate one large prime factor deterministically for reproducibility.
	p = number.getPrime(1024, randfunc=_seeded_randfunc)

	# Intentionally use q = 2 to make the RSA modulus weak.
	q = 2
	N = p * q

	# Use the common public exponent.
	e = 65537

	# Encrypt the encoded flag using RSA.
	c = pow(encoded_flag, e, N)

	# Save the generated challenge values in the challenge root directory.
	output_file_path = base_dir / "chall-file.txt"
	with open(output_file_path, "w") as f:
		print(f"N = {N}", file=f)
		print(f"e = {e}", file=f)
		print(f"c = {c}", file=f)


if __name__ == "__main__":
	main()

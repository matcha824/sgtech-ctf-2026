#!/bin/python

# python -m pip install pycryptodome

import random
from pathlib import Path
from Crypto.Util import number


SEED = random.Random(2026)


def _seeded_randfunc(n):
	"""
	Generate deterministic random bytes for reproducible prime generation.
	"""
	return SEED.getrandbits(n * 8).to_bytes(n, "big")


def main():
	"""
	Generate an RSA broadcast attack challenge.

	The script:
	1. Reads the flag from solve/flag.txt.
	2. Converts the flag into an integer.
	3. Uses the small public exponent e = 3.
	4. Generates three different RSA moduli.
	5. Encrypts the same unpadded flag under each modulus.
	6. Saves the public exponent, moduli, and ciphertexts to chall-file.txt
	   in the challenge root directory.
	"""
	base_dir = Path(__file__).resolve().parent.parent

	flag_file_path = base_dir / "solve" / "flag.txt"
	with open(flag_file_path, "r") as f:
		flag = f.read().strip()

	# Convert the flag text into an integer so it can be encrypted with RSA.
	encoded_flag = int(flag.encode().hex(), 16)

	# Use a small public exponent for the RSA broadcast attack setup.
	e = 3

	moduli = []
	ciphertexts = []

	# Generate three RSA moduli and encrypt the same unpadded message
	# under each one.
	for _ in range(e):
		p = number.getPrime(256, randfunc=_seeded_randfunc)
		q = number.getPrime(256, randfunc=_seeded_randfunc)
		N = p * q

		c = pow(encoded_flag, e, N)

		moduli.append(N)
		ciphertexts.append(c)

	# Save the generated challenge values in the challenge root directory.
	output_file_path = base_dir / "chall-file.txt"
	with open(output_file_path, "w") as f:
		for i, (N, c) in enumerate(zip(moduli, ciphertexts), start=1):
			print(f"N_{i} = {N}", file=f)
			print(f"c_{i} = {c}", file=f)

		print(f"e = {e}", file=f)


if __name__ == "__main__":
	main()
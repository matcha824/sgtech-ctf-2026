#!/bin/python

from pathlib import Path


def main():
	"""
	Solve a weak RSA challenge where one factor of N is 2.

	The script:
	1. Reads N, e, and c from chall-file.txt.
	2. Recovers p by dividing the even modulus N by 2.
	3. Computes the totient using phi(2p) = p - 1.
	4. Computes the private exponent d.
	5. Decrypts the ciphertext.
	6. Converts the decrypted integer back into text.
	7. Prints the recovered flag.
	"""
	base_dir = Path(__file__).resolve().parent.parent

	chall_file_path = base_dir / "chall-file.txt"
	with open(chall_file_path, "r") as f:
		values = {}

		for line in f:
			name, value = line.strip().split(" = ")
			values[name] = int(value)

	N = values["N"]
	e = values["e"]
	c = values["c"]

	# Since N is even, one factor is 2 and the other factor is N // 2.
	p = N // 2

	# For this challenge, N = 2p, so phi(N) = lcm(1, p - 1) = p - 1.
	totient = p - 1

	# Compute the RSA private exponent.
	d = pow(e, -1, totient)

	# Decrypt the ciphertext.
	m = pow(c, d, N)

	# Convert the decrypted integer back into readable text.
	plaintext = bytes.fromhex(hex(m)[2:]).decode()
	print(plaintext)


if __name__ == "__main__":
	main()

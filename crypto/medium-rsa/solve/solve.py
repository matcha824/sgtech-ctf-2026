#!/bin/python

from pathlib import Path


def _extended_gcd(a, b):
	"""
	Compute the greatest common divisor of a and b and Bézout coefficients.

	Returns values gcd, x, and y such that:
	a * x + b * y = gcd
	"""
	if a == 0:
		return b, 0, 1

	gcd, x1, y1 = _extended_gcd(b % a, a)

	x = y1 - (b // a) * x1
	y = x1

	return gcd, x, y


def _chinese_remainder_theorem(moduli, remainders):
	"""
	Combine ciphertexts encrypted under different moduli using the
	Chinese Remainder Theorem.
	"""
	combined_modulus = 1
	for modulus in moduli:
		combined_modulus *= modulus

	result = 0

	for modulus, remainder in zip(moduli, remainders):
		partial_modulus = combined_modulus // modulus

		# Compute the modular inverse of the partial modulus.
		_, inverse, _ = _extended_gcd(partial_modulus, modulus)

		result += remainder * partial_modulus * inverse

	return result % combined_modulus


def _integer_cube_root(n):
	"""
	Compute the exact integer cube root of n using binary search.
	"""
	low = 0
	high = 1 << ((n.bit_length() + 2) // 3)

	while low <= high:
		mid = (low + high) // 2
		cube = mid ** 3

		if cube == n:
			return mid
		elif cube < n:
			low = mid + 1
		else:
			high = mid - 1

	raise ValueError("Combined ciphertext is not a perfect cube.")


def main():
	"""
	Solve an RSA broadcast attack challenge.

	The script:
	1. Reads the public exponent, moduli, and ciphertexts from chall-file.txt.
	2. Uses the Chinese Remainder Theorem to combine the ciphertexts.
	3. Recovers the encoded flag by computing the exact cube root.
	4. Converts the recovered integer back into readable text.
	5. Prints the recovered flag.
	"""
	base_dir = Path(__file__).resolve().parent.parent

	chall_file_path = base_dir / "chall-file.txt"
	with open(chall_file_path, "r") as f:
		values = {}

		for line in f:
			name, value = line.strip().split(" = ")
			values[name] = int(value)

	moduli = [values["N_1"], values["N_2"], values["N_3"]]
	ciphertexts = [values["c_1"], values["c_2"], values["c_3"]]

	# Combine the three ciphertexts to recover the original encoded
	# message raised to the third power.
	combined_ciphertext = _chinese_remainder_theorem(moduli, ciphertexts)

	# Since e = 3, compute the exact cube root to recover the encoded flag.
	encoded_flag = _integer_cube_root(combined_ciphertext)

	# Convert the recovered integer back into readable text.
	plaintext = bytes.fromhex(hex(encoded_flag)[2:]).decode()
	print(plaintext)


if __name__ == "__main__":
	main()
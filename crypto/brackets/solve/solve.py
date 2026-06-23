#!/bin/python

from pathlib import Path


def decode(ciphertext: str) -> list[str]:
	"""
	Decode a ciphertext string that was encoded using two unique symbols
	to represent binary digits.

	Since we do not know which symbol represents 0 and which represents 1,
	this function tries both possible mappings.

	For example, if the ciphertext contains only "<" and ">":
	- Mapping 1 tries "<" = 0 and ">" = 1
	- Mapping 2 tries ">" = 0 and "<" = 1

	Args:
		ciphertext: A string containing exactly two unique encoded symbols.

	Returns:
		A list containing the two possible decoded plaintext strings.
	"""
	chars = list(set(ciphertext))

	def apply_mapping(mapping: dict[str, int], ciphertext: str) -> str:
		"""
		Apply a specific symbol-to-bit mapping to decode the ciphertext.

		The ciphertext is first converted into a list of 0s and 1s. Then,
		every group of 8 bits is converted back into a character.

		Args:
			mapping: Dictionary mapping each ciphertext symbol to 0 or 1.
			ciphertext: The encoded string to decode.

		Returns:
			The decoded plaintext strings produced by this mapping.
		"""
		# Convert each encoded symbol into its corresponding binary digit.
		mapped_chars = [mapping[c] for c in ciphertext]

		result = ""

		# Process the binary digits in groups of 8 bits.
		for i in range(0, len(mapped_chars), 8):
			# Convert one 8-bit group into its integer ASCII value
			# then convert that integer into the corresponding character.
			result += chr(sum([mapped_chars[i + j] * 2 ** (7 - j) for j in range(8)]))

		return result

	# Try both possible assignments of the two symbols to binary 0 and 1.
	mapping1 = {chars[0]: 0, chars[1]: 1}
	mapping2 = {chars[1]: 0, chars[0]: 1}

	plaintext1 = apply_mapping(mapping1, ciphertext)
	plaintext2 = apply_mapping(mapping2, ciphertext)

	return [plaintext1, plaintext2]


def main():
	"""
	Read the challenge file, repeatedly decode possible plaintexts, and
	print the first result that appears to contain the flag prefix.
	"""
	# Locate the challenge file relative to this script:
	# brackets/src/script.py -> brackets/chall-file
	chall_file_path = Path(__file__).resolve().parent.parent / "chall-file"
	with open(chall_file_path, "r") as f:
		ciphertext = str(f.read().strip())

	possible_plaintexts = [ciphertext]
	for i in range(42):
		# Decode every current plaintext candidate and flatten the resulting lists.
		outputs = [x for p in possible_plaintexts for x in decode(p)]

		# Check whether any decoded output contains the expected flag prefix.
		for output in outputs:
			if "sgctf" in output:
				print(output)
				return

		# Use this round's outputs as the candidates for the next round.
		possible_plaintexts = outputs.copy()


if __name__ == "__main__":
	main()

#!/bin/python

from pathlib import Path


def encode(plaintext: str, mapping: list[str]) -> str:
	"""
	Encode a plaintext string by converting each character to 8-bit binary,
	then replacing each binary digit using the provided mapping.

	For each character:
	- Convert the character to its ASCII value
	- Convert that value to an 8-bit binary string
	- Map each '0' or '1' with an open or closed bracket

	Example:
		If mapping = ["<", ">"], then:
		"0" becomes "<"
		"1" becomes ">"

	Args:
		plaintext: The input string to encode.
		mapping: A two-element list where mapping[0] replaces binary 0
		         and mapping[1] replaces binary 1.

	Returns:
		The encoded ciphertext string.
	"""
	ciphertext = ""

	for ch in plaintext:
		# Convert the character to an 8-bit binary representation.
		binary = format(ord(ch), "08b")

		# Replace each binary digit with the corresponding mapping symbol.
		ciphertext += ''.join([mapping[int(digit)] for digit in binary])

	return ciphertext


def main():
	"""
	Read the flag, repeatedly encode it using different bracket mappings,
	then write the final ciphertext to the challenge output file.
	"""
	# Locate the flag file relative to this script:
	# brackets/src/script.py -> brackets/solve/flag.txt
	flag_file_path = Path(__file__).resolve().parent.parent / "solve" / "flag.txt"
	with open(flag_file_path, "r") as f:
		ciphertext = str(f.read().strip())

	brackets = [
		["<", ">"],
		["[", "]"],
		["{", "}"],
	]

	# Apply each encoding layer in sequence.
	for bracket_set in brackets:
		ciphertext = encode(ciphertext, bracket_set)

	# Write the final encoded challenge file.
	chall_file_path = Path(__file__).resolve().parent.parent / "chall-file"
	with open(chall_file_path, "w") as f:
		f.write(ciphertext + "\n")


if __name__ == "__main__":
	main()

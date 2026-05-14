#!/bin/python

from pathlib import Path
from PIL import Image
import re


def main():
	"""
	Extract and print the hidden flag from chall-file.png.

	The script:
	1. Opens the challenge image.
	2. Reads the blue channel of every pixel.
	3. Treats each blue-channel value as one embedded bit.
	4. Converts every group of 8 bits back into a character.
	5. Searches the decoded text for a flag matching sgctf{...}.
	"""
	base_dir = Path(__file__).resolve().parent.parent
	img_file_path = base_dir / "chall-file.png"

	# Open the image as RGB so each pixel is always a 3-value tuple: (R, G, B).
	img = Image.open(img_file_path).convert("RGB")
	pixels = img.load()
	width, height = img.size

	# Extract one hidden bit from the blue channel of each pixel.
	bits = []
	for y in range(height):
		for x in range(width):
			_, _, blue = pixels[x, y]
			bits.append(blue)

	# Ignore any leftover bits that do not form a complete byte.
	bits = bits[:len(bits) // 8 * 8]

	# Convert every group of 8 bits into one character.
	embedded_str = "".join(
		chr(int("".join(str(bit) for bit in bits[i:i + 8]), 2))
		for i in range(0, len(bits), 8)
	)

	# Search for the flag in the decoded text.
	print(re.search(r"sgctf\{[^}]*\}", embedded_str).group())


if __name__ == "__main__":
	main()

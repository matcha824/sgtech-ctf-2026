#!/bin/python

from pathlib import Path
from PIL import Image
import math


YELLOW = (255, 255, 0)


def main():
	"""
	Generate a challenge image containing a hidden flag.

	The script:
	1. Reads the flag from solve/flag.txt.
	2. Reads filler text from filler.txt.
	3. Inserts the flag into the middle of the filler text lines.
	4. Converts the resulting text into 8-bit binary.
	5. Stores each bit in the blue channel of one pixel.
	6. Saves the image as chall-file.png in the challenge root directory.
	"""
	base_dir = Path(__file__).resolve().parent.parent

	flag_file_path = base_dir / "solve" / "flag.txt"
	with open(flag_file_path, "r") as f:
		flag = f.read().strip()

	filler_file_path = Path(__file__).resolve().parent / "filler.txt"
	with open(filler_file_path, "r") as f:
		filler = f.read().strip()

	# Insert the flag as its own line in the middle of the filler text.
	lines = filler.split("\n")
	midpoint = len(lines) // 2
	lines = lines[:midpoint] + [flag] + lines[midpoint:]

	# Convert the full hidden message into a flat list of binary digits.
	# Each character becomes exactly 8 bits.
	hidden_text = "".join(lines)
	bits = [int(bit) for ch in hidden_text for bit in f"{ord(ch):08b}"]

	# Use the smallest square image large enough to hold all bits.
	size = math.ceil(math.sqrt(len(bits)))

	# Create a yellow image. Yellow is (255, 255, 0), so the blue channel
	# can be changed to 0 or 1 without visibly altering the image much.
	img = Image.new("RGB", (size, size), YELLOW)
	pixels = img.load()

	# Store one bit per pixel in the blue channel.
	for y in range(size):
		for x in range(size):
			i = size * y + x

			if i < len(bits):
				pixels[x, y] = (255, 255, bits[i])

	# Save the generated challenge image in the challenge root directory.
	output_path = base_dir / "chall-file.png"
	img.save(output_path)


if __name__ == "__main__":
	main()

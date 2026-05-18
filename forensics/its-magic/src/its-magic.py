#!/bin/python

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def main():
	"""
	Generate a challenge file that looks like a PDF but is actually a PNG image.

	The script:
	1. Reads the flag from solve/flag.txt.
	2. Creates a blank white image.
	3. Writes the flag in large black text at the center of the image.
	4. Saves the image as chall-file.png in the challenge root directory.
	5. Renames the file to chall-file.pdf without changing the file contents.
	"""
	base_dir = Path(__file__).resolve().parent.parent

	flag_file_path = base_dir / "solve" / "flag.txt"
	with open(flag_file_path, "r") as f:
		flag = f.read().strip()

	width, height = 1280, 720

	# Create a blank white image.
	img = Image.new("RGB", (width, height), "white")
	draw = ImageDraw.Draw(img)
	font = ImageFont.load_default(size=75)

	# Measure the rendered flag text so it can be centered.
	bbox = draw.textbbox((0, 0), flag, font=font)
	text_width = bbox[2] - bbox[0]
	text_height = bbox[3] - bbox[1]

	# Center the text horizontally and vertically.
	# Subtracting bbox[1] corrects for the font's vertical offset.
	x = (width - text_width) // 2
	y = (height - text_height) // 2 - bbox[1]

	# Draw the flag onto the image.
	draw.text((x, y), flag, fill="black", font=font)

	# Save the generated challenge image in the challenge root directory.
	output_png_path = base_dir / "chall-file.png"
	img.save(output_png_path, format="PNG")

	# Rename the PNG file to .pdf.
	# The file extension changes, but the file contents are still PNG data.
	output_fake_pdf_path = base_dir / "chall-file.pdf"
	output_png_path.rename(output_fake_pdf_path)


if __name__ == "__main__":
	main()

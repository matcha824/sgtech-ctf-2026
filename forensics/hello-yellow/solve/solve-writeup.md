# Solve Writeup

## Overview

The challenge provides a PNG image that appears to be a plain yellow square. Since there is no visible text or obvious visual clue, the important idea is to look at the image data itself rather than the appearance of the image.

The flag is hidden using a simple form of image steganography. Instead of changing the visible image in an obvious way, the challenge stores data in very small changes to the pixel color values.

## Initial Analysis

Opening the image normally does not reveal much because the image looks like a solid yellow block. However, each pixel in an image is made up of color channels, usually red, green, and blue.

A yellow pixel is typically represented as:

```text
(255, 255, 0)
```

When examining the pixel values more closely, the red and green channels remain constant, but the blue channel changes slightly between `0` and `1`.

This is the key observation: the blue channel is being used to hide binary data.

## Hidden Data Format

Each pixel stores one bit of information in its blue channel:

```text
blue channel value 0 -> binary 0
blue channel value 1 -> binary 1
```

Because the blue value only changes between `0` and `1`, the image still looks yellow to the human eye. The visual difference between `(255, 255, 0)` and `(255, 255, 1)` is essentially unnoticeable.

However, programmatically, those values are different and can be extracted.

## Solving Approach

To solve the challenge, read the pixels of the image in normal order: left to right, top to bottom.

For each pixel, extract the blue channel. This produces a long sequence of binary digits.

Once the bits are extracted, group them into chunks of 8. Each group of 8 bits represents one ASCII character.

For example:

```text
01000001
```

represents the decimal value `65`, which corresponds to the character:

```text
A
```

Repeating this process for every group of 8 bits reconstructs the hidden text.

## Locating the Flag

The decoded text contains filler content, so the entire decoded message is not the flag by itself.

After reconstructing the hidden text, search through it for the expected flag format:

```text
sgctf{...}
```

Once that pattern is found, the matching string is the flag.

# Solve Writeup

## Overview

The challenge provides a file named `chall-file.pdf`. At first glance, this suggests that the file should be opened and analyzed as a normal PDF document.

However, the important idea in this challenge is that file extensions can be misleading. A file extension does not determine what type of data is actually inside the file. The real file type is determined by the file contents, especially the file header or magic bytes.

In this challenge, the file is named like a PDF, but the underlying file data is actually a PNG image.

## Initial Analysis

Trying to open the file as a normal PDF may fail, show an error, or appear corrupted. This is a clue that the file may not actually be a valid PDF.

A good first step is to inspect the file type using a tool such as:

~~~bash
file chall-file.pdf
~~~

Even though the filename ends in `.pdf`, the `file` command identifies the actual file format based on its contents.

The result should indicate that the file is really a PNG image.

## File Extension vs File Contents

A PDF file normally begins with a PDF header such as:

~~~text
%PDF
~~~

A PNG file begins with PNG magic bytes instead. These bytes identify the file as PNG data, regardless of what the file is named.

This means a file called:

~~~text
chall-file.pdf
~~~

can still internally be a PNG image if its contents were created as PNG data.

The extension is only a label. It does not automatically convert the file into that format.

## Solving Approach

To solve the challenge, first determine the real file type.

Run:

~~~bash
file chall-file.pdf
~~~

Once the file is identified as a PNG image, rename it back to the correct extension:

~~~bash
mv chall-file.pdf chall-file.png
~~~

After renaming the file, open it as an image using an image viewer.

## Key Takeaway

The main lesson of this challenge is that file extensions cannot always be trusted. When a file does not behave as expected, inspect the actual file contents.

Tools like `file`, hex editors, or magic-byte inspection can reveal the real format of a file, even when the extension is intentionally misleading.

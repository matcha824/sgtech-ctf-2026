# No Remorse - Solution Writeup

## Overview
This challenge uses a single PDF memorandum as the handout. The document looks like ordinary dramatic prose, but the real message is carried by the way parts of the text are obscured.

## Solving the PDF
The key observation is that the redactions are not random. Their lengths alternate in a way that matches Morse code, with short blocks acting as dots and long blocks acting as dashes.

Once that pattern is recognized, the solve becomes a transcription exercise:
1. Read the PDF carefully and separate each line into short and long marks.
2. Convert those marks into Morse code.
3. Decode the Morse into letters.

Working through the memorandum in order yields:

```text
-         - t
. . . .   - h
. .       - i
. . .     - s
. .       - i
. . .     - s

-         - t
- - -     - o
-         - t
. -       - a
. - . .   - l
. - . .   - l
- . - -   - y
. . - .   - f
- - -     - o

. - .     - r
. . .     - s
. . -     - u
. - .     - r
.         - e
- .       - n
- - -     - o
-         - t
- . - -   - y
- - -     - o
. . -     - u
. - .     - r
. . - .   - f
. - . .   - l
. -       - a
- - .     - g
```

This produces the flag `thisistotallyforsurenotyourflag`.

## Result
Submit the decoded lowercase text as `sgctf{thisistotallyforsurenotyourflag}`.

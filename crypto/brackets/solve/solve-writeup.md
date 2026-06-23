# Challenge Writeup

## Overview

The challenge provides a file named `chall-file` that contains an encoded flag. The encoding is based on repeatedly converting text into binary and then replacing the binary digits with pairs of bracket characters.

The solve script reverses this process by repeatedly trying both possible binary mappings for each encoded layer until it finds output containing the expected flag prefix, `sgctf`.

## Encoding Process

The original flag is read from:

```text
solve/flag.txt
```

The encoder applies three bracket-based encodings in sequence:

```python
brackets = [
    ["<", ">"],
    ["[", "]"],
    ["{", "}"],
]
```

For each layer, every character is converted into its 8-bit binary representation:

```python
format(ord(ch), "08b")
```

Each binary digit is then replaced using the current mapping.

For example, with this mapping:

```python
["<", ">"]
```

binary `0` becomes `<`, and binary `1` becomes `>`.

So a character like `A` becomes:

```text
01000001
```

and then becomes:

```text
<><<<<<>
```

After the first layer, the output is encoded again using square brackets, and then once more using curly braces. This creates multiple layers of bracket-based binary encoding.

## Important Observation

Each encoded layer uses exactly two unique characters.

However, when solving, we may not know which character represents `0` and which represents `1`.

For example, if a layer only contains `{` and `}`, there are two possible mappings:

```python
{"{": 0, "}": 1}
```

or:

```python
{"}": 0, "{": 1}
```

Only one of these mappings is correct for that layer.

Because every layer has two possible mappings, decoding creates a branching search tree.

## Decoding Function

The solve script's `decode` function takes one ciphertext string and finds the two unique characters inside it:

```python
chars = list(set(ciphertext))
```

Then it tries both possible assignments:

```python
mapping1 = {chars[0]: 0, chars[1]: 1}
mapping2 = {chars[1]: 0, chars[0]: 1}
```

For each mapping, it converts the ciphertext into a list of bits, groups those bits into chunks of 8, and converts each chunk back into a character.

The key conversion is:

```python
chr(sum([mapped_chars[i+j] * 2**(7-j) for j in range(8)]))
```

This reconstructs each byte from its eight bits.

The function returns both possible plaintexts:

```python
return [plaintext1, plaintext2]
```

## Search Strategy

The script starts with the original challenge text:

```python
possible_plaintexts = [ciphertext]
```

Then it repeatedly decodes every current candidate:

```python
outputs = [x for p in possible_plaintexts for x in decode(p)]
```

This line does two things:

1. Calls `decode(p)` on every possible plaintext candidate.
2. Flattens the resulting lists into one combined list of outputs.

After each round, the number of candidates doubles because each candidate produces two possible decodings.

The script then checks every output for the expected flag prefix:

```python
if "sgctf" in output:
    print(output)
    return
```

Once a decoded string contains `sgctf`, the script prints it and stops.

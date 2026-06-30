# Solve Writeup — Garage Crawl

## Overview
The challenge provides a Python 3.13 `.pyc` file. The player must decompile, decode, and reverse-engineer the obfuscated logic to recover a parking ticket code.

## Steps

### 1. Decompile the bytecode
Standard tools (uncompyle6, decompyle3) don't support Python 3.13. Use [PyLingual.io](https://pylingual.io) to decompile `dist.pyc`.

The decompiled output will look something like:
```python
import base64
exec(base64.b64decode('...').decode())
```

### 2. Base64 decode
Decode the base64 string to reveal the obfuscated source code. The result is valid Python with:
- All variable/function/class names replaced with random strings (e.g., `_qizemjhu`, `_tvdrwslp`)
- All literals (integers, strings, bytes) stored in a dictionary lookup table
- Imports replaced with `__import__()` calls

### 3. Reverse-engineer the logic
Map the obfuscated names back to their values using the constants dictionary. The code implements:

- **SecureRand** — A linear congruential generator (LCG) with:
  - A = 1103515245
  - C = 12345
  - M = 2^31
- **derive_ticket_code(seed)** — Seeds the LCG, generates 16 bytes, MD5-hashes them, returns first 16 hex chars
- **Secret seed** — `int.from_bytes(b"1n5an31y_H4rd_70_R34D_S3CR37")`

### 4. Compute the flag
Reimplement `derive_ticket_code` with the secret seed:

```python
import hashlib

class SecureRand:
    _A = 1103515245
    _C = 12345
    _M = 1 << 31

    def __init__(self, seed):
        self.state = seed & 0xFFFFFFFF

    def next_int(self):
        self.state = (self._A * self.state + self._C) % self._M
        return (self.state >> 16) & 0x7FFF

    def next_bytes(self, n):
        return bytes(self.next_int() & 0xFF for _ in range(n))

secret = int.from_bytes(b"1n5an31y_H4rd_70_R34D_S3CR37")
rng = SecureRand(secret)
token = rng.next_bytes(16)
digest = hashlib.md5(token).hexdigest()[:16]
print(f"sgctf{{{digest}}}")
```

Output: `sgctf{41bea38ad7b71747}`

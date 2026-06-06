# GOT

**Category:** Binary Exploitation
**Difficulty:** Intermediate

## Description

Welcome to GOT. We've set up a secure number storage service with authentication. Only authorized personnel can write to the database.

Can you help break in and read the flag?

```
nc <host> <port>
```

## Files Provided

- `challenge` — the compiled binary
- `challenge.c` — source code
- `libc.so.6` — the libc used on the server
- `exploit_template.py` — a guided exploit template with TODOs
- `Dockerfile.solver` — optional Docker environment for developing your exploit

## Getting Started

### Option 1: Docker (Recommended)

Build the solver environment which has pwntools pre-installed:

```bash
docker build -f Dockerfile.solver -t got-solve .
docker run -it --network host got-solve
```

### Option 2: Local

Install pwntools:

```bash
pip install pwntools
```

Then run your exploit:

```bash
python3 exploit_template.py
```

## Tips

- Use `checksec ./challenge` to see what protections are enabled
- Use pwntools' `ELF()` to inspect symbols and GOT entries
- See `EXPLOIT_GUIDE.md` for hints if you get stuck
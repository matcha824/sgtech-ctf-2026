# Stack Overflow

**Category:** Binary Exploitation (pwn)  
**Difficulty:** Beginner+  
**Flag format:** `SGTECHCTF{...}`

## Description

The developers of the "Stack Overflow" app claim they've added stack protection to prevent buffer overflows. There's a hidden function in the binary that prints the flag... but even if you know where it is, can you get past their defenses?

## Connection

```
nc <host> <port>
```

## Files

- `vuln` — The vulnerable x86-64 ELF binary
- `exploit.py` — Skeleton exploit script (fill in the blanks)
- `Dockerfile.solver` — Solver environment with all tools (for Apple Silicon / non-x86 users)

## Getting Started

### Option A: Native x86-64 Linux

```bash
chmod +x vuln
./vuln                          # run locally
objdump -d vuln | less          # disassemble
python3 exploit.py              # run your exploit
```

### Option B: Any architecture (Docker)

```bash
docker build -f Dockerfile.solver -t ctf-solver .
docker run -it --cap-add=SYS_PTRACE --security-opt seccomp=unconfined ctf-solver
```

Inside the container you have: `gdb-multiarch`, `python3 + pwntools`, `objdump`, `checksec`, `qemu-x86_64`.

### Debugging (Apple Silicon)

```bash
# Inside the container:
qemu-x86_64 -g 1234 ./vuln &
gdb-multiarch ./vuln -ex "target remote :1234" -ex "break greet" -ex "continue"
```

## Useful Commands

```bash
# Check binary protections
checksec --file=./vuln

# Find all function addresses
objdump -d vuln | grep -E "<\w+>:"

# Disassemble a specific function
objdump -d vuln | sed -n '/<greet>/,/^$/p'

# Generate a cyclic pattern (for offset finding)
python3 -c "from pwn import *; print(cyclic(100))"
```

## Hints

<details>
<summary>Hint 1 (mild)</summary>

The binary uses `gets()` to read input. What happens if you give it more than the buffer can hold?

</details>

<details>
<summary>Hint 2 (moderate)</summary>

There's a function in the binary that's never called during normal execution. There's also something between your buffer and the return address that you need to deal with carefully.

</details>

<details>
<summary>Hint 3 (strong)</summary>

The program checks a "guard" variable after reading your input. If you've corrupted it, the program exits before returning. You need to write the correct value back into the guard's position while also overwriting the return address.

</details>

<details>
<summary>Hint 4 (very strong)</summary>

Use `objdump -d vuln | grep movabs` to find the guard value. Use `objdump -d vuln | grep "<win>"` to find the target function address. Remember: x86-64 is little-endian.

</details>
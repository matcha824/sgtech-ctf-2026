# Stack Overflow

**Category:** Binary Exploitation (pwn)  
**Difficulty:** Medium+  
**Flag format:** `SGTECHCTF{...}`

## Key Concepts
- Buffer Overflows: A **buffer overflow** occurs when a program attempts to write more data into a fixed-length block of memory - called a **buffer** - than it can hold. This can overwrite adjacent memory, including the return address on the stack, allowing an attacker to redirect program execution.

__Note:__ This is different from a **stack overflow**, which is a condition where the stack pointer exceeds the allocated stack space, causing a crash. Stack overflows typically occur when too many function calls are made, exhausting the stack space.

- Stack Canaries: A **stack canary** is a random value placed on the stack between the buffer and the return address. If the canary is modified, the program will crash before the return address can be overwritten. __Note:__ In this challenge, we give you the canary value, but you have to determine where to place it on the stack.
- Return Address Overwrite: The **return address** is the address of the next instruction to execute after a function returns. If the return address is overwritten, the program will jump to the new address instead of the original one.
- Function Calls: **Function calls** are used to execute code in a separate function. The return address is pushed onto the stack when a function is called, and popped off the stack when the function returns.

## Background Information

### Stack Layout
When a function is called on x86-64 architecture, the stack grows downward (toward lower memory addresses). Every time a function is called, it carves out its own private workspace on the stack called a **stack frame**. The layout for a typical function looks like this:

[Higher addresses]
  Return address            (8 bytes) - where execution resumes after the function
  Saved RBP                 (8 bytes) - previous stack frame pointer
  Local variables           (variable size) - buffers, integers, etc.
[Lower addresses]

When you overflow a buffer (which sits at a lower address), you write upward through the local variables, past the 
saved RBP, and into the return address.

#### Core Components of the Stack Explained
- `rsp` (Stack Pointer): Points to the absolute top of the stack (which, because the stack grows downward, is the lowest memory adress currently being used). It moves every time you push or pop data from the stack.
- `rbp` (Base Pointer): Points to the base of the current stack frame. Unlike `rsp`, `rbp` stays completely still while the function runs. It acts as a fixed anchor so the program can easily find local variables
- Return address: This is the memory address of the exact instruction the CPU needs to execute __after__ the current function finishes and returns to the caller.

Here's how it all works together:
Imagine Function A is running, and it calls Function B.

1. The moment Function A calls Function B, the CPU automatically pushes Function A's return address onto the stack. `rsp` moves down to accommodate it.
2. Function B then starts executing. The very first thing it does is save Function A's `rbp` value (the old base pointer) onto the stack so that it can restore it later. Function A will need this to calculate offsets for its own local variables.
3. Now that the old `rbp` is safe, Function B sets its own base pointer anchor by copying the current stack pointer: `mov rbp, rsp`. Now, both `rbp` and `rsp` point to the same location, which is the top of Function B's stack frame.
4. Function B needs room for its local variables. It creates this space by subtracting from `rsp`: `sub rsp, <size>`. This moves the stack pointer down, allocating space for local variables.
5. When Function B finishes, it has to clean up and give control back to Function A. This involves moving the stack pointer back to the base pointer and instantly discarding all local variables. It also pops Function A's old base pointer back into `rbp`. Now Function A's anchor is restored
6. Lastly, Function B executes the `ret` instruction, which pops the return address off the stack and jumps the CPU's instruction pointer straight back to Function A's code.

### Stack Alignment: The 16-Byte Rule
Modern 64-bit CPUs (x86-64) enforce a rule: The stack pointer (`rsp`) must be aligned to a 16-byte boundary before any `call` instruction is executed. In other words `rsp` % 16 == 0 at the moment a `call` instruction is called. The reason for this is because modern CPUs use special instructions (like AVX or SSE for vector math) that expect data to be neatly lined up in memory blocks divisible by 16. If the data isn't aligned, the CPU has to do extra work, or worse, the program will instantly crash.

## Little-Endian Byte Order
x86-64 is little endian architecture, meaning mutli-byte values are stored with the __least significant byte first__. So for example, when writing an address like `0x00401216` into your payload, it must be encoded as `x\16\x12\x40\x00\x00\x00\x00\x00`. Python's `pwntools` library provides `p64()` which handles this conversion automatically.

## Getting Started
For this challenge, you'll need to have Docker installed on your machine (i.e. have the Docker Desktop application up and running). The reason for this is because Mac and Windows can't run Linux containers natively.

When you begin the challenge, make sure that you have the challenge files downloaded from CTFd. This includes `vuln.c`, `Makefile`, `exploit.py`, and `Dockerfile.solver`. Here's what each file does:

- `vuln.c` — The source code of the vulnerable program. You can look through it to see the function names, how each function works, etc.
- `Makefile` — Used to compile the program
- `exploit.py` — Skeleton exploit script (fill in the blanks)
- `Dockerfile.solver` — Solver environment with all tools (for Apple Silicon / non-x86 users)

Next, build the solver container
`docker build -f Dockerfile.solver -t ctf-solver .`

This compiles `vuln.c` inside an x86-64 Linux container, producing the same binary the server is running.

After that, enter the container by running 
`docker run -it --cap-add=SYS_PTRACE --security-opt seccomp=unconfined ctf-solver`

This starts a new container from the image `ctf-solver` and gives it extra permissions useful for debugging, reverse engineering, and CTF work. The `SYS_PTRACE` capability allows the container to debug other processes, and `seccomp=unconfined` disables security restrictions that might interfere with debugging.

Now, you're in `/ctf` with the compiled `vuln` binary and your exploit skeleton. Inside the container, you have: `gdb-multiarch`, `python3 + pwntools`, `objdump`, `checksec`, `qemu-x86_64`.

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

## Submitting
Once you're done crafting your exploit, run the exploit in your container by doing `python3 exploit.py`. If you're 
successful, you should see the flag printed to the console. Submit it to CTFd challenge website to earn your points.
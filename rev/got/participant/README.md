# GOT

**Category:** Binary Exploitation
**Difficulty:** Medium/Hard

## Description
Welcome to GOT. We've set up a secure number storage service with authentication. Only authorized personnel can write to the database.

Your goal is to break in and read the flag

## Background Information and Context
This challenge involves several core concepts in systems security and low-level programming. Understanding these will help you develop your exploit.

### Memory Layout of a C Program
When a C program is compiled and loaded into memory, it is organized into different sections, each with a specific purpose:

- **Text (.text) Section**: Contains the executable instructions of the program. This section is read-only.
- **Data (.data) Section**: Contains global and static variables that are __initialized__ at compile time.
- **BSS (.bss) Section**: Contains global and static variables that are __uninitialized__ or __initialized to zero__. BSS stands for "Block Started by Symbol".
    - For example, global arrays and variables declared at file sceop (like `long numbers[16]`) live in BSS. Their addresses are fixed relative to each other in the binary.
- **Heap**: Used for dynamic memory allocation during runtime.
- **Stack**: Used for function calls, local variables, and return addresses.

Understanding the memory layout is crucial for exploiting vulnerabilities, as it helps identify where to inject code or manipulate data.

### Global Offset Table (GOT) and Procedure Linkage Table (PLT)
The Global Offset Table (GOT) and Procedure Linkage Table (PLT) are mechanisms used in dynamically linked binaries to resolve function addresses at runtime. In other words, these are vital components of modern operating systems (like Linux) that allow programs to call functions in shared libraries (like `libc`) without knowing their exact addresses at compile time.

To understand why the GOT exists, you have to understand a fundamental problem in modern computing: **Position Independent Code (PIC)**. When you write a program that uses a standard function like `printf()`, that function doesn't actually live inside your compiled binary; it lives inside a shared system library. When your program is loaded into RAM, the OS might throw that shared library into any random, unpredictable memory address. Because the compiler cannot possibly know at compile time what the memory address will be, it cannot hardcode a direct jump instruction. The GOT is the clever workaround for this problem.

When a program calls a function from a shared library (like `libc`), the call goes through the PLT, which then jumps to the GOT entry. The GOT entry is initially filled with a pointer to the PLT stub, which then resolves the actual address of the function in libc and updates the GOT entry. This allows the program to call functions in shared libraries without knowing their exact addresses at compile time.

Understanding the GOT and PLT is crucial for exploiting vulnerabilities, as it allows you to redirect execution to arbitrary functions in libc.

### RELRO (RElocation Read-Only)
RELRO stands for RElocation Read-Only. It is a security feature that prevents the GOT from being writable at runtime. This is done by marking the GOT as read-only, which prevents attackers from overwriting the GOT entries and redirecting execution to arbitrary functions in libc. In other words, it's used to protect binaries against GOT overwrite attacks.

We know that the GOT is basically a directory of function pointers sitting in memory. Because the dynamic linker needs to write the real memory addresses into the GOT while the program runs, that table __must__ be writable. However, hackers realized this was a massive vulnerability. If an attack could trigger a buffer overflow, they could intentionally spill data into the GOT, overwrite the address of a standard function like `printf`, and change it to point to malicious code.

This challenge uses **partial RELRO**, which means that the GOT remains writable at runtime.

### ASLR (Address Space Layout Randomization)
ASLR is a security feature that randomizes the memory layout of a process at runtime. This makes it difficult for attackers to predict the addresses of functions in `libc`, as they are no longer at fixed locations in memory. In other words, it's used to protect binaries against memory corruption attacks.


## Files Provided
- `challenge` — the compiled binary
- `challenge.c` — source code
- `libc.so.6` — the libc used on the server. This is the C standard library - the shared library that provides functions like `printf`, `malloc`, and `free`.
- `exploit_template.py` — a guided exploit template with TODOs
- `Dockerfile.solver` — optional Docker environment for developing your exploit

## Challenge Structure

The challenge is a menu-driven C program with 3 options: **read**, **authenticate**, and **write**. The exploit has 3 stages that build on each other - you can't skip ahead beacuse each stage unlocks the capability needed for the next.

### Stage 1: Bypass Authentication
The goal here is to unlock the write functionality. Menu option 3 (write) is gated behind an `authenticated` flag. To set it, you need to submit a 64-bit random token generated at startup. You don't know the token. For this tage, `elf.symbols` might be useful.

### Stage 2: Defeat ASLR
The goal here is to find the runtime address of `system` in libc. The issue is that ASLR randomizes where `libc` is located, so you can't hardcode `system()`'s address. You need a leak.

### Stage 3: Hijack Control Flow
The goal here is to get a shell and read the flag. You now know where `system()` is, but the program never calls it. Since you now have write access (from Stage 1) and you know `system()`'s address, you can overwrite a function pointer in the GOT to redirect a function call.

## Getting Started
1. Make sure that you have Docker Desktop installed and running. Build the solver environment which has `pwntools` pre-installed:

```bash
docker build --platform linux/amd64 -f Dockerfile.solver -t got-solve .
```

This command cmopiles a static, reusable Docker image named `got-solve` based on instructions in `Dockerfile.solver`. It forces Dockcer to build the image specifically for standard 64-bit Intel/AMD processors. This is important because if you're working on an Apple Silicon Mac because Mac chips use ARM architecture. Compiling binary exploits or low-level assembly would break without forcing this x86_64 architecture.

2. Run the following command to start the container from the existing image

```bash
docker run --platform linux/amd64 -it got-solve
```

3. You should now be inside the container. You can verify this by checking the prompt, which should look something like `root@abc123:/solve#`.

4. When you think you're done crafting the exploit, you can submit it by running:

```bash
python3 exploit_template.py
```

## Tips

- Use `checksec ./challenge` to see what protections are enabled
- Use pwntools' `ELF()` to inspect symbols and GOT entries
- See `EXPLOIT_GUIDE.md` for hints if you get stuck
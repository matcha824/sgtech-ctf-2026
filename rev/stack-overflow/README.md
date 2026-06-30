# Buffer Overflow

This is a classic buffer overflow challenge where you need to exploit a vulnerable binary. Your goal is to overflow the stack buffer to redirect execution to the hidden `win()` function and retrieve the flag

**Challenge Type:** pwn

**Downloads:** `vuln` (binary)

# Background Information

## Introduction to the Stack
The **execution stack** (or **call stack**) is a runtime data structure used by a program to keep track of active function calls. Each time a function is called, a new stack frame is pushed onto the stack containing information like the function parameters, local variables, and return address. When the function finishes, its frame is popped off, and control returns to the caller. 

## Introduction to Buffer Overflows
Because the call stack stores critical information like return addresses and local variables, it becomes a high-value target when memory safety isn't enforced. A **buffer overflow** occurs when a program writes more data into a fixed-size memory buffer than it can hold, causing the extra data to spill into adjacent memory regions. If that buffer is located on the stack, the overflow can overwrite important control data in the stack frame, including the return address. This can lead to unpredictable program behavior, crashes, or in more serious cases, allow an attacker to redirect execution flow and run arbitrary code.

# Challenge Introduction
You will be provided with a vulnerable binary `vuln`. This challenge is instantiated on a Docker container running on the challenge/CTF server and this binary is being served to you by it. You are also given a `Makefile` to help you compile and build progr

# Goal
Your goal is to fill out the `exploit.py` script that will run against the challenge server host and, if successful, retrieve the value of the flag. The script is given as a skeleton and you need to fill out the required portions.

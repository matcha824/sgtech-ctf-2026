# Solution Steps

1. Download the challenge binary `vuln` from the challenge files
2. Analyze the binary using tools like `checksec`, `objdump`, or Ghidra
3. Identify the buffer overflow vulnerability in the `greet()` function
4. Calculate the offset to the return address (72 bytes: 64-byte buffer + 8-byte saved RBP)
5. Find the address of the `win()` function using `objdump -d vuln` or `nm vuln`
6. Construct the payload: 72 bytes of padding + address of win()
7. Run the exploit: `python3 solve/solve.py` (for local testing)
8. For remote exploitation: `python3 solve/solve.py remote`

## Vulnerability Details

The binary uses the unsafe `gets()` function which doesn't check buffer boundaries, allowing a classic stack-based buffer overflow. The binary is compiled with:
- No stack canary (`-fno-stack-protector`)
- No PIE (`-no-pie`)
- Executable stack (`-z execstack`)

This makes it straightforward to overwrite the return address and redirect execution to the `win()` function.
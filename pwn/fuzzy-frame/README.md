# Fuzzy Frame (CTF Challenge)

The program reads `badfile` (up to 517 bytes),
copies into a stack buffer of unknown size, and participants use GDB to find the offset, then
overwrite the return address with a NOP sled and shellcode.

- **Category**: Binary Exploitation
- **Difficulty**: Medium-Hard
- **Flag**: `sgctf-was-here`
- **Access**: `ssh ctf@<host> -p <port>` (password: `ctf`)
- **Ports**: 1 (SSH/22)
- **Container requirement**: run with `--privileged`

## Repo layout

```
fuzzy-frame/
├── Dockerfile
├── challenge/
│   ├── vuln.c
│   ├── vuln_redacted.c
│   ├── exploit_template.py
│   └── Makefile
├── setup/
│   ├── entrypoint.sh
│   ├── flag.txt
│   └── sshd_config
└── solution/
    ├── writeup.md
    └── exploit_solution.py
```

## Build & run

### Build

```bash
docker build . -t "fuzzy-frame"
```

### Connect

```bash
ssh ctf@<host> -p <port>
# password: ctf
```

### Stop / cleanup

```bash
docker stop fuzzy-frame && docker rm fuzzy-frame
```

## What participants see inside container

In `/home/ctf/`:

- `vuln`: Vulnerable binary
- `source.c`: Redacted source (`BUF_SIZE ???`)
- `exploit.py`: Exploit template (writes `badfile`)
- Run: `python3 exploit.py && ./vuln` (expects `badfile` in cwd)

Flag lives at `/root/flag.txt`.


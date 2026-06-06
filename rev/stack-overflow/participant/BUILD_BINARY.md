# How to get the compiled `vuln` binary

Since the binary must be compiled on x86-64 Linux, use one of these methods:

## Option A: Extract from the Docker host (where your challenge is already built)

```bash
# On the Docker host:
docker create --name tmp-extract <your-image-tag>
docker cp tmp-extract:/ctf/vuln ./vuln
docker rm tmp-extract

# Copy it back to your local machine:
# (from your Mac)
scp <username>@<docker-host>:~/vuln ./participant/vuln
```

## Option B: Build locally (requires working Docker)

```bash
cd pwn/stack-overflow
docker build -f src/Dockerfile -t tmp-build .
docker create --name tmp tmp-build
docker cp tmp:/ctf/vuln ./participant/vuln
docker rm tmp
```

## After you have the binary

Place `vuln` in this `participant/` folder. It will be uploaded to CTFd as a challenge file alongside `exploit.py`, `Dockerfile.solver`, and `README.md`.
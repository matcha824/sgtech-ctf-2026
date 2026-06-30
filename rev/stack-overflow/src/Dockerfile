FROM --platform=linux/amd64 ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install only what's needed to build and serve the binary
RUN apt-get update && apt-get install -y \
    gcc \
    socat \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /ctf

# Copy challenge source and build
COPY vuln.c .
COPY Makefile .
RUN make

# Create the flag
RUN echo "SGTECHCTF{c4n4ry_byp4ss_pr0}" > flag.txt

# Expose port 
EXPOSE 1337

# Serve the binary over TCP
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:./vuln,pty,raw,stderr"]

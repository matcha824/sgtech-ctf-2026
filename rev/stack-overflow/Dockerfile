FROM --platform=linux/amd64 ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    socat \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /ctf/challenge

# Copy challenge source
COPY src/vuln.c .
COPY src/Makefile .

# Build the vulnerable binary
RUN make

# Create the flag (this will be replaced with the actual flag during deployment)
RUN echo "SGTECHCTF{buff3r_0v3rfl0w_m4st3r}" > flag.txt

# Expose port for remote challenges
EXPOSE 1337

# Serve the binary over TCP using socat
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:./vuln,pty,stderr,setsid,sigint,sane"]

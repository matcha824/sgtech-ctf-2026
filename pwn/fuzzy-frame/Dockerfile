FROM --platform=linux/386 debian:bullseye-slim

RUN apt-get update && apt-get install -y \
    gcc \
    make \
    gdb \
    python3 \
    nano \
    openssh-server \
    zsh \
    && ln -sf /bin/zsh /bin/sh \
    && rm -rf /var/lib/apt/lists/*

# Create CTF user
RUN useradd -m -s /bin/bash ctf && \
    echo "ctf:ctf" | chpasswd

# Setup SSH
RUN mkdir -p /var/run/sshd && ssh-keygen -A
COPY setup/sshd_config /etc/ssh/sshd_config

# Copy and compile the vulnerable binary
COPY challenge/vuln.c /home/ctf/vuln.c
COPY challenge/Makefile /home/ctf/Makefile
RUN cd /home/ctf && make && \
    chown root:root vuln && \
    chmod 4755 vuln

# Copy challenge files for participant
COPY challenge/vuln_redacted.c /home/ctf/source.c
COPY challenge/exploit_template.py /home/ctf/exploit.py
RUN chmod +x /home/ctf/exploit.py && \
    chown ctf:ctf /home/ctf/source.c /home/ctf/exploit.py

# Place the flag
COPY setup/flag.txt /root/flag.txt
RUN chmod 400 /root/flag.txt

# Remove the real source and Makefile after compilation
RUN rm /home/ctf/vuln.c /home/ctf/Makefile

# Entrypoint
COPY setup/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 22
ENTRYPOINT ["/entrypoint.sh"]

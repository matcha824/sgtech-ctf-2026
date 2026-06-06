FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y gcc socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash ctf

WORKDIR /home/ctf

COPY challenge.c .
COPY Makefile .
COPY flag.txt .

# Build with container's libc and copy it to aknown path for easy extraction
RUN gcc -Wall -Wextra -o challenge challenge.c -Wl,-z,relro,-z,lazy && \
    cp $(ldd challenge | grep libc | awk '{print $3}') /home/ctf/libc.so.6 && \
    chmod 555 challenge && \
    chmod 444 flag.txt && \
    chown root:root flag.txt

USER ctf

EXPOSE 9001

CMD ["socat", "TCP-LISTEN:9001,reuseaddr,fork", "EXEC:./challenge,stderr"]
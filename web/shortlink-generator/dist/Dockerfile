# tinyshort -- CTF challenge image
#
# Base: Ubuntu 20.04 (focal). Chosen because the upstream wkhtmltopdf 0.12.6-1
# .deb is published for focal and the package is no longer in Debian/Ubuntu
# repos in newer releases. Pinning a known-vulnerable build is the whole point.
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Runtime deps for wkhtmltoimage + Python + curl (for the healthcheck sink).
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        wget \
        fontconfig \
        libjpeg-turbo8 \
        libpng16-16 \
        libssl1.1 \
        libx11-6 \
        libxcb1 \
        libxext6 \
        libxrender1 \
        xfonts-75dpi \
        xfonts-base \
        python3 \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Pinned vulnerable wkhtmltoimage (0.12.6-1, focal build). This release
# predates the file:// disclosure mitigations; --enable-local-file-access
# will happily render <iframe src="file:///..">.
# TARGETARCH is set by buildkit ("amd64" or "arm64") so this builds natively
# on both Apple Silicon and x86_64 hosts.
ARG TARGETARCH
RUN wget -q "https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_${TARGETARCH}.deb" -O /tmp/wkhtmltox.deb \
    && dpkg -i /tmp/wkhtmltox.deb \
    && rm /tmp/wkhtmltox.deb

# Application code.
WORKDIR /app
COPY app/requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
COPY app/ /app/

# Unprivileged runtime user. The flask app runs as `app`; the flag is owned by
# root. Players need to escalate to read it.
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app

# The flag. Permissions: only root can read it. The whole challenge is
# getting from `app` to `root`.
COPY flag.txt /root/flag.txt
RUN chown root:root /root/flag.txt && chmod 400 /root/flag.txt

# Misconfiguration: someone left the SUID bit on /usr/bin/find. Classic
# GTFOBin. Player goal: `find . -exec /bin/sh -p \; -quit` -> root shell.
RUN chmod u+s /usr/bin/find

EXPOSE 8080
USER app

# Single process, single port -- Flask via gunicorn.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "4", "--timeout", "30", "server:app"]

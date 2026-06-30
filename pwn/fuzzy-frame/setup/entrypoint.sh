#!/bin/bash
set -euo pipefail

echo 0 > /proc/sys/kernel/randomize_va_space

exec /usr/sbin/sshd -D

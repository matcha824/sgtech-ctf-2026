FROM ubuntu:22.04

# Install necessary packages
RUN apt-get update && apt-get install -y openssh-server cron sudo nano

# Setup SSH daemon directory
RUN mkdir /var/run/sshd

# 1. Create the lower-level user
RUN useradd -m -s /bin/bash junior_admin && \
    echo 'junior_admin:dont_get_paid_enough' | chpasswd

# 2. Create the flag in root's directory and make the directory readable
RUN echo "sgctf{cr0n_p4th_m4st3r_h3x0r}" > /root/flag.txt && \
    chmod 400 /root/flag.txt && \
    chmod 755 /root

# 3. Create the vulnerable root script that cron will execute
# It calls 'tar' without specifying /bin/tar, making it susceptible to PATH hijacking
RUN echo '#!/bin/bash\n\n# Quick hack to archive old logs before the disk fills up again\ntar -cf /dev/null /var/log/syslog 2>/dev/null' > /usr/local/bin/cleanup_logs.sh && \
    chmod 755 /usr/local/bin/cleanup_logs.sh

# 4. Setup the system crontab
# This explicitly defines the PATH and runs the script as root every minute
RUN echo 'PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin\n* * * * * root /usr/local/bin/cleanup_logs.sh\n' > /etc/crontab && \
    chmod 644 /etc/crontab

# 5. Create the PATH injector script
RUN echo '#!/bin/bash\n\nif [ -z "$1" ]; then\n  echo "Usage: sudo /opt/fix_cron_paths.sh <new_path>"\n  exit 1\nfi\n\n# Band-aid fix to update paths when the cleanup script breaks\nsed -i "s#^PATH=.*#PATH=$1#" /etc/crontab\necho "Cron paths updated! Hopefully it works this time..."' > /opt/fix_cron_paths.sh && \
    chmod 755 /opt/fix_cron_paths.sh

# 6. Allow junior_admin to run the injector script as root without a password
RUN echo 'junior_admin ALL=(root) NOPASSWD: /opt/fix_cron_paths.sh' >> /etc/sudoers

# Funsies Stuff
# Add a hidden decoy file to the junior_admin home directory
RUN echo "Friday TODO:\n- Fix the coffee machine\n- Ask senior admins why the log cleanup script keeps breaking\n- Try to figure out what a PATH is..." > /home/junior_admin/notes && \
    chown junior_admin:junior_admin /home/junior_admin/notes && \
    chmod 644 /home/junior_admin/notes

# Gotchya
RUN echo "Made you look" > /home/junior_admin/.secret && \
    chown junior_admin:junior_admin /home/junior_admin/.secret \
    chmod 000 /home/junior_admin/.secret

# Expose SSH port
EXPOSE 22

# Start both Cron and SSH in the foreground
CMD service cron start && /usr/sbin/sshd -D
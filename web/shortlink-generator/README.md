# CTF Web Challenge

Challenge Name: Short-link Generator Stage 1

Challenge Description: This website looks helpful, it even takes screenshots of the page so I can share my short-link on my socials and get a nice embeded preview screenshot.

The Flack server is running the Python script at /app/server.py
Not that this helps you or anything because you probably can't read the source code xD

Challenge Name: Short-link Generator Stage 2

Challenge Description: The developer made a grave error in the healthcheck endpoint as well as the setup of the Docker image by following someone's random guide online.

They have stored some hidden information in /root/flag.txt


## Detailed Description

The team will be presented with a Dockerfile hosted frontend of a Python service that takes any given link and shortens it with the service. The problem of the service is that it takes a snapshot of the resulting page and saves it as the thumbnail to display for hotlinking and embeds for things like Twitter, Facebook, or Discord rich displays.

This thumnail process is cool, it makes the service vulnerable to attack since the service has to visit the provided website (possibly malicious)

The attack vector will be:

* Use a vulnerable website to PNG library to dump the website's source code
* Find a privilege escalation because of a vulnerability through the source code
* Find the flag in the system.

## Security Vulnerability / Topics Covered

1. CVEs/Zero-days
2. Infrastructure reconnaissance
3. Privilege escalation

---

# Design (author notes)

> Internal design doc for building/reviewing the challenge. Strip before publishing to players.

## Vuln chain (3 stages)

### Stage 1 — File disclosure via wkhtmltoimage (CVE-2022-35583 / CVE-2020-21365)

- The app runs `wkhtmltoimage --enable-local-file-access <user_url> /tmp/out.png` on every submitted URL.
- Player submits a URL pointing to attacker-controlled HTML containing `<iframe src="file:///app/server.py">` (or `/etc/passwd`, `/proc/self/environ`, etc.).
- wkhtmltoimage renders the iframe into the PNG → player reads arbitrary files via the preview image.
- Recon goal: read `/app/server.py` to discover the Stage 2 sink.

### Stage 2 — RCE via the source they just leaked

- `server.py` contains a command-injection sink reachable from the same URL field. Leaning toward: the screenshot command itself uses `shell=True` interpolation with **partial** character filtering. Players have to read the source (via Stage 1) to find the filter gap and craft an injection that gets through.
- Alternative: a separate "URL health check" endpoint with a `subprocess.run(f"curl -I {url}", shell=True)` sink. Cleaner but makes Stage 1 optional, which weakens the chain.
- Decision pending — see "Open decisions" below.
- Yields RCE as the unprivileged `app` user inside the container.

### Stage 3 — SUID privesc to root → flag

- Container has one out-of-place SUID-root binary. Two flavors under consideration:
  - **GTFOBin** like `/usr/bin/find` (or `env`, `vim`) with the SUID bit set. Player runs `find . -exec /bin/sh -p \; -quit`. Highly discoverable, classic technique.
  - **Custom wrapper** — small C binary like `/usr/local/bin/url-fetch` that's SUID-root and `system("curl ...")`s with user-controlled args → PATH hijack or arg injection.
- Flag read from `/root/flag.txt` after privesc.

## File layout

```
web/shortlink-generator/
├── README.md              # this file (challenge desc + author notes)
├── dist/                  # what players get
│   ├── Dockerfile         # same one used to build the live container
│   ├── docker-compose.yml
│   └── app/
│       ├── server.py
│       ├── requirements.txt
│       └── templates/index.html
├── src/                   # build context (mirrors dist/ + flag placement)
│   ├── Dockerfile
│   ├── app/...
│   └── flag.txt           # baked into image at /root/flag.txt
└── solve/
    ├── flag.txt           # the flag string
    ├── solve-writeup.md   # full solution walkthrough
    ├── attacker.html      # iframe payload for Stage 1
    └── solve.py           # automated solver
```

The repo-level contributing guide doesn't standardize `dist/` explicitly but step 8 references it — including it here.

## Open decisions

1. **Stage 2 RCE flavor** — screenshot command itself (forces Stage 1) vs. separate health-check endpoint (cleaner narrative).
2. **SUID flavor** — GTFOBin (easier, googleable) vs. custom wrapper (more interesting). Leaning GTFOBin for medium.
3. **Network egress** — assume players can host their own page on the internet for the iframe payload? Standard CTF assumption.
4. **wkhtmltopdf vs wkhtmltoimage** — going with `wkhtmltoimage` (matches the "thumbnail" story); same CVE class.
5. **Red herrings** — keep lean for medium, or add a fake admin login / safe-but-suspicious endpoint? Leaning lean.

## Player-facing topic alignment

- **CVEs/Zero-days** → CVE-2022-35583 / CVE-2020-21365 (wkhtmltoimage file:// disclosure).
- **Infrastructure reconnaissance** → reading `server.py`, `/etc/passwd`, `/proc/self/environ` to map the app and find the next sink.
- **Privilege escalation** → SUID misconfig in the container.

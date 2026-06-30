"""
Short-link Generator
--------------------
Submit a URL, get back a short code plus a thumbnail screenshot of the page.

Routes:
    GET  /                    landing page
    POST /shorten             create a short link (renders thumbnail via wkhtmltoimage)
    GET  /s/<code>            redirect to the original URL
    GET  /preview/<code>.png  thumbnail image
    GET  /healthcheck         operator utility: HEAD-checks a URL with curl
"""
from __future__ import annotations

import os
import secrets
import string
import subprocess
from urllib.parse import urlparse

from flask import (
    Flask,
    abort,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
PREVIEW_DIR = "/tmp/previews"
os.makedirs(PREVIEW_DIR, exist_ok=True)

# This is a relatively secure place to store a secret right?
# Since the user would never be able to get my source code...
DEPLOY_TOKEN = "sgctf{never_trust_users_with_your_application}"

app = Flask(__name__)

# in-memory store: code -> original URL
LINKS: dict[str, str] = {}


def _new_code(n: int = 6) -> str:
    alphabet = string.ascii_letters + string.digits
    while True:
        code = "".join(secrets.choice(alphabet) for _ in range(n))
        if code not in LINKS:
            return code


def _is_http_url(url: str) -> bool:
    try:
        p = urlparse(url)
    except ValueError:
        return False
    return p.scheme in ("http", "https") and bool(p.netloc)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/shorten", methods=["POST"])
def shorten():
    url = (request.form.get("url") or "").strip()
    if not _is_http_url(url):
        return render_template("index.html", error="Please provide a valid http(s) URL."), 400

    code = _new_code()
    LINKS[code] = url

    out_path = os.path.join(PREVIEW_DIR, f"{code}.png")
    try:
        subprocess.run(
            [
                "wkhtmltoimage",
                "--enable-local-file-access",
                "--javascript-delay", "1500",
                "--quiet",
                "--width", "1024",
                url,
                out_path,
            ],
            timeout=30,
            check=False,
        )
    except subprocess.TimeoutExpired:
        pass

    preview_url = url_for("preview", code=code) if os.path.exists(out_path) else None
    short_url = url_for("follow", code=code, _external=True)
    return render_template(
        "index.html",
        short_url=short_url,
        preview_url=preview_url,
        original=url,
    )


@app.route("/s/<code>")
def follow(code):
    target = LINKS.get(code)
    if not target:
        abort(404)
    return redirect(target, code=302)


@app.route("/preview/<code>.png")
def preview(code):
    if not code.isalnum():
        abort(404)
    path = os.path.join(PREVIEW_DIR, f"{code}.png")
    if not os.path.exists(path):
        abort(404)
    return send_from_directory(PREVIEW_DIR, f"{code}.png", mimetype="image/png")


@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    """Operator utility: quick HEAD check on a URL to make sure it's reachable."""
    url = (request.args.get("url") or "").strip()
    if not url:
        return "usage: /healthcheck?url=https://example.com", 400

    try:
        result = subprocess.run(
            f"curl -sS -I --max-time 5 {url}",
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except subprocess.TimeoutExpired:
        return "timeout", 504

    body = (result.stdout or "") + (result.stderr or "")
    return f"<pre>{body}</pre>", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

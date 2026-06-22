from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import base64
import hashlib
import hmac
import json

HOST = "0.0.0.0"
PORT = 80
JWT_SECRET = "ZeroDay"
FLAG = "sgctf{gabriel_winter_needs_a_better_jwt_secret}"

ROOT = Path(__file__).resolve().parent
STATIC_FILES = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/index.html": ("index.html", "text/html; charset=utf-8"),
    "/app.js": ("app.js", "application/javascript; charset=utf-8"),
    "/styles.css": ("styles.css", "text/css; charset=utf-8"),
}

USERS = {
    "guest": {
        "password": "ride_the_lightning",
        "payload": {"name": "guest", "role": "guest"},
    }
}


def b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def b64url_decode(value: str) -> bytes:
    value += "=" * ((4 - len(value) % 4) % 4)
    return base64.urlsafe_b64decode(value.encode())


def create_jwt(payload: dict) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    encoded_header = b64url_encode(json.dumps(header, separators=(",", ":")).encode())
    encoded_payload = b64url_encode(json.dumps(payload, separators=(",", ":")).encode())
    signing_input = f"{encoded_header}.{encoded_payload}"
    signature = hmac.new(
        JWT_SECRET.encode(), signing_input.encode(), hashlib.sha256
    ).digest()
    return f"{signing_input}.{b64url_encode(signature)}"


def extract_bearer(auth_header: str | None) -> str | None:
    if not auth_header:
        return None
    auth_header = auth_header.strip()
    if auth_header.lower().startswith("authorization: bearer "):
        return auth_header[len("authorization: bearer "):].strip()
    if auth_header.lower().startswith("bearer "):
        return auth_header[len("bearer "):].strip()
    return auth_header


def verify_jwt(token: str | None) -> dict | None:
    if not token:
        return None
    try:
        encoded_header, encoded_payload, signature = token.split(".")
        header = json.loads(b64url_decode(encoded_header))
        if header.get("alg") != "HS256":
            return None

        signing_input = f"{encoded_header}.{encoded_payload}"
        expected = b64url_encode(
            hmac.new(JWT_SECRET.encode(), signing_input.encode(), hashlib.sha256).digest()
        )
        if not hmac.compare_digest(signature, expected):
            return None

        payload = json.loads(b64url_decode(encoded_payload))
        return payload
    except Exception:
        return None


class Handler(BaseHTTPRequestHandler):
    def send_text(self, status: int, body: str, content_type: str = "text/plain; charset=utf-8"):
        data = body.encode()
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def send_json(self, status: int, obj: dict):
        self.send_text(status, json.dumps(obj), "application/json; charset=utf-8")

    def do_GET(self):
        path = self.path.split("?", 1)[0]

        if path in STATIC_FILES:
            filename, content_type = STATIC_FILES[path]
            target = ROOT / filename
            if not target.exists():
                self.send_text(404, "Not found")
                return
            data = target.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return

        if path == "/api/session":
            token = extract_bearer(self.headers.get("Authorization"))
            payload = verify_jwt(token)
            if not payload:
                self.send_json(401, {"authenticated": False})
                return
            self.send_json(200, {"authenticated": True, "user": payload})
            return

        if path == "/api/flag":
            token = extract_bearer(self.headers.get("Authorization"))
            payload = verify_jwt(token)
            if payload == {"name": "admin", "role": "admin"}:
                self.send_json(200, {"flag": FLAG})
                return
            self.send_json(403, {"error": "forbidden"})
            return

        self.send_text(404, "Not found")

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        if path != "/api/login":
            self.send_text(404, "Not found")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length).decode()
            data = json.loads(body or "{}")
        except Exception:
            self.send_json(400, {"error": "bad request"})
            return

        username = str(data.get("username", "")).strip()
        password = str(data.get("password", ""))
        user = USERS.get(username)
        if not user or user["password"] != password:
            self.send_json(401, {"error": "invalid credentials"})
            return

        token = create_jwt(user["payload"])
        self.send_json(200, {"authorization": f"Bearer {token}"})

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    HTTPServer((HOST, PORT), Handler).serve_forever()

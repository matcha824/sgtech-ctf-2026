# Name
Path Traversal

# Flag
Contained in `solve/flag.txt`

# Message
We secured our new API with OAuth 2.0 and DPoP, the modern proof-of-possession scheme that cryptographically binds every access token to its owner's key. Register a client, prove you hold your key, and you'll be granted access to the public endpoints. The flag, of course, lives somewhere more private that your token was never meant to reach. Our access checks are airtight, though. Can you prove us wrong?
The first port points to the authentication server. The second port points to the resource server.

# Files to include with the challenge
`Dockerfile`, `src/servers/**` -> containerize please


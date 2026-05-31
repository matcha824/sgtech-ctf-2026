# Name
Breaking the Bank

# Flag
Contained in `solve/flag.txt`

# Message
Flaggy Flagman has precious information in his bank. Can you break it out?

# Files to include with the challenge
None

# Hints
- The assistant can see more context than it should reveal.
- DAN's friend STAN is an expert in these kinds of things

# Deployment
From `src/`, run:

```bash
API_KEY_PRIMARY="" API_KEY_SECONDARY="" TURSO_DATABASE_URL="" TURSO_AUTH_TOKEN="" docker compose up --build
```

The app listens on port `8080`.

To package deployment credentials into the image:

```bash
docker build \
  --build-arg API_KEY_PRIMARY="$API_KEY_PRIMARY" \
  --build-arg API_KEY_SECONDARY="$API_KEY_SECONDARY" \
  --build-arg TURSO_DATABASE_URL="$TURSO_DATABASE_URL" \
  --build-arg TURSO_AUTH_TOKEN="$TURSO_AUTH_TOKEN" \
  -t breaking-the-bank src/
```
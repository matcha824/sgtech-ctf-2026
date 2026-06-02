# Paste-it Notes

Medium difficulty web challenge.

Paste-it Notes is a small pastebin app with a Node.js frontend and a Go backend. The frontend proxies API requests to the backend, and the backend seeds the flag as the first paste in memory. The intended solve path is a request smuggling bug that lets a smuggled request change backend state so the hidden flag becomes accessible. The flag is not returned directly by the smuggled request; players must make one more normal request to retrieve it.

## Goal

Recover the hidden flag from the paste store.

## Run

In `./src`

```
docker build -t paste-it-notes .; docker run -p 3000:3000 -t paste-it-notes
```

## Reference Solve

See `solve.py` for the reference exploit flow and `solve.md` for the challenge notes.

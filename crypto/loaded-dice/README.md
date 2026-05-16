# Name
Loaded Dice

# Flag
Contained in `solve/flag.txt`

# Message
The dealer swears the new electronic dice rolls completely random numbers every single time. But I managed to grab a copy of their encryption script, and I'm pretty sure the game is rigged. Can you beat the house and decrypt this file?

# Files to include with the challenge
`encrypt.py`, `flag.enc`

# Hints
- A "random" number generator is only random if you don't know where it starts.
- Python's `random` module is fully deterministic when seeded.

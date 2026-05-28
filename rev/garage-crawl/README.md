# Name
Garage Crawl

# Flag
Contained in `solve/flag.txt`

# Message
You're stuck in a parking garage, and the exit gate won't open without a valid ticket code. The system handed you a receipt, but the barcode reader is busted. All you managed to grab was the garage's ticket validation program. Reverse-engineer it and figure out the code to escape. 

# Files to include with the challenge
`dist.pyc`

# Hints
- Python bytecode can be decompiled. Look for tools that support Python 3.13.
- What's hiding under the base64?
- The "random" number generator isn't random at all if you know the seed.

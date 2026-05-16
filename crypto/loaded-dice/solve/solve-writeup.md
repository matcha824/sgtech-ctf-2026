# Loaded Dice - Solution Writeup

## Vulnerability
The encryption script uses Python's `random` module to generate the keystream for an XOR cipher, but explicitly seeds it with the hardcoded integer `1337`. Python's `random` is a Mersenne Twister PRNG — fully deterministic from its seed. Because the seed is visible in the source code shipped to players, the entire keystream is reproducible, making the XOR encryption trivially reversible.

## Solution Steps
1. Read `encrypt.py` and identify the hardcoded seed: `random.seed(1337)`.
2. Read the hex string from `flag.enc` and convert it back to bytes.
3. In a new script, seed `random` with the same value.
4. For each encrypted byte, call `random.randint(0, 255)` to regenerate the keystream byte, then XOR it with the encrypted byte to recover the plaintext byte.
5. Concatenate the recovered bytes. The result is `tdpCTF{p53ud0_r4nd0m_15_n0t_s3cur3}`.

## Running the solve
From `solve/`:

```
python3 solve.py
```

Expected output: `Recovered Flag: tdpCTF{p53ud0_r4nd0m_15_n0t_s3cur3}`

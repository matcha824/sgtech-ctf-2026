# Solve Writeup

## Overview

The challenge provides a text file containing one public exponent, three RSA moduli, and three ciphertexts.

Each ciphertext is an encryption of the same plaintext flag under a different RSA modulus.

The mistake is that the same unpadded message was encrypted multiple times using a small public exponent:

~~~text
e = 3
~~~

This creates the conditions for Håstad's broadcast attack. By combining the ciphertexts with the Chinese Remainder Theorem, the original message can be recovered without factoring any of the RSA moduli.

## Initial Analysis

The challenge provides three separate RSA encryptions:

~~~text
c_1 = m^3 mod N_1
c_2 = m^3 mod N_2
c_3 = m^3 mod N_3
~~~

The plaintext value `m` is the same in all three equations. Only the moduli are different.

Normally, reducing an encrypted value modulo `N` prevents directly recovering the original plaintext. However, because the same message was encrypted three times with `e = 3`, the three ciphertexts provide enough information to reconstruct `m^3`.

The key observations are:

- The public exponent is small: `e = 3`.
- The same plaintext was reused for all three ciphertexts.
- The plaintext was encrypted without randomized padding.
- The three moduli are different.

## Walk-through

For each recipient, RSA encryption produces:

~~~text
c_i = m^e mod N_i
~~~

Since `e = 3`, the provided ciphertexts satisfy:

~~~text
c_1 = m^3 mod N_1
c_2 = m^3 mod N_2
c_3 = m^3 mod N_3
~~~

The Chinese Remainder Theorem allows these three modular equations to be combined into one value modulo the product of the moduli:

~~~text
N = N_1 * N_2 * N_3
~~~

Using the three ciphertexts and moduli, it is possible to compute a value `C` such that:

~~~text
C = m^3 mod N
~~~

Because the flag is small compared to the combined size of the three RSA moduli, its cube is also smaller than their product:

~~~text
m^3 < N_1 * N_2 * N_3
~~~

This means that no modular wraparound occurred after the ciphertexts were combined. Therefore:

~~~text
C = m^3
~~~

not merely:

~~~text
C = m^3 mod N
~~~

Once the exact value of `m^3` is known, recovering the plaintext only requires computing the exact integer cube root.

The recovered integer `m` can then be converted back into readable text to reveal the flag.

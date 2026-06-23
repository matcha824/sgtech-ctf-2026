# Solve Writeup

## Overview

The challenge provides a text file containing three RSA values: `N`, `e`, and `c`.

At first glance, this looks like a normal RSA challenge. `N` is the modulus, `e` is the public exponent, and `c` is the ciphertext.

The weakness is not in the ciphertext or the exponent. The weakness is in how the RSA modulus was generated.

## Initial Analysis

The most important value to inspect is `N`.

In a properly generated RSA challenge, `N` should be the product of two large odd primes. Since the product of two odd numbers is also odd, a normal RSA modulus should be odd.

However, this challenge's `N` is even.

That observation immediately reveals that one of the factors of `N` is `2`.

## Why This Breaks the Challenge

RSA depends on the fact that factoring `N` should be difficult. If an attacker can factor `N`, then they can recover the private key and decrypt the ciphertext.

Normally, an RSA modulus has the form:

~~~text
N = p * q
~~~

where `p` and `q` are both large prime numbers.

In this challenge, `N` is even, which means it is divisible by `2`. Therefore, one factor is immediately known:

~~~text
q = 2
~~~

The other factor can be recovered with:

~~~text
p = N / 2
~~~

Once both factors are known, the totient can be computed. For RSA, the totient is usually:

~~~text
phi(N) = lcm(p - 1, q - 1)
~~~

Since `q = 2`, this becomes:

~~~text
phi(N) = lcm(p - 1, 2 - 1)
phi(N) = lcm(p - 1, 1)
phi(N) = p - 1
~~~

With the totient known, the private exponent `d` can be calculated as the modular inverse of `e`:

~~~text
d = e^(-1) mod phi(N)
~~~

Finally, the ciphertext can be decrypted using:

~~~text
m = c^d mod N
~~~

The decrypted value `m` is the original plaintext message encoded as a number. Converting that number back into text reveals the flag.

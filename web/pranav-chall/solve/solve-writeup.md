# Flaming Backdoor - Solution

The strategy is to use the Hypothesis library as a random input generator to the function `is_ip_address_in_cidr_block` and to use an oracle (source of truth) to find inputs that can the function to generate incorrect. Output. Check out `solution.py` for such an implementation using the `ipaddress` library as an oracle.

When you run `solution.py`, you get something like the following
```
PS C:\Users\navee\Documents\sgtech-ctf-2026\web\pranav-chall> pipenv run python .\solve\solution.py
FOUND BUG: 224.181.147.84 in 37.68.133.241/26 - got True, expected False
FOUND BUG: 224.181.147.133 in 37.68.133.241/26 - got True, expected False
FOUND BUG: 224.181.68.133 in 37.68.133.241/26 - got True, expected False
FOUND BUG: 68.181.68.133 in 37.68.133.241/26 - got True, expected False
FOUND BUG: 68.181.68.133 in 37.133.133.241/26 - got True, expected False
FOUND BUG: 68.181.133.133 in 37.133.133.241/26 - got True, expected False
FOUND BUG: 68.181.133.133 in 133.133.133.241/26 - got True, expected False
FOUND BUG: 248.67.45.255 in 115.255.64.209/26 - got True, expected False
FOUND BUG: 26.67.45.255 in 115.255.64.209/26 - got True, expected False
FOUND BUG: 26.67.45.26 in 115.255.64.209/26 - got True, expected False
FOUND BUG: 26.67.45.45 in 115.255.64.209/26 - got True, expected False
FOUND BUG: 26.67.45.64 in 115.255.64.209/26 - got True, expected False
FOUND BUG: 204.4.158.238 in 103.185.255.211/26 - got True, expected False
FOUND BUG: 204.255.158.238 in 103.185.255.211/26 - got True, expected False
FOUND BUG: 204.204.158.238 in 103.185.255.211/26 - got True, expected False
FOUND BUG: 211.204.158.238 in 103.185.255.211/26 - got True, expected False
FOUND BUG: 211.103.158.238 in 103.185.255.211/26 - got True, expected False
FOUND BUG: 211.103.158.238 in 103.103.255.211/26 - got True, expected False
FOUND BUG: 27.148.108.6 in 95.224.200.41/26 - got True, expected False
FOUND BUG: 27.148.108.148 in 95.224.200.41/26 - got True, expected False
FOUND BUG: 224.148.108.148 in 95.224.200.41/26 - got True, expected False
```

The flag is the number that is common among all the failing inputs - 26. The backdoor is that a prefix length of 26 results in the function always outputing `True`, no matter the ip address.

Check out `main.py` to see the source code of `is_ip_address_in_cidr_block`.
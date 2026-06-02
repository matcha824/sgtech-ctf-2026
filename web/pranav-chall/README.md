# Flaming Backdoor

You recently joined Inferno technologies, a company that specializes in developing firewalls. Recently, the company's firewalls have become immensely popular among the software industry, particularly due to FlameThrower, the company's extremely efficient, open source firewall implementation. Due to the immense popularity, Ember, the company's CEO, worries that some external contributors may be hackers who are injecting backdoors into FlameThrower.

To find potential backdoors, Ember has hired you as a pen tester for Inferno technologies. She wants you to analyse FlameThrower's `is_ip_address_in_cidr_block(ip_address, cidr_block)` function, a function that determines if a given ip address lies within a given cidr block. To help you with your task, she has found the python library [Hypothesis](https://hypothesis.readthedocs.io/en/latest/), a tool which can try hundreds of inputs to try to break functions.

## Goal

Explore what test cases cause `is_ip_address_in_cidr_block` to deliver incorrect output (`Fals`' when it should output `True` or vice versa). Use the Hypothesis python library. The flag is a number that is common among the failing test cases.

## Getting Started

1. Run `pipenv install` to install all dependencies
2. Run `pipenv run python experiment.py` and explore / modify the file

Ignore `main.py` and `pyarmor_runtime_000000/*`. This is the obfuscated source code of `is_ip_address_in_cidr_block`.
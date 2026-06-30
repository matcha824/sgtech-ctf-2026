# Flaming Backdoor

You recently joined Inferno technologies, a company that specializes in developing firewalls. Recently, the company's firewalls have become immensely popular among the software industry, particularly due to FlameThrower, the company's extremely efficient, open source firewall implementation. Due to the immense popularity, Ember, the company's CEO, worries that some external contributors may be hackers who are injecting backdoors into FlameThrower.

To find potential backdoors, Ember has hired you as a pen tester for Inferno technologies. She wants you to analyse FlameThrower's `is_ip_address_in_cidr_block(ip_address, cidr_block)` function, a function that determines if a given ip address lies within a given cidr block. To help you with your task, she has found the python library [Hypothesis](https://hypothesis.readthedocs.io/en/latest/), a tool which can try hundreds of inputs to try to break functions.

## Challenge Goal

Explore what test cases cause `is_ip_address_in_cidr_block` to deliver incorrect output (`False` when it should output `True` or vice versa). Use the Hypothesis python library. The flag is a number that is common among the failing test cases. Your submission will be in the format `sgctf{ENTER COMMON NUMBER HERE}`.

## Getting Started

1. Install `pipenv` using [this guide](https://pipenv.pypa.io/en/latest/installation.html)
2. Run `pipenv install` to install all dependencies
3. Run `pipenv run python experiment.py` and explore / modify the file

Ignore `main.pyc`. This is the compiled source code of `is_ip_address_in_cidr_block`. The code is obfuscated via compilation so that you focus on using Hypothesis to solve the challenge instead of reviewing source code.

## Learning Goal

The learning goal of the challenge was to expose you to property based testing. Property based testing is a strategy to augment unit testing by making sure code works on 100s of random inputs, rather than a single, static input. Property based testing can help uncover bugs in newly created functionality and can make sure no bugs are introduced when old functionality is refactored or modified. Hypothesis is one of the ways of doing property based testing with python.

## Usage of AI

Permissible Uses of AI for this challenge

- understanding CIDR and IP address concepts
- understanding python and pipenv
- exploring and understanding libraries, such as `hypothesis` or `ipaddress`
- understanding the code in `experiment.py`

Non-permissible uses of AI

- giving all the project files and asking for a solution

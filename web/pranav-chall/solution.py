from hypothesis import given, settings, strategies as st
from main import is_ip_address_in_cidr_block
import ipaddress


# Strategy to generate valid IPv4 bytes (0-255)
def ipv4_byte():
    return st.integers(min_value=0, max_value=255).map(str)


# Strategy to generate valid IPv4 addresses
def ipv4_address():
    return st.tuples(ipv4_byte(), ipv4_byte(), ipv4_byte(), ipv4_byte()).map(
        lambda x: ".".join(x)
    )


# Strategy to generate valid CIDR blocks
def cidr_block():
    return st.tuples(
        ipv4_byte(),
        ipv4_byte(),
        ipv4_byte(),
        ipv4_byte(),
        st.integers(min_value=0, max_value=32),
    ).map(lambda x: f"{x[0]}.{x[1]}.{x[2]}.{x[3]}/{x[4]}")


@given(ip=ipv4_address(), cidr=cidr_block())
@settings(max_examples=1000)
def test_find_bugs(ip, cidr):
    result = is_ip_address_in_cidr_block(ip, cidr)

    # Use ipaddress library as oracle
    ip_obj = ipaddress.IPv4Address(ip)
    network = ipaddress.IPv4Network(cidr, strict=False)
    expected = ip_obj in network

    if result != expected:
        print(f"FOUND BUG: {ip} in {cidr} - got {result}, expected {expected}")


test_find_bugs()

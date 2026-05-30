from hypothesis import given, settings, strategies as st
from main import is_ip_address_in_cidr_block
import ipaddress


# Strategy to generate valid IPv4 octets (0-255)
def ipv4_octet():
    return st.integers(min_value=0, max_value=255)


# Strategy to generate valid IPv4 addresses
def ipv4_address():
    return st.tuples(ipv4_octet(), ipv4_octet(), ipv4_octet(), ipv4_octet()).map(
        lambda x: ".".join(map(str, x))
    )


# Strategy to generate valid CIDR blocks
def cidr_block():
    return st.tuples(
        ipv4_octet(),
        ipv4_octet(),
        ipv4_octet(),
        ipv4_octet(),
        st.integers(min_value=0, max_value=32),
    ).map(lambda x: f"{x[0]}.{x[1]}.{x[2]}.{x[3]}/{x[4]}")


@given(ip=ipv4_address(), cidr=cidr_block())
@settings(max_examples=10000)
def test_find_bugs(ip, cidr):
    print("Trying", ip, "and", cidr)

    result = is_ip_address_in_cidr_block(ip, cidr)
    # Use ipaddress library as oracle
    ip_obj = ipaddress.IPv4Address(ip)
    network = ipaddress.IPv4Network(cidr, strict=False)
    expected = ip_obj in network

    if result != expected:
        print(f"FOUND BUG: {ip} in {cidr} - got {result}, expected {expected}")
    assert result == expected


if __name__ == "__main__":
    # Run the property-based tests
    test_find_bugs()
    print("All Hypothesis tests passed!")

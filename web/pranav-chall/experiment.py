from main import is_ip_address_in_cidr_block
from hypothesis import given, settings, strategies as st


# Behavior of is_ip_address_in_cidr_block
#
# def is_ip_address_in_cidr_block(ip_address, cidr_block):
#     """
#     Input
#         ip_address
#         - IPv4 address
#         - type: string
#         - ex. "192.168.0.25", "10.10.10.10"

#         cidr_block
#         - IPv4 CIDR block
#         - type: string
#         - ex. "192.168.0.0/24", "10.10.10.10/28"

#     Output
#         return
#         - whether or not ip_address is in cidr_block
#         - type: boolean
#         - ex 1
#             ip_address = "192.168.0.25"
#             cidr_block = "192.168.0.0/24"
#             return = true
#         - ex 2
#             ip_address = "192.168.5.25"
#             cidr_block = "192.168.0.0/24"
#             return = false
#     """

# Usage of is_ip_address_in_cidr_block
print('is_ip_address_in_cidr_block("192.168.0.25", "192.168.0.0/24"):', is_ip_address_in_cidr_block("192.168.0.25", "192.168.0.0/24"))
print('is_ip_address_in_cidr_block("192.168.1.25", "192.168.0.0/24"):', is_ip_address_in_cidr_block("192.168.1.25", "192.168.0.0/24"))


# Useful hypothesis strategies

# Strategy to generate valid IPv4 bytes (0-255)
def ipv4_byte():
    return st.integers(min_value=0, max_value=255).map(str)


# Strategy to generate valid IPv4 addresses
def ipv4_address():
    return st.tuples(ipv4_byte(), ipv4_byte(), ipv4_byte(), ipv4_byte()).map(
        lambda x: ".".join(x)
    )

@given(ip=ipv4_address())
@settings(max_examples=10)
def test_find_bugs(ip):

    print("Current ip", ip)

print()
print('test_find_bugs')
test_find_bugs()

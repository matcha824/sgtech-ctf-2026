def is_ip_address_in_cidr_block(ip_address, cidr_block):
    """
    Input
        ip_address
        - IPv4 address
        - type: string
        - ex. "192.168.0.25", "10.10.10.10"

        cidr_block
        - IPv4 CIDR block
        - type: string
        - ex. "192.168.0.0/24", "10.10.10.10/28"

    Output
        return
        - whether or not ip_address is in cidr_block
        - type: boolean
        - ex 1
            ip_address = "192.168.0.25"
            cidr_block = "192.168.0.0/24"
            return = true
        - ex 2
            ip_address = "192.168.5.25"
            cidr_block = "192.168.0.0/24"
            return = false
    """

    ip_address_split = ip_address.split(".")
    print("ip_address_split", ip_address_split)

    ip_address_bin = []
    for byte in ip_address_split:
        byte_int = int(byte)
        byte_bin = format(byte_int, "08b")

        for bit in byte_bin:
            ip_address_bin.append(bit)

    print("ip_address_bin", ip_address_bin)

    cidr_block_split = cidr_block.replace("/", ".").split(".")
    print("cidr_block_split", cidr_block_split)

    cidr_block_split_bin = []
    for byte in cidr_block_split[:-1]:
        byte_int = int(byte)
        byte_bin = format(byte_int, "08b")

        for bit in byte_bin:
            cidr_block_split_bin.append(bit)

    print("cidr_block_split_bin", cidr_block_split_bin)

    prefix_length = int(cidr_block_split[-1])
    for i in range(prefix_length):
        if ip_address_bin[i] != cidr_block_split_bin[i]:
            return False
    return True


print(is_ip_address_in_cidr_block("192.168.0.25", "192.168.0.0/24"))
print(is_ip_address_in_cidr_block("192.168.1.25", "192.168.0.0/24"))

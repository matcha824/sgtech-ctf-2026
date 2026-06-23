import sys

matches = {}
def find_patterns(data):

    min_len = 16

    for i in range(len(data) - min_len + 1):
        # assuming that the function structure is identical for code that is similar, we can match the bytes exactly of the assembly
        if (
            data[i] == 0x35 and
            data[i + 15] == 0x83 and
            data[i + 16] == 0xF8
        ): 
            # the lock tells you which order it should be in, let's harvest it
            pinNum = data[i+17]
            # this is the pin that we need to match
            matches[pinNum] = data[i+1] + (data[i+2]<<8) + (data[i+3]<<16) + (data[i+4]<<24)

    return matches

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <binary_file>")
        sys.exit(1)

    filename = sys.argv[1]

    with open(filename, "rb") as f:
        data = f.read()

    find_patterns(data)

    if not matches:
        print("No matches found.")
        return

    print(f"Found {len(matches)} matches:")
    print(matches)
    matches[0] = 1
    
    for i in range(1, len(matches)):
        print(f"r.call(e.symbols[\"pin{i-1}\"], [{matches[i] * pow(matches[i-1], 1000000005, 1000000007) % 1000000007}])")
    

if __name__ == "__main__":
    main()
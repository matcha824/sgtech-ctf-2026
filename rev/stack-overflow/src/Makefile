all:
	gcc vuln.c -o vuln -fno-stack-protector -no-pie -z execstack -g

clean:
	rm -f vuln

# Notes:
# -fno-stack-protector: Disable stack canary checks
# -no-pie: Disable position-independent executable
# -z execstack: Make stack executable (for shellcode)
# -g: Include debug information

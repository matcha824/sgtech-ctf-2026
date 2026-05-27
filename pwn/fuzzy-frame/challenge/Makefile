CC      = gcc
CFLAGS  = -m32 -g -fno-stack-protector -z execstack -no-pie
BUF_SIZE = 232

vuln: vuln.c
	$(CC) $(CFLAGS) -DBUF_SIZE=$(BUF_SIZE) -o vuln vuln.c
	chown root:root vuln
	chmod 4755 vuln

clean:
	rm -f vuln

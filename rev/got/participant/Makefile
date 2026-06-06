CC = gcc
CFLAGS = -Wall -Wextra
SRC = challenge.c
BIN = challenge

# Detect OS: Linux gets Partial RELRO; macOS skips unsupported linker flags
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
    # PIE enabled (default), Partial RELRO (writable GOT), NX enabled
    # -z,lazy overrides modern GCC's default Full RELRO
    LDFLAGS = -Wl,-z,relro,-z,lazy
else
    LDFLAGS =
endif

.PHONY: all clean

all: $(BIN)

$(BIN): $(SRC)
    $(CC) $(CFLAGS) -o $(BIN) $(SRC) $(LDFLAGS)

clean:
    rm -f $(BIN)
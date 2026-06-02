//go:build darwin

package main

import (
	"fmt"
	"os"
	"syscall"
	"unsafe"
)

func isTerminal() bool {
	var termios [256]byte
	_, _, err := syscall.Syscall6(
		syscall.SYS_IOCTL,
		os.Stdout.Fd(),
		syscall.TIOCGETA,
		uintptr(unsafe.Pointer(&termios[0])),
		0, 0, 0,
	)
	return err == 0
}

func clearScreen() {
	fmt.Print("\033[2J\033[3J\033[H")
}

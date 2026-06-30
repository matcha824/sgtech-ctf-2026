//go:build windows

package main

import (
	"fmt"
	"os"
	"syscall"
	"unsafe"
)

var (
	kernel32                       = syscall.NewLazyDLL("kernel32.dll")
	procGetConsoleMode             = kernel32.NewProc("GetConsoleMode")
	procSetConsoleMode             = kernel32.NewProc("SetConsoleMode")
	procGetStdHandle               = kernel32.NewProc("GetStdHandle")
	procSetConsoleCursorPosition   = kernel32.NewProc("SetConsoleCursorPosition")
	procFillConsoleOutputCharacter = kernel32.NewProc("FillConsoleOutputCharacterW")
	procFillConsoleOutputAttribute = kernel32.NewProc("FillConsoleOutputAttribute")
	procGetConsoleScreenBufferInfo = kernel32.NewProc("GetConsoleScreenBufferInfo")
)

const (
	stdOutputHandle          = ^uintptr(0) - 1 + 1 // STD_OUTPUT_HANDLE = -11
	enableVirtualTerminal    = 0x0004
)

func init() {
	// Enable ANSI escape codes on Windows 10+
	handle, _, _ := procGetStdHandle.Call(uintptr(0xFFFFFFF5)) // STD_OUTPUT_HANDLE
	var mode uint32
	procGetConsoleMode.Call(handle, uintptr(unsafe.Pointer(&mode)))
	procSetConsoleMode.Call(handle, uintptr(mode|enableVirtualTerminal))
}

func isTerminal() bool {
	handle, _, _ := procGetStdHandle.Call(uintptr(0xFFFFFFF5))
	var mode uint32
	ret, _, _ := procGetConsoleMode.Call(handle, uintptr(unsafe.Pointer(&mode)))
	return ret != 0
}

func clearScreen() {
	// Try ANSI first (Windows 10+)
	fmt.Print("\033[2J\033[3J\033[H")
	// Fallback: also use console API
	handle, _, _ := procGetStdHandle.Call(uintptr(0xFFFFFFF5))

	type coord struct {
		x int16
		y int16
	}
	type smallRect struct {
		left   int16
		top    int16
		right  int16
		bottom int16
	}
	type consoleScreenBufferInfo struct {
		size              coord
		cursorPosition    coord
		attributes        uint16
		window            smallRect
		maximumWindowSize coord
	}

	var info consoleScreenBufferInfo
	procGetConsoleScreenBufferInfo.Call(handle, uintptr(unsafe.Pointer(&info)))

	size := uint32(info.size.x) * uint32(info.size.y)
	var written uint32
	origin := coord{0, 0}

	procFillConsoleOutputCharacter.Call(
		handle, uintptr(' '), uintptr(size),
		*(*uintptr)(unsafe.Pointer(&origin)),
		uintptr(unsafe.Pointer(&written)),
	)
	procFillConsoleOutputAttribute.Call(
		handle, uintptr(info.attributes), uintptr(size),
		*(*uintptr)(unsafe.Pointer(&origin)),
		uintptr(unsafe.Pointer(&written)),
	)
	procSetConsoleCursorPosition.Call(handle, *(*uintptr)(unsafe.Pointer(&origin)))
	_ = os.Stdout // keep import
}

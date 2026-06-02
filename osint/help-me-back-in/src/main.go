package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"

	"can-you-help-me-get-back-in/internal/game"
)

func main() {
	if !isTerminal() {
		fmt.Println("This program must be run in an interactive terminal.")
		os.Exit(1)
	}

	reader := bufio.NewReader(os.Stdin)

	for {
		clearScreen()
		printBanner()
		g := game.New()
		runGame(g, reader)

		fmt.Println("\n--- Call ended ---")
		fmt.Print("\nWould you like to make another call? (y/n): ")
		input, _ := reader.ReadString('\n')
		input = strings.TrimSpace(strings.ToLower(input))
		if input != "y" && input != "yes" {
			fmt.Println("Goodbye.")
			break
		}
	}
}

func runGame(g *game.Game, reader *bufio.Reader) {
	for {
		clearScreen()
		node := g.CurrentNode()
		if node == nil {
			break
		}

		fmt.Println(strings.Repeat("─", 60))
		fmt.Println()
		fmt.Printf("  Sarah: %s\n", node.Dialogue)
		fmt.Println()
		fmt.Println(strings.Repeat("─", 60))

		if len(node.Choices) == 0 {
			fmt.Println("\n[The call has ended]")
			fmt.Print("\nPress Enter to continue...")
			reader.ReadString('\n')
			break
		}

		fmt.Println("\nWhat do you say?")
		fmt.Println()
		for i, choice := range node.Choices {
			fmt.Printf("  %d) %s\n", i+1, choice.Text)
		}
		fmt.Println()
		fmt.Print("Your choice: ")

		input, _ := reader.ReadString('\n')
		input = strings.TrimSpace(input)
		choice, err := strconv.Atoi(input)
		if err != nil || choice < 1 || choice > len(node.Choices) {
			continue
		}

		g.MakeChoice(choice - 1)
	}
}

func printBanner() {
	fmt.Println(strings.Repeat("═", 60))
	fmt.Println("        CUSTOMER SUPPORT LINE - INCOMING CALL")
	fmt.Println(strings.Repeat("═", 60))
	fmt.Println()
	fmt.Println("  Caller: Sarah Mitchell")
	fmt.Println("  Issue:  Account locked - requesting password reset")
	fmt.Println("  Note:   Bill payment pending")
	fmt.Println()
	fmt.Println(strings.Repeat("═", 60))
	fmt.Println()
	fmt.Println("  [Connecting call...]")
	fmt.Println()
}

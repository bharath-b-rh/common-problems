package main

import (
	"fmt"
	"os"
)

func main() {

	var input int

	fmt.Println("What would you like to find?")
	fmt.Println("\t1. Reverse of a given number")
	fmt.Println("\t2. Fibonacci series up to the given term")
	fmt.Println("\t3. Given string is a palindrome")

	fmt.Print("\n")
	if _, err := fmt.Scanf("%d", &input); err != nil {
		panic("failed to read input: " + err.Error())
	}
	fmt.Print("\n")

	switch input {
	case 1:
		revNum()
	case 2:
		fibonacci()
	case 3:
		palindrome()
	default:
		panic("invalid input")
	}

	fmt.Println("\nGoodbye!")
	os.Exit(0)
}

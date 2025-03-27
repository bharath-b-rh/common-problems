package main

import (
	"fmt"
)

func palindrome() {
	var (
		input string
	)

	fmt.Println("Enter a string")
	if _, err := fmt.Scanf("%s", &input); err != nil {
		panic(err)
	}
	reverse := []rune(input)
	for i, j := 0, len(reverse)-1; i < j; i, j = i+1, j-1 {
		reverse[i], reverse[j] = reverse[j], reverse[i]
	}

	fmt.Printf("The reverse of %s is %s", input, string(reverse))
	if input == string(reverse) {
		fmt.Print(", and is a palindrome\n")
	} else {
		fmt.Print(", and is not a palindrome\n")
	}
}

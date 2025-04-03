package main

import (
	"fmt"
)

func revNum() {
	var (
		input, number, reverse int
	)

	fmt.Println("Enter a number to find the reverse of it")
	if _, err := fmt.Scanf("%d", &input); err != nil {
		panic(err)
	}

	number = input
	for number > 0 {
		reverse = reverse*10 + (number % 10)
		number /= 10
	}

	fmt.Println("The reverse of", input, "is", reverse)
}

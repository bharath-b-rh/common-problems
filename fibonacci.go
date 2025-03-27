package main

import (
	"fmt"
)

func fibonacci() {
	var (
		input int
		a     int = 0
		b     int = 1
	)

	fmt.Println("Enter the required number of fibonacci sequence")
	if _, err := fmt.Scanf("%d", &input); err != nil {
		panic(err)
	}

	fmt.Printf("%d, %d", a, b)
	for i := 2; i < input; i++ {
		fmt.Printf(", %d", a+b)
		a, b = b, a+b
	}
	fmt.Print("\n")
}

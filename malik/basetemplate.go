package main

import (
	"bufio"
	"fmt"
	"os"
)

func main() {
	fileName := os.Args[1]
	version := os.Args[2]

	fmt.Println("File Name: ", fileName, version)

	file, err := os.Open(fileName)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close() // defer closing the file

	scanner := bufio.NewScanner(file)
	games := GamesFromScanner(scanner)

	// fmt.Println(games)
	fmt.Println("Answer Problem 1:", problem1(games))
	fmt.Println("Answer Problem 2:", problem2(games))
}

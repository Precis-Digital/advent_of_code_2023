/*
go build main.go
./main input.txt v1
*/

package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
)

type NumberLocationMap map[[2]int]int
type SymbolLocationMap map[[2]int]string

func problem1(numberLocation NumberLocationMap, symbolLocation SymbolLocationMap) int {

	partNumberSum := 0

	for location, number := range numberLocation {
		numberLength := len(strconv.Itoa(number))

		isAdjacentToSymbol := false
		// traverse the length of the number
		for i := 0; i < numberLength; i++ {
			x := location[0]
			y := location[1] + i

			// check in all directions for a symbol
			for i := -1; i <= 1; i++ {
				for j := -1; j <= 1; j++ {
					if _, ok := symbolLocation[[2]int{x + i, y + j}]; ok {
						isAdjacentToSymbol = true
					}
				}
			}
		}
		if isAdjacentToSymbol {
			partNumberSum += number
		}

	}
	return partNumberSum
}

func problem2(numberLocation NumberLocationMap, symbolLocation SymbolLocationMap) int {
	// pretty much the same solutoin, but just need to keep track of if the symbol is a *...
	// then need to store the symbol location, number location and value in a map of maps, to handle duplicates of numbers

	gears := make(map[[2]int]map[[2]int]int)

	gearRatioSum := 0

	for numberPostion, number := range numberLocation {
		numberLength := len(strconv.Itoa(number))

		// traverse the length of the number
		for i := 0; i < numberLength; i++ {
			x := numberPostion[0]
			y := numberPostion[1] + i

			// check in all directions for a symbol
			for i := -1; i <= 1; i++ {
				for j := -1; j <= 1; j++ {
					symbolPosition := [2]int{x + i, y + j}
					if symbolLocation[symbolPosition] == "*" {
						// if the symbol doesnt already exist, create the inner map
						if _, ok := gears[symbolPosition]; !ok {
							gears[symbolPosition] = make(map[[2]int]int)
						}
						gears[symbolPosition][numberPostion] = number
					}
				}
			}
		}
	}

	for _, adjacentNumberMap := range gears {
		// if there are only 2 adjacentNumbers in the map. Then take the product of the two numbers
		if len(adjacentNumberMap) == 2 {
			ratio := 1
			for _, ratios := range adjacentNumberMap {
				ratio *= ratios
			}
			gearRatioSum += ratio
		}
	}
	return gearRatioSum
}

func extractNumbersAndSymbols(s *bufio.Scanner) (NumberLocationMap, SymbolLocationMap) {

	numberRegex, _ := regexp.Compile("([0-9]+)")
	// find any symbol not a number or the "."
	symbolRegex, _ := regexp.Compile("[^0-9.]")

	// location, key is array of 2 ints and the value is an integer
	numberLocation := make(NumberLocationMap)
	symbolLocation := make(SymbolLocationMap)

	row := 0
	for s.Scan() {
		line := s.Text()
		numbersFound := numberRegex.FindAllStringIndex(line, -1)
		symbolsFound := symbolRegex.FindAllStringIndex(line, -1)
		for _, number := range numbersFound {
			partNumber, _ := strconv.Atoi(line[number[0]:number[1]])
			numberLocation[[2]int{row, number[0]}] = partNumber
		}
		for _, symbol := range symbolsFound {
			symbolLocation[[2]int{row, symbol[0]}] = line[symbol[0]:symbol[1]]
		}
		row++
	}
	return numberLocation, symbolLocation
}

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
	numberLocation, symbolLocation := extractNumbersAndSymbols(scanner)
	fmt.Println("Answer Problem 1:", problem1(numberLocation, symbolLocation))
	fmt.Println("Answer Problem 2:", problem2(numberLocation, symbolLocation))
}

package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

var numberDict = map[string]int{
	"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
	"six": 6, "seven": 7, "eight": 8, "nine": 9,
}

func findInteger(calibration string, reverse bool) string {
	var calibrationIter []rune
	if reverse {
		calibrationIter = reverseRuneSlice([]rune(calibration))
	} else {
		calibrationIter = []rune(calibration)
	}

	for _, value := range calibrationIter {
		if isDigit(value) {
			return string(value)
		}
	}
	return ""
}

func findIntegerOrSpelledOutNumber(calibration string, reverse bool) string {
	var calibrationIter []rune
	if reverse {
		calibrationIter = reverseRuneSlice([]rune(calibration))
	} else {
		calibrationIter = []rune(calibration)
	}

	for i, value := range calibrationIter {
		if isDigit(value) {
			return string(value)
		} else {
			for spelledOutNumber, number := range numberDict {
				if matchSpelledOutNumber(string(calibrationIter), i, spelledOutNumber, reverse) {
					return strconv.Itoa(number)
				}
			}
		}
	}

	return ""
}

func matchSpelledOutNumber(text string, index int, word string, reverse bool) bool {
	length := len(word)
	if reverse {
		if index-length+1 < 0 {
			return false
		}
		return text[index-length+1:index+1] == reverseString(word)
	}
	if index+length > len(text) {
		return false
	}
	return text[index:index+length] == word
}

func calculateTotal(calibrationValues []string, solutionFunction func(string, bool) string) int {
	total := 0
	for _, calibrationValue := range calibrationValues {
		firstNumber := solutionFunction(calibrationValue, false)
		lastNumber := solutionFunction(calibrationValue, true)
		combinedNumber, err := strconv.Atoi(firstNumber + lastNumber)
		if err != nil {
			fmt.Println("Error converting to int:", err)
			continue
		}
		total += combinedNumber
	}
	return total
}

func reverseRuneSlice(runes []rune) []rune {
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return runes
}

func reverseString(s string) string {
	runes := []rune(s)
	return string(reverseRuneSlice(runes))
}

func isDigit(r rune) bool {
	return r >= '0' && r <= '9'
}

func main() {
	file, err := os.Open("inputs/day01.txt")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	var puzzleInput []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		puzzleInput = append(puzzleInput, scanner.Text())
	}

	solution1 := calculateTotal(puzzleInput, findInteger)
	solution2 := calculateTotal(puzzleInput, findIntegerOrSpelledOutNumber)

	fmt.Printf("Solution 1: %d\n", solution1)
	fmt.Printf("Solution 2: %d\n", solution2)
}

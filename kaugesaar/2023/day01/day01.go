package day01

import (
	_ "embed" // For embedding the input file
	"kaugesaar-aoc/common"
	"kaugesaar-aoc/utils"
	"math"
	"strings"
	"unicode"
)

//go:embed day1.txt
var fileInput string

// Solver for day 1 and its both parts
type Solver struct{}

func p2() string {
	rows := strings.Split(fileInput, "\n")
	var numbers []int

	digitMap := map[string]int{
		"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
		"six": 6, "seven": 7, "eight": 8, "nine": 9,
	}

	findNumber := func(word string, index int) (string, bool) {
		start := int(math.Max(0, float64(index-1)))
		for i := 1; i <= 5 && start+i <= len(word); i++ {
			slicedWord := word[start : start+i]
			if num, exsists := digitMap[slicedWord]; exsists {
				return utils.ToStr(num), true
			}
		}
		return "", false
	}

	for _, row := range rows {
		var first, last string
		foundFirst := false
		currentWord := ""

		for i, r := range row {
			if unicode.IsDigit(r) {
				if !foundFirst {
					first = string(r)
					foundFirst = true
				}
				last = string(r)
			} else if unicode.IsLetter(r) {
				currentWord += string(r)
				if num, exsits := findNumber(row, i); exsits {
					if !foundFirst {
						first = num
						foundFirst = true
					}
					last = num
					currentWord = ""
				}
			}
		}

		number := utils.ToInt(first + last)
		numbers = append(numbers, number)
	}

	return utils.ToStr(utils.SumArr(numbers))
}

func p1() string {
	rows := strings.Split(fileInput, "\n")
	var numbers []int

	for _, row := range rows {
		var first, last string
		foundFirst := false

		for _, r := range row {
			if unicode.IsDigit(r) {
				if !foundFirst {
					first = string(r)
					foundFirst = true
				}
				last = string(r)
			}
		}

		number := utils.ToInt(first + last)
		numbers = append(numbers, number)
	}

	return utils.ToStr(utils.SumArr(numbers))
}

// Part1 the solution for part 1, day 1
func (s Solver) Part1() common.Solution {
	return common.Solution{
		Day:    1,
		Part:   1,
		Answer: p1(),
	}
}

// Part2 the solution for part 2, day 1
func (s Solver) Part2() common.Solution {
	return common.Solution{
		Day:    1,
		Part:   2,
		Answer: p2(),
	}
}

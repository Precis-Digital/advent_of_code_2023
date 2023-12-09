package day01

import (
	"kaugesaar-aoc/solution"
	"kaugesaar-aoc/utils"
	"strings"
	"unicode"
)

// Solver for day 1 and its both parts
type Solver struct{}

func parser(part int) string {
	rows := utils.ReadFile("day1.txt")
	var numbers []int

	findFirst := func(s string) string {
		for i := 0; i < len(s); i++ {
			if unicode.IsDigit(rune(s[i])) {
				return string(s[i])
			}
		}
		return ""
	}

	findLast := func(s string) string {
		for i := len(s) - 1; i >= 0; i-- {
			if unicode.IsDigit(rune(s[i])) {
				return string(s[i])
			}
		}
		return ""
	}

	for _, row := range rows {
		if part == 2 {
			row = replacer(row)
		}

		first := findFirst(row)
		last := findLast(row)

		number := utils.ToInt(first + last)
		numbers = append(numbers, number)
	}

	return utils.ToStr(utils.SumArr(numbers))
}

func replacer(s string) string {
	replaceMap := map[string]string{
		"one":   "o1e",
		"two":   "t2o",
		"three": "t3e",
		"four":  "4",
		"five":  "5e",
		"six":   "6",
		"seven": "7n",
		"eight": "e8t",
		"nine":  "n9e",
	}

	for key, value := range replaceMap {
		s = strings.ReplaceAll(s, key, value)
	}

	return s
}

// Part1 the solution for part 1, day 1
func (s Solver) Part1() solution.Response {
	return solution.Response{
		Day:    1,
		Part:   1,
		Answer: parser(1),
	}
}

// Part2 the solution for part 2, day 1
func (s Solver) Part2() solution.Response {
	return solution.Response{
		Day:    1,
		Part:   2,
		Answer: parser(2),
	}
}

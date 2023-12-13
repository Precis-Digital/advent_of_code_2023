package day13

import (
	"kaugesaar-aoc/solution"
	"kaugesaar-aoc/utils"
)

// Solver for day 13 and its both parts
type Solver struct{}

type Pattern struct {
	cols []string
	rows []string
}

func parser() []Pattern {
	lines := utils.ReadFileByNN("day13.txt")

	var patterns []Pattern

	for _, l := range lines {
		rows, cols := len(l), len(l[0])
		var p Pattern

		for c := 0; c < cols; c++ {
			var col string
			for r := 0; r < rows; r++ {
				col += string(l[r][c])
			}
			p.cols = append(p.cols, col)
		}

		for r := 0; r < rows; r++ {
			var row string
			for c := 0; c < cols; c++ {
				row += string(l[r][c])
			}
			p.rows = append(p.rows, row)
		}

		patterns = append(patterns, p)
	}

	return patterns
}

func findReflection(patterns []string, multiplier int) int {
	for i := 1; i < len(patterns); i++ {
		if patterns[i] != patterns[i-1] {
			continue
		}

		x, y := i, i-1
		isValidReflection := true

		for j := 0; j < utils.MinInt(i, len(patterns)-i)-1; j++ {
			x++
			y--
			if patterns[x] != patterns[y] {
				isValidReflection = false
				break
			}
		}

		if isValidReflection {
			return i * multiplier
		}
	}

	return 0
}

func cleanTheSmudgeAndFindReflection(patterns []string, multiplier int) int {
	for i := 1; i < len(patterns); i++ {
		levenDistance := utils.LevenshteinDistance(patterns[i], patterns[i-1])
		if levenDistance > 1 {
			continue
		}

		foundSmudge := levenDistance == 1
		x, y := i, i-1
		isValidReflection := true

		for j := 0; j < utils.MinInt(i, len(patterns)-i)-1; j++ {
			x++
			y--
			levenDistance = utils.LevenshteinDistance(patterns[x], patterns[y])
			if levenDistance > 1 {
				isValidReflection = false
				break
			}

			if levenDistance == 1 {
				if foundSmudge {
					isValidReflection = false
					break
				} else {
					foundSmudge = true
				}
			}
		}

		if isValidReflection && foundSmudge {
			return i * multiplier
		}
	}

	return 0
}

func p1() string {
	patterns := parser()
	sum := 0
	for _, pattern := range patterns {
		sum += findReflection(pattern.rows, 100)
		sum += findReflection(pattern.cols, 1)
	}
	return utils.ToStr(sum)
}

func p2() string {
	patterns := parser()
	sum := 0
	for _, pattern := range patterns {
		sum += cleanTheSmudgeAndFindReflection(pattern.rows, 100)
		sum += cleanTheSmudgeAndFindReflection(pattern.cols, 1)
	}
	return utils.ToStr(sum)
}

// Part1 the solution for part 1, day 13
func (s Solver) Part1() solution.Response {
	return solution.Response{
		Day:    13,
		Part:   1,
		Answer: p1(),
	}
}

// Part2 the solution for part 2, day 13
func (s Solver) Part2() solution.Response {
	return solution.Response{
		Day:    13,
		Part:   2,
		Answer: p2(),
	}
}

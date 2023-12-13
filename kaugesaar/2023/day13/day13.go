package day13

import (
	"kaugesaar-aoc/solution"
	"kaugesaar-aoc/utils"
	"strings"
)

// Solver for day 13 and its both parts
type Solver struct{}

type Pattern struct {
	cols []string
	rows []string
}

func parser() []Pattern {
	rows := utils.ReadFile("day13.txt")
	var lines [][][]string
	var line [][]string

	for i, row := range rows {
		if len(row) == 0 {
			line = make([][]string, 0)
			continue
		}

		line = append(line, strings.Split(row, ""))

		if len(rows)-1 == i || len(rows[i+1]) == 0 {
			lines = append(lines, line)
		}
	}

	var patterns []Pattern

	for _, l := range lines {
		rows, cols := len(l), len(l[0])

		var p Pattern

		for c := 0; c < cols; c++ {
			var col string
			for r := 0; r < rows; r++ {
				col += l[r][c]
			}
			p.cols = append(p.cols, col)
		}

		for r := 0; r < rows; r++ {
			var row string
			for c := 0; c < cols; c++ {
				row += l[r][c]
			}
			p.rows = append(p.rows, row)
		}

		patterns = append(patterns, p)
	}

	return patterns
}

func findReflection(patterns []string, multiplier int) int {
	for i := 1; i < len(patterns); i++ {
		curr, prev := i, i-1

		if patterns[curr] == patterns[prev] {
			x, y := curr, prev
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
	return utils.ToStr(2)
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

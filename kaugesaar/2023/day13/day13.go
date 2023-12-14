package day13

import (
	"kaugesaar-aoc/solution"
	"kaugesaar-aoc/utils"
)

// Solver for day 13 and its both parts
type Solver struct{}

type Pattern struct {
	cols [][]byte
	rows [][]byte
}

func parser() []Pattern {
	lines := utils.ReadFileByNN("day13.txt")

	patterns := make([]Pattern, len(lines))

	for l, line := range lines {
		rows, cols := len(line), len(line[0])
		var p Pattern
		p.cols = make([][]byte, cols)
		p.rows = make([][]byte, rows)

		for c := 0; c < cols; c++ {
			col := make([]byte, rows)
			for r := 0; r < rows; r++ {
				col[r] = line[r][c]
			}
			p.cols[c] = col
		}

		for r := 0; r < rows; r++ {
			row := make([]byte, cols)
			for c := 0; c < cols; c++ {
				row[c] = line[r][c]
			}
			p.rows[r] = row
		}

		patterns[l] = p
	}

	return patterns
}

func findReflection(pattern [][]byte, smudges, multiplier int) int {
	for i := 0; i < len(pattern)-1; i++ {
		mismatch := 0
		for j := 0; j <= utils.MinInt(i, len(pattern)-i-2); j++ {
			x := i - j
			y := i + 1 + j
			for c := range pattern[0] {
				if pattern[x][c] != pattern[y][c] {
					mismatch++
				}
			}
		}
		if mismatch == smudges {
			return (1 + i) * multiplier
		}
	}
	return 0
}

func p1() string {
	patterns := parser()
	sum := 0
	for _, pattern := range patterns {
		sum += findReflection(pattern.rows, 0, 100)
		sum += findReflection(pattern.cols, 0, 1)
	}
	return utils.ToStr(sum)
}

func p2() string {
	patterns := parser()
	sum := 0
	for _, pattern := range patterns {
		sum += findReflection(pattern.rows, 1, 100)
		sum += findReflection(pattern.cols, 1, 1)
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

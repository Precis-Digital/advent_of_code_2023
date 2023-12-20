package day14

import (
	"crypto/sha256"
	"fmt"
	"kaugesaar-aoc/solution"
	"kaugesaar-aoc/utils"
)

// Solver for day 14 and its both parts
type Solver struct{}

func parser() [][]byte {
	rows := utils.ReadFile("day14.txt")
	grid := make([][]byte, len(rows))
	for i := range rows {
		grid[i] = []byte(rows[i])
	}
	return grid
}

func rollNorth(grid [][]byte) [][]byte {
	for {
		done := true
		for r := 0; r < len(grid)-1; r++ {
			for c := 0; c < len(grid[0]); c++ {
				if grid[r+1][c] == 'O' && grid[r][c] == '.' {
					grid[r][c] = 'O'
					grid[r+1][c] = '.'
					done = false
				}
			}
		}
		if done {
			break
		}
	}
	return grid
}

func rotateGrid(grid [][]byte) [][]byte {
	rotated := make([][]byte, len(grid[0]))
	for c := range rotated {
		rotated[c] = make([]byte, len(grid))
		for r := range grid {
			rotated[c][len(grid)-1-r] = grid[r][c]
		}
	}
	return rotated
}

func hashGrid(grid [][]byte) string {
	h := sha256.New()
	for _, row := range grid {
		h.Write(row)
	}
	return fmt.Sprintf("%s", h.Sum(nil))
}

func p1() string {
	grid := parser()
	grid = rollNorth(grid)

	sum := 0
	for r, row := range grid {
		for _, col := range row {
			if col == 'O' {
				sum += len(grid) - r
			}
		}
	}

	return utils.ToStr(sum)
}

func p2() string {
	grid := parser()

	cache := make(map[string]int)
	for i := 1; i < int(1e9); i++ {
		for j := 0; j < 4; j++ {
			grid = rollNorth(grid)
			grid = rotateGrid(grid)
		}

		key := hashGrid(grid)

		if seenAt, ok := cache[key]; ok {
			if (int(1e9)-i)%(i-seenAt) == 0 {
				break
			}
		} else {
			cache[key] = i
		}
	}

	sum := 0

	for r, row := range grid {
		for _, col := range row {
			if col == 'O' {
				sum += len(grid) - r
			}
		}
	}

	return utils.ToStr(sum)
}

// Part1 the solution for part 1, day 14
func (s Solver) Part1() solution.Response {
	return solution.Response{
		Day:    14,
		Part:   1,
		Answer: p1(),
	}
}

// Part2 the solution for part 2, day 14
func (s Solver) Part2() solution.Response {
	return solution.Response{
		Day:    14,
		Part:   2,
		Answer: p2(),
	}
}

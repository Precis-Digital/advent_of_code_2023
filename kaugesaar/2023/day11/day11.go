package day11

import (
	"kaugesaar-aoc/solution"
	"kaugesaar-aoc/utils"
)

// Solver for day 11 and its both parts
type Solver struct{}

func parser() ([][]rune, [][2]int) {
	rows := utils.ReadFile("day11.txt")

	universe := make([][]rune, len(rows))
	for r, row := range rows {
		universe[r] = make([]rune, len(row))
		for c, char := range row {
			universe[r][c] = char
		}
	}

	var galaxies [][2]int
	for r, row := range universe {
		for c, col := range row {
			if col == '#' {
				galaxies = append(galaxies, [2]int{r, c})
			}
		}
	}

	return universe, galaxies
}

func exapandGalaxies(universe [][]rune, galaxies [][2]int) [][2]int {
	rows, cols := len(universe), len(universe[0])

	var emptyRows, emptyCols []int

	for r := 0; r < rows; r++ {
		hasGalaxy := false
		for _, c := range universe[r] {
			if c == '#' {
				hasGalaxy = true
				break
			}
		}
		if !hasGalaxy {
			emptyRows = append(emptyRows, r)
		}
	}

	for c := 0; c < cols; c++ {
		hasGalaxy := false
		for r := 0; r < rows; r++ {
			if universe[r][c] == '#' {
				hasGalaxy = true
				break
			}
		}
		if !hasGalaxy {
			emptyCols = append(emptyCols, c)
		}
	}

	for i := len(emptyRows) - 1; i >= 0; i-- {
		r := emptyRows[i]
		for j := range galaxies {
			if galaxies[j][0] > r {
				galaxies[j][0]++
			}
		}
	}

	for i := len(emptyCols) - 1; i >= 0; i-- {
		c := emptyCols[i]
		for j := range galaxies {
			if galaxies[j][1] > c {
				galaxies[j][1]++
			}
		}
	}

	return galaxies
}

func p1() string {
	universe, galaxies := parser()
	galaxies = exapandGalaxies(universe, galaxies)
	sum := 0
	for i := 0; i < len(galaxies); i++ {
		for j := i + 1; j < len(galaxies); j++ {
			sum += utils.Abs(galaxies[i][0]-galaxies[j][0]) + utils.Abs((galaxies[i][1] - galaxies[j][1]))
		}
	}
	return utils.ToStr(sum)
}

func p2() string {
	return utils.ToStr(2)
}

// Part1 the solution for part 1, day 11
func (s Solver) Part1() solution.Response {
	return solution.Response{
		Day:    11,
		Part:   1,
		Answer: p1(),
	}
}

// Part2 the solution for part 2, day 11
func (s Solver) Part2() solution.Response {
	return solution.Response{
		Day:    11,
		Part:   2,
		Answer: p2(),
	}
}

package day09

import (
	_ "embed" // For embedding the input file
	"kaugesaar-aoc/solution"
	"kaugesaar-aoc/utils"
	"regexp"
	"strings"
)

// Solver for day 9 and its both parts
type Solver struct{}

//go:embed day9.txt
var fileInput string

func parser() [][]int {
	rows := strings.Split(fileInput, "\n")
	histories := make([][]int, len(rows))
	digitRe := regexp.MustCompile(`-\d+|\d+`)

	for i, row := range rows {
		nums := digitRe.FindAllString(row, -1)
		histories[i] = make([]int, len(nums))
		for j, num := range nums {
			histories[i][j] = utils.ToInt(num)
		}
	}

	return histories
}

func calcluateDistance(histories [][]int, isPartTwo bool) int {
	sum := 0

	for _, history := range histories {
		var distances [][]int

		if isPartTwo {
			history = utils.ReverseIntArray(history)
		}

		for len(history) > 1 {
			distances = append(distances, history)

			nextRow := make([]int, len(history)-1)
			for i := 0; i < len(nextRow); i++ {
				nextRow[i] = history[i+1] - history[i]
			}

			history = nextRow
		}

		distances = append(distances, history)

		for i := len(distances) - 2; i >= 0; i-- {
			distances[i] = append(distances[i], distances[i+1][len(distances[i+1])-1]+distances[i][len(distances[i])-1])
		}

		sum += distances[0][len(distances[0])-1]
	}

	return sum
}

func p1() string {
	histories := parser()

	sum := calcluateDistance(histories, false)

	return utils.ToStr(sum)
}

func p2() string {
	histories := parser()

	sum := calcluateDistance(histories, true)

	return utils.ToStr(sum)
}

// Part1 the solution for part 1, day 9
func (s Solver) Part1() solution.Response {
	return solution.Response{
		Day:    9,
		Part:   1,
		Answer: p1(),
	}
}

// Part2 the solution for part 2, day 9
func (s Solver) Part2() solution.Response {
	return solution.Response{
		Day:    9,
		Part:   2,
		Answer: p2(),
	}
}

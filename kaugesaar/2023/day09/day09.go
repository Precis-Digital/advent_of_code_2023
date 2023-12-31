package day09

import (
	"kaugesaar-aoc/solution"
	"kaugesaar-aoc/utils"
	"regexp"
)

// Solver for day 9 and its both parts
type Solver struct{}

func parser() [][]int {
	rows := utils.ReadFile("day9.txt")
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

func nextValue(history []int) int {
	if utils.SumArr(history) == 0 {
		return 0
	}

	differences := make([]int, len(history)-1)

	for i := 1; i < len(history); i++ {
		difference := history[i] - history[i-1]
		differences[i-1] = difference
	}

	return history[len(history)-1] + nextValue(differences)
}

func calculateDistance(histories [][]int, isPartTwo bool) int {
	sum := 0

	for _, history := range histories {
		if isPartTwo {
			history = utils.ReverseIntArray(history)
		}
		sum += nextValue(history)
	}

	return sum
}

func p1() string {
	histories := parser()

	sum := calculateDistance(histories, false)

	return utils.ToStr(sum)
}

func p2() string {
	histories := parser()

	sum := calculateDistance(histories, true)

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

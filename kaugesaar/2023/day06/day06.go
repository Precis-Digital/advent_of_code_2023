package day06

import (
	"kaugesaar-aoc/solution"
	"kaugesaar-aoc/utils"
)

type Race struct {
	Time     int
	Distance int
}

var races = []Race{
	{62, 553},
	{64, 1010},
	{91, 1473},
	{90, 1074},
}

var races2 = []Race{
	{62649190, 553101014731074},
}

// Solver for day 6 and its both parts
type Solver struct{}

func countWaysToWin(race Race) int {
	ways := 0
	for i := 0; i < race.Time; i++ {
		distance := i * (race.Time - i)
		if distance > race.Distance {
			ways++
		}
	}
	return ways
}

func p1() string {
	totalWays := 1

	for _, race := range races {
		waysToWin := countWaysToWin(race)
		totalWays *= waysToWin
	}

	return utils.ToStr(totalWays)
}

func p2() string {
	totalWays := 1

	for _, race := range races2 {
		waysToWin := countWaysToWin(race)
		totalWays *= waysToWin
	}

	return utils.ToStr(totalWays)
}

// Part1 the solution for part 1, day 6
func (s Solver) Part1() solution.Response {
	return solution.Response{
		Day:    5,
		Part:   1,
		Answer: p1(),
	}
}

// Part2 the solution for part 2, day 6
func (s Solver) Part2() solution.Response {
	return solution.Response{
		Day:    5,
		Part:   2,
		Answer: p2(),
	}
}

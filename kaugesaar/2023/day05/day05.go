package day05

import (
	"kaugesaar-aoc/solution"
	"kaugesaar-aoc/utils"
	"strings"
	"unicode"
)

// Solver for day 5 and its both parts
type Solver struct{}

type Seed struct {
	Start int
	End   int
}

type Level struct {
	Source      int
	Destination int
	Length      int
}

type Almanac struct {
	Seeds     []int
	Levels    [][]Level
	SeedPairs []Seed
}

func parser() Almanac {
	var a Almanac

	rows := utils.ReadFile("day5.txt")

	seeds := strings.Fields(rows[0])[1:]

	for _, seed := range seeds {
		a.Seeds = append(a.Seeds, utils.ToInt(seed))
	}

	for i := 0; i < len(a.Seeds); i += 2 {
		a.SeedPairs = append(a.SeedPairs, Seed{
			Start: a.Seeds[i],
			End:   a.Seeds[i] + a.Seeds[i+1],
		})
	}

	var levels []Level

	isNewMap := true

	for i, row := range rows[3:] {

		if len(row) == 0 {
			continue
		}

		if isNewMap {
			levels = make([]Level, 0)
			isNewMap = false
		}

		if unicode.IsLetter(rune(row[0])) || i == len(rows)-4 {
			a.Levels = append(a.Levels, levels)
			isNewMap = true
		}

		if unicode.IsDigit(rune(row[0])) {
			nums := strings.Fields(row)
			if len(nums) > 2 {
				levels = append(levels, Level{
					Source:      utils.ToInt(nums[1]),
					Destination: utils.ToInt(nums[0]),
					Length:      utils.ToInt(nums[2]),
				})
			}
		}
	}

	return a
}

func p1() string {
	a := parser()

	seeds := make([]int, len(a.Seeds))

	for i, seed := range a.Seeds {
		for _, level := range a.Levels {
			for _, l := range level {
				if seed >= l.Source && seed < l.Source+l.Length {
					offset := seed - l.Source
					seed = l.Destination + offset
					break
				}
			}
			seeds[i] = seed
		}
	}

	min := utils.MinArr(seeds)

	return utils.ToStr(min)
}

func p2() string {
	a := parser()

	pairs := a.SeedPairs

	for _, level := range a.Levels {
		var newPairs []Seed

		for _, sp := range pairs {
			var mapped []Seed
			unmapped := []Seed{{sp.Start, sp.End}}

			for _, l := range level {
				var m []Seed

				for _, um := range unmapped {
					low := Seed{um.Start, utils.MinInt(um.End, l.Source)}
					mid := Seed{utils.MaxInt(um.Start, l.Source), utils.MinInt(um.End, l.Source+l.Length)}
					high := Seed{utils.MaxInt(um.Start, l.Source+l.Length), um.End}

					if low.Start < low.End {
						m = append(m, low)
					}

					if mid.Start < mid.End {
						mapped = append(mapped, Seed{
							Start: mid.Start - l.Source + l.Destination,
							End:   mid.End - l.Source + l.Destination,
						})
					}

					if high.Start < high.End {
						m = append(m, high)
					}
				}

				unmapped = m
			}

			newPairs = append(newPairs, mapped...)
			newPairs = append(newPairs, unmapped...)
		}

		pairs = newPairs
	}

	min := pairs[0].Start
	for _, pair := range pairs {
		if pair.Start < min {
			min = pair.Start
		}
	}

	return utils.ToStr(min)
}

// Part1 the solution for part 1, day 5
func (s Solver) Part1() solution.Response {
	return solution.Response{
		Day:    5,
		Part:   1,
		Answer: p1(),
	}
}

// Part2 the solution for part 2, day 5
func (s Solver) Part2() solution.Response {
	return solution.Response{
		Day:    5,
		Part:   2,
		Answer: p2(),
	}
}

package day03

import (
	"kaugesaar-aoc/solution"
	"kaugesaar-aoc/utils"
	"regexp"
	"unicode"
)

// Solver for day 3 and its both parts
type Solver struct{}

type Point struct {
	X int
	Y int
}

func parser() map[Point][]int {
	directions := []Point{{-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1}}
	rows := utils.ReadFile("day3.txt")
	digitRe := regexp.MustCompile(`\d+`)

	symbolMap := map[Point]rune{}
	for y, str := range rows {
		for x, r := range str {
			if r != '.' && !unicode.IsDigit(r) {
				symbolMap[Point{X: x, Y: y}] = r
			}
		}
	}

	partsMap := map[Point][]int{}
	for y, str := range rows {
		for _, match := range digitRe.FindAllStringIndex(str, -1) {
			bounds := map[Point]struct{}{}
			num := utils.ToInt(str[match[0]:match[1]])

			for x := match[0]; x < match[1]; x++ {
				for _, dir := range directions {
					bounds[Point{X: x + dir.X, Y: y + dir.Y}] = struct{}{}
				}
			}

			for part := range bounds {
				if _, ok := symbolMap[part]; ok {
					partsMap[part] = append(partsMap[part], num)
				}
			}
		}
	}

	return partsMap
}

func p1() string {
	parts := parser()
	sum := 0

	for _, partNums := range parts {
		for _, nums := range partNums {
			sum += nums
		}
	}

	return utils.ToStr(sum)
}

func p2() string {
	parts := parser()
	sum := 0

	for _, partNums := range parts {
		if len(partNums) == 2 {
			sum += partNums[0] * partNums[1]
		}
	}

	return utils.ToStr(sum)
}

// Part1 the solution for part 1, day 3
func (s Solver) Part1() solution.Response {
	return solution.Response{
		Day:    3,
		Part:   1,
		Answer: p1(),
	}
}

// Part2 the solution for part 2, day 3
func (s Solver) Part2() solution.Response {
	return solution.Response{
		Day:    3,
		Part:   2,
		Answer: p2(),
	}
}

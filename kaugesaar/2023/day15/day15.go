package day15

import (
	"kaugesaar-aoc/solution"
	"kaugesaar-aoc/utils"
	"strings"
)

// Solver for day 15 and its both parts
type Solver struct{}

type Lens struct {
	Label       string
	FocalLength int
}

func parser() []string {
	rows := utils.ReadFile("day15.txt")
	rows = strings.Split(rows[0], ",")
	return rows
}

func hashValue(str string) int {
	currentValue := 0
	for _, s := range str {
		currentValue = (currentValue + int(s)) * 17
		currentValue = currentValue % 256
	}
	return currentValue
}

func parseStep(step string) (label string, op rune, focalLength int) {
	if strings.Contains(step, "=") {
		parts := strings.Split(step, "=")
		label, focalLength = parts[0], utils.ToInt(parts[1])
		op = '='
	} else if strings.Contains(step, "-") {
		parts := strings.Split(step, "-")
		label = parts[0]
		op = '-'

	}

	return label, op, focalLength
}

func p1() string {
	steps := parser()

	sum := 0
	for _, step := range steps {
		sum += hashValue(step)
	}

	return utils.ToStr(sum)
}

func p2() string {
	steps := parser()
	boxes := make(map[int][]Lens, 256)

	for _, step := range steps {
		label, op, focalLength := parseStep(step)
		box := hashValue(label)

		switch op {
		case '=':
			found := false
			for i, lens := range boxes[box] {
				if lens.Label == label {
					boxes[box][i] = Lens{Label: label, FocalLength: focalLength}
					found = true
					break
				}
			}
			if !found {
				boxes[box] = append(boxes[box], Lens{Label: label, FocalLength: focalLength})
			}
		case '-':
			for i, lens := range boxes[box] {
				if lens.Label == label {
					boxes[box] = append(boxes[box][:i], boxes[box][i+1:]...)
					break
				}
			}
		}
	}

	sum := 0
	for box, lenses := range boxes {
		for i, lens := range lenses {
			sum += (box + 1) * (i + 1) * lens.FocalLength
		}
	}

	return utils.ToStr(sum)
}

// Part1 the solution for part 1, day 15
func (s Solver) Part1() solution.Response {
	return solution.Response{
		Day:    15,
		Part:   1,
		Answer: p1(),
	}
}

// Part2 the solution for part 2, day 15
func (s Solver) Part2() solution.Response {
	return solution.Response{
		Day:    15,
		Part:   2,
		Answer: p2(),
	}
}

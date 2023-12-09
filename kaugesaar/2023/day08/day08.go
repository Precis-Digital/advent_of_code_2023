package day08

import (
	_ "embed" // For embedding the input file
	"kaugesaar-aoc/solution"
	"kaugesaar-aoc/utils"
	"regexp"
	"strings"
)

// Solver for day 8 and its both parts
type Solver struct{}

//go:embed day8.txt
var fileInput string

type Network map[string][2]string

func parser() ([]int, Network) {
	rows := strings.Split(fileInput, "\n")
	nodeRe := regexp.MustCompile(`[A-Z]{3,3}`)

	var directions []int

	for _, dir := range rows[0] {
		if dir == 'R' {
			directions = append(directions, 1)
		}
		if dir == 'L' {
			directions = append(directions, 0)
		}
	}

	rows = rows[2:]
	nodes := make(Network, len(rows))

	for _, row := range rows {
		parts := strings.SplitN(row, " = ", 2)
		n := nodeRe.FindAllString(parts[1], -1)
		nodes[parts[0]] = [2]string{n[0], n[1]}
	}

	return directions, nodes
}

func findTotalSteps(network Network, directions []int, startNode, endNode string) int {
	currentNode := startNode
	steps := 0
	for {
		for _, dir := range directions {
			currentNode = network[currentNode][dir]
			steps++
			if strings.HasSuffix(currentNode, endNode) {
				return steps
			}
		}
	}

}

func p1() string {
	directions, network := parser()

	steps := findTotalSteps(network, directions, "AAA", "ZZZ")

	return utils.ToStr(steps)
}

func p2() string {
	directions, network := parser()

	var positions []string
	for position := range network {
		if strings.HasSuffix(position, "A") {
			positions = append(positions, position)
		}
	}

	var steps []int
	for _, position := range positions {
		steps = append(steps, findTotalSteps(network, directions, position, "Z"))
	}

	sum := utils.LCM(steps[0], steps[1], steps[2:]...)

	return utils.ToStr(sum)
}

// Part1 the solution for part 1, day 8
func (s Solver) Part1() solution.Response {
	return solution.Response{
		Day:    8,
		Part:   1,
		Answer: p1(),
	}
}

// Part2 the solution for part 2, day 8
func (s Solver) Part2() solution.Response {
	return solution.Response{
		Day:    8,
		Part:   2,
		Answer: p2(),
	}
}

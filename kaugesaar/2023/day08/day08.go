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

type Cycle struct {
	offset int
	length int
	steps  int
}

func parser() (instructions []int, nodes map[string][]string) {
	rows := strings.Split(fileInput, "\n")
	nodeRe := regexp.MustCompile(`[A-Z]{3,3}`)

	for _, instruction := range strings.Split(rows[0], "") {
		if instruction == "R" {
			instructions = append(instructions, 2)
		} else {
			instructions = append(instructions, 1)
		}
	}

	rows = rows[2:]
	nodes = make(map[string][]string, len(rows))

	for _, row := range rows {
		parts := strings.SplitN(row, " = ", 2)
		n := nodeRe.FindAllString(parts[1], -1)
		nodes[parts[0]] = []string{parts[0], n[0], n[1]}
	}

	return instructions, nodes
}

func findCycle(nodes map[string][]string, instructions []int, currentNode string) (offset, cycle int) {
	found := false
	for {
		for _, instruction := range instructions {
			currentNode = nodes[currentNode][instruction]

			if found && currentNode[2] == 'Z' {
				return offset, cycle
			}

			if currentNode[2] == 'Z' {
				found = true
			}

			if found {
				cycle++
			} else {
				offset++
			}
		}
	}
}

func p1() string {
	instructions, nodes := parser()

	steps := 0
	found := false

	currentNode := "AAA"

	for !found {
		for _, instruction := range instructions {
			currentNode = nodes[currentNode][instruction]
			steps++
			if currentNode == "ZZZ" {
				found = true
				break
			}
		}
	}

	return utils.ToStr(steps)
}

func p2() string {
	instructions, nodes := parser()

	currentNodes := []string{}

	for key := range nodes {
		if key[2] == 'A' {
			currentNodes = append(currentNodes, key)
		}
	}

	cycles := make([]Cycle, 0)

	for _, currentNode := range currentNodes {
		offset, length := findCycle(nodes, instructions, currentNode)
		cycles = append(cycles, Cycle{offset, length, offset})
	}

	for {
		steps := 0
		for i := range cycles {
			if cycles[i].steps > steps {
				steps = cycles[i].steps
			}
		}

		for i := range cycles {
			for cycles[i].steps < steps {
				cycles[i].steps += cycles[i].length
			}
		}

		allEqual := true
		for i := range cycles[1:] {
			if cycles[i].steps != cycles[i+1].steps {
				allEqual = false
				break
			}
		}

		if allEqual {
			break
		} else {
			for i := range cycles {
				cycles[i].steps += cycles[i].length
			}
		}
	}

	return utils.ToStr(cycles[0].steps + 1)
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

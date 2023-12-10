package day10

import (
	"kaugesaar-aoc/solution"
	"kaugesaar-aoc/utils"
)

/**
	"╔": "╔",
	"╗": "╗",
	"╚": "╚",
	"╝": "╝",
	"═": "═",
	"║": "║",
**/

// Solver for day 10 and its both parts
type Solver struct{}

type Pipe struct {
	North bool
	East  bool
	South bool
	West  bool
}

type Pos struct {
	X int
	Y int
}

var tilesMap = map[rune]Pipe{
	'|': {true, false, true, false},
	'-': {false, true, false, true},
	'L': {true, true, false, false},
	'J': {true, false, false, true},
	'7': {false, false, true, true},
	'F': {false, true, true, false},
	'.': {false, false, false, false},
	'S': {true, true, true, true},
}

func parser() (Pos, map[Pos]Pipe) {
	rows := utils.ReadFile("day10.txt")

	pipes := map[Pos]Pipe{}

	startPos := Pos{0, 0}

	for y, row := range rows {
		for x, char := range row {
			pipes[Pos{x, y}] = tilesMap[char]
			if char == 'S' {
				startPos = Pos{x, y}
			}
		}
	}

	return startPos, pipes
}

func findFurthestPosition(startPos Pos, pipes map[Pos]Pipe) int {
	visited := make(map[Pos]bool)
	queue := []Pos{startPos}
	distances := make(map[Pos]int)
	distances[startPos] = 0
	maxDistance := 0

	for len(queue) > 0 {
		currentPos := queue[0]
		queue = queue[1:]

		if distances[currentPos] > maxDistance {
			maxDistance = distances[currentPos]
		}

		for _, direction := range []struct{ dx, dy int }{{1, 0}, {-1, 0}, {0, 1}, {0, -1}} {
			neighbor := Pos{currentPos.X + direction.dx, currentPos.Y + direction.dy}
			if canMove(currentPos, neighbor, pipes) && !visited[neighbor] {
				queue = append(queue, neighbor)
				visited[neighbor] = true
				distances[neighbor] = distances[currentPos] + 1
			}
		}
	}

	return maxDistance
}

func canMove(from, to Pos, pipes map[Pos]Pipe) bool {
	dx := to.X - from.X
	dy := to.Y - from.Y

	fromPipe := pipes[from]
	toPipe := pipes[to]

	if dy == -1 {
		return fromPipe.North && toPipe.South
	}

	if dy == 1 {
		return fromPipe.South && toPipe.North
	}

	if dx == 1 {
		return fromPipe.East && toPipe.West
	}

	if dx == -1 {
		return fromPipe.West && toPipe.East
	}

	return false
}

func p1() string {
	startPos, pipes := parser()
	distance := findFurthestPosition(startPos, pipes)
	return utils.ToStr(distance)
}

func p2() string {
	return utils.ToStr(2)
}

// Part1 the solution for part 1, day 10
func (s Solver) Part1() solution.Response {
	return solution.Response{
		Day:    10,
		Part:   1,
		Answer: p1(),
	}
}

// Part2 the solution for part 2, day 10
func (s Solver) Part2() solution.Response {
	return solution.Response{
		Day:    10,
		Part:   2,
		Answer: p2(),
	}
}

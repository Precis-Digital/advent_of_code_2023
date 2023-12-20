package day10

import (
	"kaugesaar-aoc/solution"
	"kaugesaar-aoc/utils"
	"strings"
)

// Solver for day 10 and its both parts
type Solver struct{}

const (
	Up int = iota
	Right
	Down
	Left
)

func parser() ([][][4]bool, [2]int) {
	rows := utils.ReadFile("day10.txt")
	var start [2]int
	graph := make([][][4]bool, len(rows))
	for r, row := range rows {
		graph[r] = make([][4]bool, len(row))
		for c, tile := range strings.Split(row, "") {
			if tile == "S" {
				start[0], start[1] = r, c
			}
			graph[r][c] = getConnection(tile)
		}
	}
	return graph, start
}

func getConnection(tile string) [4]bool {
	switch tile {
	case "|":
		return [4]bool{true, false, true, false}
	case "-":
		return [4]bool{false, true, false, true}
	case "L":
		return [4]bool{true, true, false, false}
	case "J":
		return [4]bool{true, false, false, true}
	case "7":
		return [4]bool{false, false, true, true}
	case "F":
		return [4]bool{false, true, true, false}
	default:
		return [4]bool{false, false, false, false}
	}
}

func findLoop(graph [][][4]bool, start [2]int) (map[[2]int]bool, bool) {
	row, col := start[0], start[1]
	var dir int
	for idx, val := range graph[row][col] {
		if val {
			dir = idx
			break
		}
	}
	visited := make(map[[2]int]bool)
	for {
		if _, exsists := visited[[2]int{row, col}]; exsists {
			return visited, true
		}
		visited[[2]int{row, col}] = true
		cameFrom := 0
		switch dir {
		case Up:
			row--
			cameFrom = Down
		case Right:
			col++
			cameFrom = Left
		case Down:
			row++
			cameFrom = Up
		case Left:
			col--
			cameFrom = Right
		default:
			panic("Invalid direction")
		}
		if !graph[row][col][cameFrom] {
			return nil, false
		}
		for i := 0; i < 4; i++ {
			if i != cameFrom && graph[row][col][i] {
				dir = i
				break
			}
		}
	}
}

func findFullLoop(graph [][][4]bool, start [2]int) map[[2]int]bool {
	fullLoop := make(map[[2]int]bool)
	for _, startTile := range []string{"J", "|", "-", "L", "7", "F"} {
		graph[start[0]][start[1]] = getConnection(startTile)
		if loop, found := findLoop(graph, start); found {
			fullLoop = loop
			break
		}
	}
	return fullLoop
}

func p1() string {
	graph, start := parser()
	loop := findFullLoop(graph, start)
	return utils.ToStr(len(loop) / 2)
}

func p2() string {
	graph, start := parser()
	loop := findFullLoop(graph, start)
	sum := 0
	for r := range graph {
		inside := false
		for c := range graph[r] {
			if !loop[[2]int{r, c}] {
				if inside {
					sum++
				}
			} else if graph[r][c][0] {
				inside = !inside
			}
		}
	}
	return utils.ToStr(sum)
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

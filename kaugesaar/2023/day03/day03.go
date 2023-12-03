package day03

import (
	_ "embed" // For embedding the input file
	"kaugesaar-aoc/solution"
	"kaugesaar-aoc/utils"
	"regexp"
	"strings"
	"unicode"
)

//go:embed day3.txt
var fileInput string

// Solver for day 3 and its both parts
type Solver struct{}

// Cell is a cell in the schematic
type Cell struct {
	value            string
	isSymbol         bool
	isNumber         bool
	isVisited        bool
	isGear           bool
	nAdjacentNumbers int
	adjacentNumbers  []int
}

var (
	symbolRegex     = regexp.MustCompile(`[^\.0-9]`)
	digitRegex      = regexp.MustCompile(`(\d+|[^\d])`)
	numberCells     = make(map[string]*Cell)
	parsedschematic = parser()
)

func isGear(s string) bool {
	return s == "*"
}

func makeCellFromString(s string, row, start, end int) *Cell {
	cord := utils.ToStr(row) + utils.ToStr(start) + utils.ToStr(end)
	if unicode.IsDigit(rune(s[0])) {

		if cell, exists := numberCells[cord]; exists {
			return cell
		}

		cell := &Cell{
			value:     s,
			isSymbol:  false,
			isNumber:  true,
			isVisited: false,
			isGear:    false,
		}
		numberCells[cord] = cell
		return cell
	}

	return &Cell{
		value:     s,
		isSymbol:  isSymbol(s),
		isGear:    isGear(s),
		isNumber:  false,
		isVisited: false,
	}
}

func isSymbol(s string) bool {
	return symbolRegex.MatchString(s)
}

func parser() [][]*Cell {
	var schematic [][]*Cell
	rows := strings.Split(fileInput, "\n")

	for x, row := range rows {
		var cells []*Cell
		matches := digitRegex.FindAllStringIndex(row, -1)
		for _, match := range matches {
			start, end := match[0], match[1]
			for i := start; i < end; i++ {
				cells = append(cells, makeCellFromString(string(row[start:end]), x, start, end))
			}
		}
		schematic = append(schematic, cells)
	}

	parseschematic(schematic)

	return schematic
}

func p1() string {
	sum := 0
	for _, row := range parsedschematic {
		for _, cell := range row {
			if cell.isSymbol {
				sum += utils.SumArr(cell.adjacentNumbers)
			}
		}
	}

	return utils.ToStr(sum)
}

func p2() string {
	sum := 0
	for _, row := range parsedschematic {
		for _, cell := range row {
			if cell.isGear && cell.nAdjacentNumbers == 2 {
				sum += cell.adjacentNumbers[0] * cell.adjacentNumbers[1]
			}
		}
	}

	return utils.ToStr(sum)
}

func parseAdjacentNumbers(source *Cell, schematic [][]*Cell, x, y int) {
	for dx := -1; dx <= 1; dx++ {
		for dy := -1; dy <= 1; dy++ {
			nx, ny := x+dx, y+dy
			if nx >= 0 && nx < len(schematic) && ny >= 0 && ny < len(schematic[nx]) {
				cell := schematic[nx][ny]
				if cell.isNumber && cell.isVisited == false {
					num := utils.ToInt(cell.value)
					cell.isVisited = true
					source.adjacentNumbers = append(source.adjacentNumbers, num)
					source.nAdjacentNumbers++
				}
			}
		}
	}
}

func parseschematic(schematic [][]*Cell) {
	for x, row := range schematic {
		for y, cell := range row {
			if cell.isSymbol {
				parseAdjacentNumbers(cell, schematic, x, y)
			}
		}
	}
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

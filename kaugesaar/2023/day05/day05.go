package day05

import (
	_ "embed" // For embedding the input file
	"kaugesaar-aoc/solution"
	"kaugesaar-aoc/utils"
	"regexp"
	"strings"
	"unicode"
)

//go:embed day5.txt
var fileInput string

// Solver for day 5 and its both parts
type Solver struct{}

type Instruction struct {
	SourceNumber      int
	DestinationNumber int
	Length            int
}

type Map struct {
	Source       string
	Destination  string
	Instructions []Instruction
}

type Almanac struct {
	SeedsToBePlanted []int
	Maps             map[string]Map
}

func parser() Almanac {
	var almanac Almanac
	var mapName string
	var currentMap Map

	almanac.Maps = make(map[string]Map)

	rows := strings.Split(strings.ReplaceAll(fileInput, " map:", ""), "\n")
	digits := regexp.MustCompile(`\d+`)

	for _, seed := range digits.FindAllString(rows[0], -1) {
		almanac.SeedsToBePlanted = append(almanac.SeedsToBePlanted, utils.ToInt(seed))
	}

	rows = rows[1:]

	for i, row := range rows {

		if mapName != "" && row == "" || len(rows) == i+1 {
			almanac.Maps[mapName] = currentMap
			currentMap = Map{}
		}

		if row == "" {
			continue
		}

		if unicode.IsLetter(rune(row[0])) {
			splits := strings.Split(row, "-")
			mapName = row
			currentMap.Source = splits[0]
			currentMap.Destination = splits[2]
		}

		if unicode.IsDigit(rune(row[0])) {
			nums := digits.FindAllString(row, -1)
			destStart := utils.ToInt(nums[0])
			sourceStart := utils.ToInt(nums[1])
			length := utils.ToInt(nums[2])
			currentMap.Instructions = append(currentMap.Instructions, Instruction{
				SourceNumber:      sourceStart,
				DestinationNumber: destStart,
				Length:            length,
			})
		}

	}

	return almanac
}

func plant(sourceNumber int, m Map) int {

	for _, ins := range m.Instructions {
		if sourceNumber >= ins.SourceNumber && sourceNumber < ins.SourceNumber+ins.Length {
			offset := sourceNumber - ins.SourceNumber
			return ins.DestinationNumber + offset
		}
	}

	return sourceNumber
}

func isInRange(a, b, len int) bool {
	if a+len > b {
		return true
	}
	return false
}

func p1() string {
	almanac := parser()

	min := int(^uint(0) >> 1)

	for _, seed := range almanac.SeedsToBePlanted {
		soil := plant(seed, almanac.Maps["seed-to-soil"])
		fertilizer := plant(soil, almanac.Maps["soil-to-fertilizer"])
		water := plant(fertilizer, almanac.Maps["fertilizer-to-water"])
		light := plant(water, almanac.Maps["water-to-light"])
		temperature := plant(light, almanac.Maps["light-to-temperature"])
		humidity := plant(temperature, almanac.Maps["temperature-to-humidity"])
		location := plant(humidity, almanac.Maps["humidity-to-location"])

		min = utils.MinInt(min, location)
	}

	return utils.ToStr(min)
}

func p2() string {
	return ""
}

// Part1 the solution for part 1, day 5
func (s Solver) Part1() solution.Response {
	return solution.Response{
		Day:    3,
		Part:   1,
		Answer: p1(),
	}
}

// Part2 the solution for part 2, day 5
func (s Solver) Part2() solution.Response {
	return solution.Response{
		Day:    3,
		Part:   2,
		Answer: p2(),
	}
}

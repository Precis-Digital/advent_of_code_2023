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

type Seed struct {
	Start  int
	Length int
}

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
	Seeds            []Seed
	Maps             map[string]Map
}

func parser() Almanac {
	var almanac Almanac
	var mapName string
	var currentMap Map

	almanac.Maps = make(map[string]Map)

	rows := strings.Split(strings.ReplaceAll(fileInput, " map:", ""), "\n")
	digitRe := regexp.MustCompile(`\d+`)
	nums := digitRe.FindAllString(rows[0], -1)

	for _, seed := range nums {
		almanac.SeedsToBePlanted = append(almanac.SeedsToBePlanted, utils.ToInt(seed))
	}

	for i := 0; i < len(nums); i += 2 {
		almanac.Seeds = append(almanac.Seeds, Seed{
			Start:  utils.ToInt(nums[i]),
			Length: utils.ToInt(nums[i+1]),
		})
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
			nums := digitRe.FindAllString(row, -1)
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

func reversePlant(destNumber int, m Map) int {
	for _, ins := range m.Instructions {
		if destNumber >= ins.DestinationNumber && destNumber < ins.DestinationNumber+ins.Length {
			offset := destNumber - ins.DestinationNumber
			return ins.SourceNumber + offset
		}
	}
	return destNumber
}

func isValidSeed(a Almanac, seed int) bool {
	for _, s := range a.Seeds {
		if seed >= s.Start && seed < s.Start+s.Length {
			return true
		}
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
	almanac := parser()

	min := int(^uint(0) >> 1)
	testLocation := 0

	for min == int(^uint(0)>>1) {
		humidity := reversePlant(testLocation, almanac.Maps["humidity-to-location"])
		temperature := reversePlant(humidity, almanac.Maps["temperature-to-humidity"])
		light := reversePlant(temperature, almanac.Maps["light-to-temperature"])
		water := reversePlant(light, almanac.Maps["water-to-light"])
		fertilizer := reversePlant(water, almanac.Maps["fertilizer-to-water"])
		soil := reversePlant(fertilizer, almanac.Maps["soil-to-fertilizer"])
		seed := reversePlant(soil, almanac.Maps["seed-to-soil"])

		if isValidSeed(almanac, seed) {
			min = testLocation
		}

		testLocation++
	}

	return utils.ToStr(min)
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

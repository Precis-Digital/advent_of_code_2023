package day04

import (
	_ "embed" // For embedding the input file
	"kaugesaar-aoc/solution"
	"kaugesaar-aoc/utils"
	"math"
	"regexp"
	"slices"
	"strings"
)

//go:embed day4.txt
var fileInput string

// Solver for day 4 and its both parts
type Solver struct{}

type Card struct {
	Numbers        []int
	WinningNumbers []int
}

var digitRegex = regexp.MustCompile(`\d+`)

func parser() []Card {
	var cards []Card
	rows := strings.Split(fileInput, "\n")

	for _, row := range rows {
		numbers := strings.Split(row, ": ")[1]
		var card Card
		for i, set := range strings.Split(numbers, " | ") {
			split := digitRegex.FindAllString(set, -1)
			for _, s := range split {
				if i == 0 {
					card.Numbers = append(card.Numbers, utils.ToInt(s))
				} else {
					card.WinningNumbers = append(card.WinningNumbers, utils.ToInt(s))
				}
			}
		}
		cards = append(cards, card)
	}

	return cards
}

func p1() string {
	sum := 0
	cards := parser()
	for _, card := range cards {
		matches := 0
		points := 0
		for _, n := range card.Numbers {
			if slices.Contains(card.WinningNumbers, n) {
				points = int(math.Pow(float64(2), float64(matches)))
				matches++
			}
		}
		sum += points
	}
	return utils.ToStr(sum)
}

func p2() string {
	cards := parser()
	nWins := make(map[int]int)
	instances := make(map[int]int)

	for i, card := range cards {
		wins := 0
		for _, n := range card.Numbers {
			if slices.Contains(card.WinningNumbers, n) {
				wins++
			}
		}
		nWins[i] = wins
		instances[i] = 1
	}

	var copies []int
	for i := range nWins {
		copies = append(copies, i)
	}

	for len(copies) != 0 {
		card := copies[0]
		wins := nWins[card]
		for _, c := range getCardsFrom(card+1, card+wins) {
			instances[c]++
			copies = append(copies, c)
		}
		copies = copies[1:]
	}

	sum := 0
	for _, n := range instances {
		sum += n
	}

	return utils.ToStr(sum)
}

func getCardsFrom(min, max int) []int {
	cards := make([]int, max-min+1)
	for i := range cards {
		cards[i] = min + i
	}
	return cards
}

// Part1 the solution for part 1, day 4
func (s Solver) Part1() solution.Response {
	return solution.Response{
		Day:    3,
		Part:   1,
		Answer: p1(),
	}
}

// Part2 the solution for part 2, day 4
func (s Solver) Part2() solution.Response {
	return solution.Response{
		Day:    3,
		Part:   2,
		Answer: p2(),
	}
}

package day04

import (
	"kaugesaar-aoc/solution"
	"kaugesaar-aoc/utils"
	"math"
	"regexp"
	"slices"
	"strings"
)

// Solver for day 4 and its both parts
type Solver struct{}

type Card struct {
	Numbers        []int
	WinningNumbers []int
}

var digitRe = regexp.MustCompile(`\d+`)

func parser() []Card {
	rows := utils.ReadFile("day4.txt")

	cards := make([]Card, len(rows))

	for i, row := range rows {
		var card Card
		parts := strings.SplitN(row, ": ", 2)
		ticketParts := strings.SplitN(parts[1], " | ", 2)

		card.Numbers = parseNumbers(ticketParts[0])
		card.WinningNumbers = parseNumbers(ticketParts[1])
		cards[i] = card
	}

	return cards
}

func parseNumbers(input string) []int {
	numStrs := digitRe.FindAllString(input, -1)
	nums := make([]int, len(numStrs))

	for i, numStr := range numStrs {
		nums[i] = utils.ToInt(numStr)
	}

	return nums
}

func p1() string {
	sum := 0
	cards := parser()

	for _, card := range cards {
		wins := 0
		points := 0
		for _, n := range card.Numbers {
			if slices.Contains(card.WinningNumbers, n) {
				points = int(math.Pow(float64(2), float64(wins)))
				wins++
			}
		}
		sum += points
	}

	return utils.ToStr(sum)
}

func p2() string {
	cards := parser()
	copies := make([]int, len(cards))
	for i := range copies {
		copies[i] = 1
	}

	for i, card := range cards {
		wins := 0
		for _, n := range card.Numbers {
			if slices.Contains(card.WinningNumbers, n) {
				wins++
			}
		}
		for j := 0; j < wins; j++ {
			// "Cards will never make you copy a card past the end of the table."
			copies[i+j+1] += copies[i]
		}
	}

	sumCopies := 0
	for _, v := range copies {
		sumCopies += v
	}

	return utils.ToStr(sumCopies)
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

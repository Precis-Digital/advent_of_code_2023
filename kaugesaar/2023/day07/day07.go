package day07

import (
	_ "embed" // For embedding the input file
	"kaugesaar-aoc/solution"
	"kaugesaar-aoc/utils"
	"sort"
	"strings"
)

const (
	fiveOfAKind  = 7
	fourOfAKind  = 6
	fullHouse    = 5
	threeOfAKind = 4
	twoPair      = 3
	pair         = 2
	nothing      = 1
)

// Solver for day 7 and its both parts
type Solver struct{}

//go:embed day7.txt
var fileInput string

func cardIndex(c rune, isPartTwo bool) int {
	switch c {
	case 'A':
		return 14
	case 'K':
		return 13
	case 'Q':
		return 12
	case 'J':
		if isPartTwo {
			return 1
		}
		return 11
	case 'T':
		return 10
	default:
		return int(c - '0')
	}
}

func getHandType(counts []int, jokers int) int {
	max := 0
	for _, count := range counts {
		if count > max {
			max = count
		}
	}

	switch {
	case max+jokers == 5:
		return fiveOfAKind

	case max+jokers == 4:
		return fourOfAKind

	case max == 3:
		for _, count := range counts {
			if count == 2 {
				return fullHouse
			}
		}
		return threeOfAKind

	case max == 2:
		pairs := 0
		for _, count := range counts {
			if count == 2 {
				pairs++
			}
		}
		switch {
		case pairs == 2 && jokers == 1:
			return fullHouse
		case pairs == 1 && jokers == 1:
			return threeOfAKind
		case pairs == 2 && jokers == 0:
			return twoPair
		default:
			return pair
		}
	case max == 1 && jokers == 2:
		return threeOfAKind
	case max == 1 && jokers == 1:
		return pair
	default:
		return nothing
	}
}

func handStrength(cards string, isPartTwo bool) (int, int) {
	jokers := 0
	countsByCard := make(map[rune]int)
	for _, c := range cards {
		if isPartTwo && c == 'J' {
			jokers++
		} else {
			countsByCard[c]++
		}
	}

	counts := make([]int, 0, len(countsByCard))
	for _, v := range countsByCard {
		counts = append(counts, v)
	}

	idx := 0
	for _, c := range cards {
		idx = (idx << 4) + cardIndex(c, isPartTwo)
	}

	return getHandType(counts, jokers), idx
}

func parser(isPartTwo bool) [][]int {
	rows := strings.Split(fileInput, "\n")
	hands := make([][]int, 0)
	for _, row := range rows {
		if row == "" {
			continue
		}

		hand := make([]int, 3)
		parts := strings.Split(row, " ")

		hand[0], hand[1] = handStrength(parts[0], isPartTwo)
		hand[2] = utils.ToInt(parts[1])
		hands = append(hands, hand)
	}

	sort.Slice(hands, func(i, j int) bool {
		if hands[i][0] == hands[j][0] {
			return hands[i][1] < hands[j][1]
		}
		return hands[i][0] < hands[j][0]
	})

	return hands
}

func p1() string {
	sum := 0
	hands := parser(false)

	for i, hand := range hands {
		sum += hand[2] * (i + 1)
	}

	return utils.ToStr(sum)
}

func p2() string {
	sum := 0
	hands := parser(true)

	for i, hand := range hands {
		sum += hand[2] * (i + 1)
	}

	return utils.ToStr(sum)
}

// Part1 the solution for part 1, day 7
func (s Solver) Part1() solution.Response {
	return solution.Response{
		Day:    7,
		Part:   1,
		Answer: p1(),
	}
}

// Part2 the solution for part 2, day 7
func (s Solver) Part2() solution.Response {
	return solution.Response{
		Day:    7,
		Part:   2,
		Answer: p2(),
	}
}

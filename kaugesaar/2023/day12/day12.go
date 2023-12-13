package day12

import (
	"fmt"
	"kaugesaar-aoc/solution"
	"kaugesaar-aoc/utils"
	"strings"
)

// Solver for day 12 and its both parts
type Solver struct{}

func parser() ([]string, [][]int) {
	rows := utils.ReadFile("day12.txt")
	springs := make([]string, len(rows))
	nums := make([][]int, len(rows))
	for r, row := range rows {
		parts := strings.SplitN(row, " ", 2)
		springs[r] = parts[0]
		sizes := strings.Split(parts[1], ",")
		size := make([]int, len(sizes))
		for i := range sizes {
			size[i] = utils.ToInt(sizes[i])
		}
		nums[r] = size
	}
	return springs, nums
}

func encodeState(springsLen, withinVal, remainingLen int) int {
	return (springsLen << 20) | (withinVal << 10) | remainingLen
}

func possibleWays(cache map[int]int, springs string, within *int, remaining []int) int {
	withinVal := 0
	if within != nil {
		withinVal = *within
	}

	key := encodeState(len(springs), withinVal, len(remaining))
	if val, ok := cache[key]; ok {
		return val
	}

	if len(remaining) > 0 && withinVal > remaining[0] {
		return 0
	}

	if len(springs) == 0 {
		if within == nil && len(remaining) == 0 {
			return 1
		}
		if within != nil && len(remaining) == 1 && *within == remaining[0] {
			return 1
		}
		return 0
	}
	if within != nil && len(remaining) == 0 {
		return 0
	}

	ways := 0

	switch springs[0] {
	case '.':
		if within != nil && *within != remaining[0] {
			ways = 0
		} else if within != nil {
			ways = possibleWays(cache, springs[1:], nil, remaining[1:])
		} else {
			ways = possibleWays(cache, springs[1:], nil, remaining)
		}
	case '#':
		if within != nil {
			newWithin := *within + 1
			ways = possibleWays(cache, springs[1:], &newWithin, remaining)
		} else {
			newWithin := 1
			ways = possibleWays(cache, springs[1:], &newWithin, remaining)
		}
	case '?':
		if within != nil {
			newWithin := *within + 1
			ways = possibleWays(cache, springs[1:], &newWithin, remaining)
			if *within == remaining[0] {
				ways += possibleWays(cache, springs[1:], nil, remaining[1:])
			}
		} else {
			newWithin := 1
			ways = possibleWays(cache, springs[1:], &newWithin, remaining) + possibleWays(cache, springs[1:], nil, remaining)
		}
	default:
		panic(fmt.Sprintf("spaghetti code panic!! %s", string(springs[0])))
	}

	cache[key] = ways
	return ways
}

func p1() string {
	springs, nums := parser()
	sum := 0
	for i := range springs {
		sum += possibleWays(make(map[int]int), springs[i], nil, nums[i])
	}
	return utils.ToStr(sum)
}

func p2() string {
	springs, nums := parser()
	sum := 0
	for i := range springs {
		unfoldedSprings := strings.Repeat(springs[i]+"?", 4) + springs[i]
		unfoldedNums := make([]int, 0, len(nums[i])*5)
		for j := 0; j < 5; j++ {
			unfoldedNums = append(unfoldedNums, nums[i]...)
		}
		sum += possibleWays(make(map[int]int), unfoldedSprings, nil, unfoldedNums)
	}
	return utils.ToStr(sum)
}

// Part1 the solution for part 1, day 12
func (s Solver) Part1() solution.Response {
	return solution.Response{
		Day:    12,
		Part:   1,
		Answer: p1(),
	}
}

// Part2 the solution for part 2, day 12
func (s Solver) Part2() solution.Response {
	return solution.Response{
		Day:    12,
		Part:   2,
		Answer: p2(),
	}
}

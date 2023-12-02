package day02

import (
	_ "embed" // For embedding the input file
	"kaugesaar-aoc/common"
	"kaugesaar-aoc/utils"
	"regexp"
	"strings"
)

//go:embed day2.txt
var fileInput string

// Solver for day 1 and its both parts
type Solver struct{}

// Game contains the game data
type Game struct {
	GameID  int
	IsValid bool
	Blue    int
	Green   int
	Red     int
}

func parser() []Game {
	rows := strings.Split(fileInput, "\n")

	var games []Game

	for i, row := range rows {
		var game Game
		game.GameID = i + 1
		game.IsValid = true

		for _, subGame := range strings.Split(row, ";") {
			blues := regexp.MustCompile(`(\d+) blue`).FindAllStringSubmatch(subGame, -1)
			reds := regexp.MustCompile(`(\d+) red`).FindAllStringSubmatch(subGame, -1)
			greens := regexp.MustCompile(`(\d+) green`).FindAllStringSubmatch(subGame, -1)

			for _, red := range reds {
				game.Red = utils.MaxInt(game.Red, utils.ToInt(red[1]))
			}

			for _, green := range greens {
				game.Green = utils.MaxInt(game.Green, utils.ToInt(green[1]))
			}

			for _, blue := range blues {
				game.Blue = utils.MaxInt(game.Blue, utils.ToInt(blue[1]))
			}

			if game.Red > 12 || game.Green > 13 || game.Blue > 14 {
				game.IsValid = false
			}

		}

		games = append(games, game)
	}

	return games
}

func p1() string {
	games := parser()

	validGames := 0

	for _, game := range games {
		if game.IsValid {
			validGames += game.GameID
		}
	}

	return utils.ToStr(validGames)
}

func p2() string {
	games := parser()

	totalPower := 0

	for _, game := range games {
		power := game.Red * game.Green * game.Blue
		totalPower += power
	}

	return utils.ToStr(totalPower)
}

// Part1 the solution for part 1, day 1
func (s Solver) Part1() common.Solution {
	return common.Solution{
		Day:    1,
		Part:   1,
		Answer: p1(),
	}
}

// Part2 the solution for part 2, day 1
func (s Solver) Part2() common.Solution {
	return common.Solution{
		Day:    1,
		Part:   2,
		Answer: p2(),
	}
}

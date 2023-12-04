package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

// i need to create a data structure like Games = map[gameId]Array[games] where games is a counter where the keys are red, blue, green

type Round struct {
	red   int
	blue  int
	green int
}

type Games map[int][]Round

func GamesFromScanner(s *bufio.Scanner) Games {
	games := make(map[int][]Round)

	for s.Scan() {
		row := s.Text()
		fmt.Println(row)

		r, _ := regexp.Compile("Game ([0-9]+)")

		// sample in put Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green

		// split the string on the colon
		rowSplit := strings.Split(row, ":")
		rowSplit[0] = strings.TrimSpace(rowSplit[0])

		// this is the game id as int
		gameId, _ := strconv.Atoi(r.FindStringSubmatch(rowSplit[0])[1])

		if _, ok := games[gameId]; !ok {
			games[gameId] = []Round{}
		}

		// next break the string on the semicolon
		rawRounds := strings.Split(rowSplit[1], ";")
		for _, rawRound := range rawRounds {
			var round Round
			// now we have a round, we need to split it on the comma
			rawColors := strings.Split(rawRound, ",")
			for _, color := range rawColors {
				// now we have a color, we need to split it on the space
				rawColor := strings.Split(color, " ")
				// now we have a color and a number
				color := rawColor[2]
				number, _ := strconv.Atoi(rawColor[1])
				if color == "red" {
					round.red = number
				}
				if color == "blue" {
					round.blue = number
				}
				if color == "green" {
					round.green = number
				}
				fmt.Println(color, number)
			}
			games[gameId] = append(games[gameId], round)
		}

	}
	return games
}

func problem1(games Games) int {
	redCubes := 12
	greenCubes := 13
	blueCubes := 14

	sumOfGameIdsForValidGames := 0

	for gameId, rounds := range games {
		gamePossible := true
		for _, round := range rounds {
			if round.red > redCubes || round.green > greenCubes || round.blue > blueCubes {
				gamePossible = false
			}
		}
		if gamePossible {
			sumOfGameIdsForValidGames += gameId
		}
	}
	return sumOfGameIdsForValidGames
}



func problem2(games Games) int {

	sumOfGameIdsForValidGames := 0

	for _, rounds := range games {
		maxRedCubes := 0
		maxGreenCubes := 0
		maxBlueCubes := 0
		for _, round := range rounds {
			if maxRedCubes < round.red {
				maxRedCubes = round.red
			}
			if maxGreenCubes < round.green {
				maxGreenCubes = round.green
			}
			if maxBlueCubes < round.blue {
				maxBlueCubes = round.blue
			}
		}
		sumOfGameIdsForValidGames += maxRedCubes * maxGreenCubes * maxBlueCubes
	}
	return sumOfGameIdsForValidGames
}

func main() {
	fileName := os.Args[1]
	version := os.Args[2]

	fmt.Println("File Name: ", fileName, version)

	file, err := os.Open(fileName)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close() // defer closing the file

	scanner := bufio.NewScanner(file)
	games := GamesFromScanner(scanner)

	// fmt.Println(games)
	fmt.Println("Answer Problem 1:", problem1(games))
	fmt.Println("Answer Problem 2:", problem2(games))
}

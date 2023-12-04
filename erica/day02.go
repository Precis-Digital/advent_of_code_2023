package main

import (
    "fmt"
    "strings"
    "regexp"
    "strconv"
    "erica/utils"
)

var STONE_LIMITS = map[string]int{
    "red":   12,
    "green": 13,
    "blue":  14,
}

func evaluateRounds(rounds []string) (bool, map[string]int) {
    gameIsPossible := true
    stonesNeeded := map[string]int{
        "red":   0,
        "green": 0,
        "blue":  0,
    }

    for _, gameRound := range rounds {
        for color, value := range STONE_LIMITS {
            re := regexp.MustCompile(fmt.Sprintf(`(\d+)\s+%s`, color))
            nrStonesByColor := re.FindAllStringSubmatch(gameRound, -1)

            stonesByRound := 0
            for _, match := range nrStonesByColor {
                stones, _ := strconv.Atoi(match[1])
                stonesByRound += stones
            }

            stonesNeeded[color] = max(stonesNeeded[color], stonesByRound)

            if stonesByRound > value {
                gameIsPossible = false
            }
        }
    }

    return gameIsPossible, stonesNeeded
}

func findPossibleGamesAndPowerOfStones(games []string) ([]int, []int) {
    possibleGames := []int{}
    powerOfStones := []int{}

    for _, game := range games {
        roundsInGame := strings.Split(game, ";")
        gameIsPossible, maxDict := evaluateRounds(roundsInGame)

        prod := 1
        for _, value := range maxDict {
            prod *= value
        }
        powerOfStones = append(powerOfStones, prod)

        if gameIsPossible {
            gameKey := strings.Replace(strings.Split(game, ":")[0], "Game ", "", 1)
            gameKeyInt, _ := strconv.Atoi(gameKey)
            possibleGames = append(possibleGames, gameKeyInt)
        }
    }

    return possibleGames, powerOfStones
}

func main() {
    inputFilePath := "inputs/day02.txt"
    content, _ := utils.ReadFile(inputFilePath)

    puzzleInput := strings.Split(strings.TrimSpace(content), "\n")
    possibleGameKeys, powerOfStonesPerGame := findPossibleGamesAndPowerOfStones(puzzleInput)

    sumPossibleGameKeys := 0
    sumPowerOfStonesPerGame := 0

    for _, key := range possibleGameKeys {
        sumPossibleGameKeys += key
    }

    for _, power := range powerOfStonesPerGame {
        sumPowerOfStonesPerGame += power
    }

    fmt.Printf("Solution 1: %d\n", sumPossibleGameKeys)
    fmt.Printf("Solution 2: %d\n", sumPowerOfStonesPerGame)
}

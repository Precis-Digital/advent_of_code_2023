package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

type Cards map[int][][]int

func sliceAtoi(sa []string) ([]int, error) {
	si := make([]int, 0, len(sa))
	for _, a := range sa {
		i, err := strconv.Atoi(a)
		if err != nil {
			return si, err
		}
		si = append(si, i)
	}
	return si, nil
}

func IntPow(n, m int) int {
	if m == 0 {
		return 1
	}
	result := n
	for i := 2; i <= m; i++ {
		result *= n
	}
	return result
}

func ArraySum(numbers []int) int {
	sum := 0
	for _, number := range numbers {
		sum += number
	}
	return sum
}

func preProcess(s *bufio.Scanner) Cards {
	s.Split(bufio.ScanLines)
	r, _ := regexp.Compile(`(\d+)`)

	game := make(Cards)
	for s.Scan() {
		//Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
		/// {1: [[41 48 83 86 17] [83 86  6 31 17  9 48 53]]}
		row := s.Text()
		card := strings.Split(row, ": ")[0]
		numbers := strings.Split(row, ": ")[1]
		cardNumber, err := strconv.Atoi(r.FindString(card))
		if err != nil {
			panic(err)
		}

		winningNumbers, err := sliceAtoi(r.FindAllString(strings.Split(numbers, " | ")[0], -1))
		if err != nil {
			panic(err)
		}

		playerNumbers, err := sliceAtoi(r.FindAllString(strings.Split(numbers, " | ")[1], -1))
		if err != nil {
			panic(err)
		}

		game[cardNumber] = [][]int{winningNumbers, playerNumbers}
	}
	return game
}

func calculateNumberOfWiningNumbers(winningNumbers []int, playerNumbers []int) int {

	winningNumberMap := make(map[int]bool)
	for _, winningNumber := range winningNumbers {
		winningNumberMap[winningNumber] = true
	}

	winningNumberCount := 0
	for _, playerNumber := range playerNumbers {
		if _, ok := winningNumberMap[playerNumber]; ok {
			winningNumberCount++
		}
	}
	return winningNumberCount
}
func problem1(cards Cards) int {

	totalScore := 0

	for _, card := range cards {
		winningNumbers := card[0]
		playerNumbers := card[1]
		winningNumberCount := calculateNumberOfWiningNumbers(winningNumbers, playerNumbers)
		if winningNumberCount > 0 {
			totalScore += IntPow(2, (winningNumberCount - 1))
		}
	}
	return totalScore
}

func problem2(cards Cards) int {
	numCards := len(cards)

	winninNumberCache := make(map[int]int)
	counterArray := make([]int, numCards+1)

	// initialize the array with ones and pre-compute the winning numbers
	for i := 1; i <= numCards; i++ {
		cardNumber := i
		winningNumberCount := calculateNumberOfWiningNumbers(cards[cardNumber][0], cards[cardNumber][1])
		counterArray[i] = 1
		winninNumberCache[i] = winningNumberCount
	}

	for i := 1; i <= numCards; i++ {

		cardNumber := i
		winningNumberCount := winninNumberCache[cardNumber]
		for j := i + 1; j <= i+winningNumberCount; j++ {
			counterArray[j] += counterArray[i]
		}
	}

	// fmt.Println(winninNumberCache, counterArray)

	return ArraySum(counterArray)
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
	cards := preProcess(scanner)
	fmt.Println("Answer Problem 1:", problem1(cards))
	fmt.Println("Answer Problem 2:", problem2(cards))
}

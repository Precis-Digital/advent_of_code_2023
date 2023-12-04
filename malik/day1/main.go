package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
)

// laziness with n
func replaceStringNumebersWithDigits(s string) string {
	m := make(map[string]string)
	m["one"] = "1"
	m["two"] = "2"
	m["three"] = "3"
	m["four"] = "4"
	m["five"] = "5"
	m["six"] = "6"
	m["seven"] = "7"
	m["eight"] = "8"
	m["nine"] = "9"

	val, ok := m[s]
	if ok {
		return val
	}
	return s

}

func Reverse(s string) string {
	runes := []rune(s)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

func main() {

	fileName := os.Args[1]

	version := os.Args[2]

	fmt.Println("File Name: ", fileName)

	file, err := os.Open(fileName)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close() // defer closing the file

	scanner := bufio.NewScanner(file)

	if version == "v1" {
		fmt.Println("expected answer: 55208")
	}

	if version == "v2" {
		fmt.Println("expected answer: 54578")
	}

	answer := 0

	for scanner.Scan() {
		row := scanner.Text()

		number := 0

		if version == "v2" {
			r2, _ := regexp.Compile("[0-9]|one|two|three|four|five|six|seven|eight|nine")
			r3, _ := regexp.Compile("[0-9]|enin|thgie|neves|xis|evif|ruof|eerht|owt|eno")

			l := replaceStringNumebersWithDigits(r2.FindString(row))
			r := replaceStringNumebersWithDigits(Reverse(r3.FindString(Reverse(row))))
			a, _ := strconv.Atoi(l)
			b, _ := strconv.Atoi(r)
			number = a*10 + b
		} else {
			r, _ := regexp.Compile("[0-9]")
			found := r.FindAllString(row, -1)
			a, _ := strconv.Atoi(found[0])
			b, _ := strconv.Atoi(found[len(found)-1])
			number = a*10 + b

		}
		// fmt.Println("row:", row)
		// fmt.Println("numer", number)

		// fmt.Println(found, number)
		answer += number

	}

	fmt.Println("Answer: ", answer)

	if err := scanner.Err(); err != nil {
		fmt.Println("Error reading from file:", err)
	}
}

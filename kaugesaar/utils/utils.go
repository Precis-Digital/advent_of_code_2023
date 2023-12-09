package utils

import (
	"bufio"
	"os"
	"strconv"
)

func ReadFile(filename string) []string {
	rows := []string{}
	file, _ := os.Open(filename)
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		rows = append(rows, scanner.Text())
	}
	return rows
}

func ToInt(s string) int {
	i, _ := strconv.Atoi(s)
	return i
}

func ToStr(i int) string {
	return strconv.Itoa(i)
}

func MaxInt(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func MinInt(a, b int) int {
	if a > b {
		return b
	}
	return a
}

func SumArr(arr []int) int {
	sum := 0
	for _, value := range arr {
		sum += value
	}
	return sum
}

func MinArr(arr []int) int {
	min := arr[0]
	for _, value := range arr {
		if value < min {
			min = value
		}
	}
	return min
}

func ReverseIntArray(arr []int) []int {
	reversed := make([]int, len(arr))
	for i, value := range arr {
		reversed[len(arr)-1-i] = value
	}
	return reversed
}

func LCM(a, b int, ints ...int) int {
	result := a * b / GCD(a, b)
	for _, i := range ints {
		result = LCM(result, i)
	}
	return result
}

func GCD(a, b int) int {
	if a == 0 {
		return b
	}
	return GCD(b%a, a)
}

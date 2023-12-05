package utils

import "strconv"

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

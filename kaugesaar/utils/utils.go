package utils

import (
	"bufio"
	"os"
	"path/filepath"
	"strconv"
	"strings"
)

func ReadFileByNN(filename string) [][]string {
	rows := ReadFile(filename)
	var lines [][]string
	var line []string

	for i, row := range rows {
		if len(row) == 0 {
			line = make([]string, 0)
			continue
		}

		line = append(line, row)

		if len(rows)-1 == i || len(rows[i+1]) == 0 {
			lines = append(lines, line)
		}
	}

	return lines
}

func ReadFile(filename string) []string {
	rows := []string{}

	wd, _ := os.Getwd()
	isTestRun := ""

	if strings.Contains(wd, "day") {
		isTestRun = "../../"
	}

	file, err := os.Open(filepath.Join(wd, isTestRun, "./inputs", filename))
	if err != nil {
		panic(err)
	}

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

func Abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func LevenshteinDistance(str1, str2 string) int {
	lenStr1 := len(str1)
	lenStr2 := len(str2)

	dp := make([][]int, lenStr1+1)
	for i := range dp {
		dp[i] = make([]int, lenStr2+1)
	}

	for i := 0; i <= lenStr1; i++ {
		for j := 0; j <= lenStr2; j++ {
			if i == 0 {
				dp[i][j] = j
			} else if j == 0 {
				dp[i][j] = i
			} else if str1[i-1] == str2[j-1] {
				dp[i][j] = dp[i-1][j-1]
			} else {
				dp[i][j] = 1 + min(dp[i-1][j],
					dp[i][j-1],
					dp[i-1][j-1])
			}
		}
	}

	return dp[lenStr1][lenStr2]
}

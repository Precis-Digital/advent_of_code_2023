package main

import (
	"fmt"
	"kaugesaar-aoc/2023/day01"
	"kaugesaar-aoc/2023/day02"
	"kaugesaar-aoc/common"
	"kaugesaar-aoc/utils"
	"os"
	"time"
)

type Solver interface {
	Part1() common.Solution
	Part2() common.Solution
}

var solvers = []Solver{
	day01.Solver{},
	day02.Solver{},
}

func run(solve func() common.Solution) {
	start := time.Now()
	s := solve()
	elapsed := time.Since(start)
	ms := float64(elapsed.Nanoseconds()) / 1e6

	fmt.Printf("P%d | %s | %0.3fms\n", s.Part, s.Answer, ms)
}

func printDay(day int) {
	fmt.Printf("------- 🎄 Day %d 🎄 -------\n", day)
}

func runAllSolvers() {
	for i, solver := range solvers {
		printDay(i + 1)
		run(solver.Part1)
		run(solver.Part2)
	}
}

func runSolver(day string, part string) {
	d := utils.ToInt(day)
	solver := solvers[d-1]

	printDay(d)

	switch part {
	case "1":
		run(solver.Part1)
	case "2":
		run(solver.Part2)
	default:
		run(solver.Part1)
		run(solver.Part2)
	}
}

func main() {
	numArgs := len(os.Args)

	switch numArgs {
	case 1:
		runAllSolvers()
	case 2:
		runSolver(os.Args[1], "")
	case 3:
		runSolver(os.Args[1], os.Args[2])
	default:
		fmt.Println("Invalid number of arguments")
		os.Exit(1)
	}
}

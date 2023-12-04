package cmd

import (
	"fmt"
	"kaugesaar-aoc/solution"
	"time"

	"github.com/spf13/cobra"
)

func runSolver(cmd *cobra.Command, args []string) {
	day, _ := cmd.Flags().GetInt("day")
	part, _ := cmd.Flags().GetInt("part")

	if day == 0 {
		runAllSolvers()
		return
	}

	runDayPart(day, part)
}

func runAllSolvers() {
	for i, solver := range solvers {
		printDay(i + 1)
		run(solver.Part1)
		run(solver.Part2)
	}
}

func runDayPart(day int, part int) {
	solver := solvers[day-1]

	printDay(day)

	switch part {
	case 1:
		run(solver.Part1)
	case 2:
		run(solver.Part2)
	default:
		run(solver.Part1)
		run(solver.Part2)
	}
}

func run(solve func() solution.Response) {
	start := time.Now()
	s := solve()
	elapsed := time.Since(start)
	ms := float64(elapsed.Nanoseconds()) / 1e6

	fmt.Printf("P%d | %s | %0.3fms\n", s.Part, s.Answer, ms)
}

func printDay(day int) {
	fmt.Printf("------- 🎄 Day %d 🎄 -------\n", day)
}

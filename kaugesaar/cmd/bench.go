package cmd

import (
	"fmt"
	"kaugesaar-aoc/solution"
	"testing"

	"github.com/spf13/cobra"
)

type Benchmark struct {
	f func() solution.Response
}

var benchmark Benchmark

func runBench(cmd *cobra.Command, args []string) {
	day, _ := cmd.Flags().GetInt("day")
	part, _ := cmd.Flags().GetInt("part")

	fmt.Println("---- 🔨 Running benchmark 🔨 ----")
	fmt.Println("| Day | Part | Runtime |")
	fmt.Println("|-----|------|---------|")

	if day == 0 {
		runAllBenchmarks()
		return
	}

	runBenchmarkDayPart(day, part)
}

func runAllBenchmarks() {
	for i, solver := range solvers {
		bench(solver.Part1, i+1, 1)
		bench(solver.Part2, i+1, 2)
	}
}

func runBenchmarkDayPart(day int, part int) {
	solver := solvers[day-1]

	switch part {
	case 1:
		bench(solver.Part1, day, 1)
	case 2:
		bench(solver.Part2, day, 2)
	default:
		bench(solver.Part1, day, 1)
		bench(solver.Part2, day, 2)
	}
}

func runBenchmark(t *testing.B) {
	for i := 0; i < t.N; i++ {
		benchmark.f()
	}
}

func bench(solve func() solution.Response, day int, part int) {
	benchmark.f = solve
	t := testing.Benchmark(runBenchmark)
	fmt.Printf("|  %d  |  %d   | %.3fms |\n", day, part, toMs(t.NsPerOp()))
}

func toMs(nsPerOp int64) float64 {
	return float64(nsPerOp) / 1000000.0
}

package cmd

import (
	"kaugesaar-aoc/2023/day01"
	"kaugesaar-aoc/2023/day02"
	"kaugesaar-aoc/solution"

	"github.com/spf13/cobra"
)

var solvers = []solution.Solver{
	day01.Solver{},
	day02.Solver{},
}

// NewCLI returns the root command for the CLI
func NewCLI() *cobra.Command {
	rootCmd := &cobra.Command{
		Use:   "aoc",
		Short: "aoc is a CLI tool for solving Advent of Code puzzles",
	}

	run := &cobra.Command{
		Use:   "run",
		Short: "Run all solvers, or optionally specify the day and part",
		Run:   runSolver,
	}

	run.PersistentFlags().Int("day", 0, "Specify the day")
	run.PersistentFlags().Int("part", 0, "Specify the part")

	bench := &cobra.Command{
		Use:   "bench",
		Short: "Benchmark all solvers, or optionally specify the day and part",
		Run:   runBench,
	}

	bench.PersistentFlags().Int("day", 0, "Specify the day")
	bench.PersistentFlags().Int("part", 0, "Specify the part")

	rootCmd.AddCommand(run, bench)

	return rootCmd
}

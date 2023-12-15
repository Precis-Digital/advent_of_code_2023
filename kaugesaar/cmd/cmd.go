package cmd

import (
	"kaugesaar-aoc/2023/day01"
	"kaugesaar-aoc/2023/day02"
	"kaugesaar-aoc/2023/day03"
	"kaugesaar-aoc/2023/day04"
	"kaugesaar-aoc/2023/day05"
	"kaugesaar-aoc/2023/day06"
	"kaugesaar-aoc/2023/day07"
	"kaugesaar-aoc/2023/day08"
	"kaugesaar-aoc/2023/day09"
	"kaugesaar-aoc/2023/day10"
	"kaugesaar-aoc/2023/day11"
	"kaugesaar-aoc/2023/day12"
	"kaugesaar-aoc/2023/day13"
	"kaugesaar-aoc/2023/day14"
	"kaugesaar-aoc/2023/day15"
	"kaugesaar-aoc/solution"

	"github.com/spf13/cobra"
)

var solvers = []solution.Solver{
	day01.Solver{},
	day02.Solver{},
	day03.Solver{},
	day04.Solver{},
	day05.Solver{},
	day06.Solver{},
	day07.Solver{},
	day08.Solver{},
	day09.Solver{},
	day10.Solver{},
	day11.Solver{},
	day12.Solver{},
	day13.Solver{},
	day14.Solver{},
	day15.Solver{},
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

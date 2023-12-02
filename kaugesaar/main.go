package main

import (
	"kaugesaar-aoc/cmd"

	"github.com/spf13/cobra"
)

func main() {
	cobra.CheckErr(cmd.NewCLI().Execute())
}

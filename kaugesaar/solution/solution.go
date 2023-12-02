package solution

type Solver interface {
	Part1() Response
	Part2() Response
}

type Response struct {
	Day    int
	Part   int
	Answer string
}

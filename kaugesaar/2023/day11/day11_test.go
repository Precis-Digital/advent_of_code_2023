package day11

import "testing"

func TestPart1(t *testing.T) {
	result := p1()
	expected := "9522407"
	if result != expected {
		t.Errorf("Result is incorrect, got %s, wanted: %s", result, expected)
	}
}

func TestPart2(t *testing.T) {
	result := p2()
	expected := "544723432977"
	if result != expected {
		t.Errorf("Result is incorrect, got %s, wanted: %s", result, expected)
	}
}

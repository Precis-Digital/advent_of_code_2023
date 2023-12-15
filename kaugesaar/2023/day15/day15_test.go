package day15

import "testing"

func TestPart1(t *testing.T) {
	result := p1()
	expected := "507291"
	if result != expected {
		t.Errorf("Result is incorrect, got %s, wanted: %s", result, expected)
	}
}

func TestPart2(t *testing.T) {
	result := p2()
	expected := "296921"
	if result != expected {
		t.Errorf("Result is incorrect, got %s, wanted: %s", result, expected)
	}
}

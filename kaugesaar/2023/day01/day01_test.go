package day01

import "testing"

func TestPart1(t *testing.T) {
	result := parser(1)
	expected := "56042"
	if result != expected {
		t.Errorf("Results is incorrect, got %s, wanted: %s", result, expected)
	}
}

func TestPart2(t *testing.T) {
	result := parser(2)
	expected := "55358"
	if result != expected {
		t.Errorf("Results is incorrect, got %s, wanted: %s", result, expected)
	}
}

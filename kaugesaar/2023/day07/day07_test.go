package day07

import "testing"

func TestPart1(t *testing.T) {
	result := p1()
	expected := "250474325"
	if result != expected {
		t.Errorf("Result is incorrect, got %s, wanted: %s", result, expected)
	}
}

func TestPart2(t *testing.T) {
	result := p2()
	expected := "248909434"
	if result != expected {
		t.Errorf("Result is incorrect, got %s, wanted: %s", result, expected)
	}
}

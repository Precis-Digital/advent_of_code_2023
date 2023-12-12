package day12

import "testing"

func TestPart1(t *testing.T) {
	result := p1()
	expected := "7732"
	if result != expected {
		t.Errorf("Result is incorrect, got %s, wanted: %s", result, expected)
	}
}

func TestPart2(t *testing.T) {
	result := p2()
	expected := "4500070301581"
	if result != expected {
		t.Errorf("Result is incorrect, got %s, wanted: %s", result, expected)
	}
}

package day05

import "testing"

func TestPart1(t *testing.T) {
	result := p1()
	expected := "31599214"
	if result != expected {
		t.Errorf("Results is incorrect, got %s, wanted: %s", result, expected)
	}
}

func TestPart2(t *testing.T) {
	result := p2()
	expected := "20358599"
	if result != expected {
		t.Errorf("Results is incorrect, got %s, wanted: %s", result, expected)
	}
}

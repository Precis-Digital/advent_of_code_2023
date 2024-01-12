package main

import (
	"bufio"
	"errors"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

func ToInt(s string) int {
	i, err := strconv.Atoi(s)
	if err != nil {
		panic(err)
	}
	return i
}

func strSliceToIntSlice(strs []string) ([]int, error) {
    var ints []int
    for _, s := range strs {
		num := ToInt(s)
        ints = append(ints, num)
    }
    return ints, nil
}

func ArrayMin(arr []int) int {
	min := arr[0]
	for _, val := range arr {
		if val < min {
			min = val
		}
	}
	return min
}


func generateSubRanges(sourceRange [2]int, mapRange [2]int) ([][2]int, error) {
	// note each range represents a closed interval inclusive of the first and last number
	sourceLowerBound := sourceRange[0]
	sourceUpperBound := sourceRange[1]
	mapLowerBound := mapRange[0]
	mapUpperBound := mapRange[1]

	// there is no overlap
	if sourceUpperBound < mapLowerBound || sourceLowerBound > mapUpperBound {
		return [][2]int{sourceRange}, nil	
	}

	// if the source range is a subset of the map range
	if sourceLowerBound >= mapLowerBound && sourceUpperBound <= mapUpperBound {
		return [][2]int{sourceRange}, nil
	}

	// if the lower bound of the map range intersects with the source range
	if mapLowerBound <= sourceUpperBound && mapLowerBound > sourceLowerBound && mapUpperBound >= sourceUpperBound {
		return [][2]int{[2]int{sourceLowerBound, mapLowerBound - 1}, [2]int{mapLowerBound, sourceUpperBound}}, nil
	}

	// if the upper bound of the map range intersects with the source range
	if mapUpperBound >= sourceLowerBound && mapUpperBound < sourceUpperBound && mapLowerBound <= sourceLowerBound {
		return [][2]int{[2]int{sourceLowerBound, mapUpperBound}, [2]int{mapUpperBound + 1, sourceUpperBound}}, nil
	}
	
	// if the map range is a subset of the source range
	if mapLowerBound > sourceLowerBound && mapUpperBound < sourceUpperBound {
		return [][2]int{[2]int{sourceLowerBound, mapLowerBound - 1}, [2]int{mapLowerBound, mapUpperBound}, [2]int{mapUpperBound + 1, sourceUpperBound}}, nil
	}

	return nil, errors.New("Error generating sub ranges")
}

func compareSubRange(a [2]int, b[2]int) bool {
	return a[0] == b[0] && a[1] == b[1]
}


func testGenerateSubRanges() {

	actual, err := generateSubRanges([2]int{1, 10}, [2]int{1, 10})
	if err != nil {
		fmt.Println("Test 1 Failed", err)
	}
	expected := [2]int{1, 10}
	
	if len(actual) == 1 && compareSubRange(actual[0], expected) {
		fmt.Println("Test 1 Passed")
	} else {
		fmt.Println("Test 1 Failed")
	}

	actual, err = generateSubRanges([2]int{1, 10}, [2]int{1, 5})
	fmt.Println("Actual: ", actual)
	if err != nil {
		fmt.Println("Test 2 Failed", err)
	}
	// expected 1,5 and 6,10
	expected2a := [2]int{1, 5}
	expected2b := [2]int{6, 10}

	if len(actual) == 2 && compareSubRange(actual[0], expected2a) && compareSubRange(actual[1], expected2b) {
		fmt.Println("Test 2 Passed")
	} else {
		fmt.Println("Test 2 Failed")
	}

	actual, err = generateSubRanges([2]int{1, 10}, [2]int{5, 10})
	fmt.Println("Actual: ", actual)
	if err != nil {
		fmt.Println("Test 3 Failed", err)
	}
	// expected 1,4 and 5,10
	expected3a := [2]int{1, 4}
	expected3b := [2]int{5, 10}

	if len(actual) == 2 && compareSubRange(actual[0], expected3a) && compareSubRange(actual[1], expected3b) {
		fmt.Println("Test 3 Passed")
	} else {
		fmt.Println("Test 3 Failed")
	}

	// test map range is a subset of source range
	actual, err = generateSubRanges([2]int{1, 10}, [2]int{5, 6})
	fmt.Println("Actual: ", actual)
	if err != nil {
		fmt.Println("Test 4 Failed", err)
	}
	// expected 1,4 and 5,10
	expected4a := [2]int{1, 4}
	expected4b := [2]int{5, 6}
	expected4c := [2]int{7, 10}

	if len(actual) == 3 && compareSubRange(actual[0], expected4a) && compareSubRange(actual[1], expected4b) && compareSubRange(actual[2], expected4c) {
		fmt.Println("Test 4 Passed")
	} else {
		fmt.Println("Test 4 Failed")
	}

	// test source range is a subset of map range
	actual, err = generateSubRanges([2]int{5, 6}, [2]int{1, 10})
	fmt.Println("Actual: ", actual)
	if err != nil {
		fmt.Println("Test 5 Failed", err)
	}
	if len(actual) == 1 && compareSubRange(actual[0], [2]int{5, 6}) {
		fmt.Println("Test 5 Passed")
	} else {
		fmt.Println("Test 5 Failed")
	}

	// test no overlap
	actual, err = generateSubRanges([2]int{1, 4}, [2]int{5, 10})
	fmt.Println("Actual: ", actual)
	if err != nil {
		fmt.Println("Test 6 Failed", err)
	}
	if len(actual) == 1 && compareSubRange(actual[0], [2]int{1, 4}) {
		fmt.Println("Test 6 Passed")
	} else {
		fmt.Println("Test 6 Failed")
	}

	// test touch at the lower bound
	actual, err = generateSubRanges([2]int{1, 5}, [2]int{5, 10})
	fmt.Println("Actual: ", actual)
	if err != nil {
		fmt.Println("Test 7 Failed", err)
	}
	if len(actual) == 2 && compareSubRange(actual[0], [2]int{1, 4}) && compareSubRange(actual[1], [2]int{5, 5}) {
		fmt.Println("Test 7 Passed")
	} else {
		fmt.Println("Test 7 Failed")
	}

	// test touch at the upper bound
	actual, err = generateSubRanges([2]int{6, 10}, [2]int{1, 6})
	fmt.Println("Actual: ", actual)
	if err != nil {
		fmt.Println("Test 8 Failed", err)
	}
	if len(actual) == 2 && compareSubRange(actual[0], [2]int{6, 6}) && compareSubRange(actual[1], [2]int{7, 10}) {
		fmt.Println("Test 8 Passed")
	} else {
		fmt.Println("Test 8 Failed")
	}
}
	

func preProcess(scanner *bufio.Scanner) ([]int, [][][]int, error) {
    var seeds []int
    var maps [][][]int
    var currentMap [][]int

    for scanner.Scan() {
        line := scanner.Text()
        if line == "" {
            if currentMap != nil {
                maps = append(maps, currentMap)
                currentMap = nil
            }
            continue
        }

        if strings.HasPrefix(line, "seeds:") {
            seedStrs := strings.Fields(line[len("seeds:"):])
            var err error
            seeds, err = strSliceToIntSlice(seedStrs)
            if err != nil {
                return nil, nil, err
            }
        } else if !strings.Contains(line, "map:") {
            nums, err := strSliceToIntSlice(strings.Fields(line))
            if err != nil {
                return nil, nil, err
            }
            currentMap = append(currentMap, nums)
        }
    }
    if currentMap != nil {
        maps = append(maps, currentMap)
    }

    return seeds, maps, scanner.Err()
}


func transformId(id int, sourceRangeStart int, rangeLength int, destinationRangeStart int) int {
	if id >= sourceRangeStart && id < sourceRangeStart + rangeLength {
		return id + (destinationRangeStart - sourceRangeStart)
	}
	return id
}

func idInRange(id int, rangeStart int, rangeLength int) bool {
	return id >= rangeStart && id < rangeStart + rangeLength
}

func problem1(seeds []int, maps [][][]int) int {

	lowestSeed := math.MaxInt64

	for _, seed := range seeds {
		currentId := seed
		for _, m := range maps {
			// fmt.Println("Current Id: ", currentId)
			newCurrentId := currentId
			for _, row := range m {
				destinationRangeStart := row[0]
				sourceRangeStart := row[1]
				rangeLength := row[2]
				if idInRange(currentId, sourceRangeStart, rangeLength) {
					newCurrentId = transformId(currentId, sourceRangeStart, rangeLength, destinationRangeStart)
				}
			}
			currentId = newCurrentId
		}
		if currentId < lowestSeed {
			lowestSeed = currentId
		}
		// fmt.Println("Seed:", seed, "Final Id: ", currentId)
	}

	return lowestSeed
}


func problem2(seeds[]int, maps[][][]int) int {
	// this part is kinda like binary search
	fmt.Println("seeds", seeds)

	subRanges := [][2]int{}

	for i := 0; i < len(seeds); i++ {
		if i%2 == 0 {
			subRanges = append(subRanges, [2]int{seeds[i], seeds[i] + seeds[i+1] - 1})
		}
	}
	fmt.Println("subRanges", subRanges)
	for _, m := range maps {
		newSubRanges := make(map[[2]int]bool)		
		transformedSubRanges := [][2]int{}
		// makes a strong assumption that rules dont overlap each other!!! if they do then this will break, but then 2 seeds can map to multiple locations
		for _, subRange := range subRanges {
			matchedRule := false
			for _, row := range m {
				// this assumes map cant over lap in ranges
				// destinationRangeStart := row[0]
				sourceRangeStart := row[1]
				rangeLength := row[2]

				preProcessSubRanges, err := generateSubRanges(subRange, [2]int{sourceRangeStart, sourceRangeStart + rangeLength - 1})
				if err != nil {
					fmt.Println("Error generating sub ranges", err)
				}

				if len(preProcessSubRanges) <= 1 {
					continue
				} else {
					matchedRule = true
				}

				// fmt.Println("preProcessSubRanges", preProcessSubRanges)

				for _, preProcessSubRange := range preProcessSubRanges {

					// before adding go through all new sub ranges and if there is a sub range that starts at the same location and is longer then remove it
				
					subRangeExists := false

					for sr := range newSubRanges {
						if sr[0] == preProcessSubRange[0] && sr[1] > preProcessSubRange[1] {
							delete(newSubRanges, sr)
						}

						if sr[0] == preProcessSubRange[0] && sr[1] < preProcessSubRange[1] {
							subRangeExists = true
						}
					}

					if !subRangeExists {
						newSubRanges[preProcessSubRange] = true
					}
					

					
				}
			}


			if !matchedRule {
				newSubRanges[subRange] = true
			}



		}

		for subRange := range newSubRanges {
			// fmt.Println("subRange", subRange)
			currentStart := subRange[0]
			currentEnd := subRange[1]

			newStart := currentStart
			newEnd := currentEnd
			for _, row := range m {
				destinationRangeStart := row[0]
				sourceRangeStart := row[1]
				rangeLength := row[2]
				// fmt.Println("newStart, newEnd, sourceRangeStart, rangeLength, destinationRangeStart", newStart, newEnd, sourceRangeStart, rangeLength, destinationRangeStart)

				// they should split so they're always in the same range
				if idInRange(currentStart, sourceRangeStart, rangeLength) && idInRange(currentEnd, sourceRangeStart, rangeLength) {
					newStart = transformId(currentStart, sourceRangeStart, rangeLength, destinationRangeStart)
					newEnd = transformId(currentEnd, sourceRangeStart, rangeLength, destinationRangeStart)
				}

				if idInRange(currentStart, sourceRangeStart, rangeLength) && !idInRange(currentEnd, sourceRangeStart, rangeLength) {
					fmt.Println("Error: currentStart in range but currentEnd not in range", subRange, row)
				}
				if idInRange(currentEnd, sourceRangeStart, rangeLength) && !idInRange(currentStart, sourceRangeStart, rangeLength) {
					fmt.Println("Error: currentEnd in range but currentStart not in range", subRange, row)
				}
			}
			transformedSubRanges = append(transformedSubRanges, [2]int{newStart, newEnd})
		}

		// fmt.Println("transformedSubRanges > subRanges", transformedSubRanges)

		subRanges = transformedSubRanges
	}
	fmt.Println("subRanges", subRanges)
	lowestLocation := math.MaxInt64
	for _, sr := range subRanges {
		if sr[0] < lowestLocation {
			lowestLocation = sr[0]
		}

		if sr[1] < lowestLocation {
			lowestLocation = sr[1]
		}
	}

	return lowestLocation	
}


// func problem2(seeds []int, maps [][][]int) int {
// 	// this part is kinda like binary search
// }

func main() {
	fileName := os.Args[1]
	version := os.Args[2]

	fmt.Println("File Name: ", fileName, version)

	file, err := os.Open(fileName)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close() // defer closing the file

	scanner := bufio.NewScanner(file)
	seeds, maps, err := preProcess(scanner)

	fmt.Println("Seeds: ", seeds)
	// fmt.Println("Maps: ", maps)

	fmt.Println("Answer Problem 1:", problem1(seeds, maps)) //35 on test data
	// testGenerateSubRanges()

	// wrong answer, worked on test, but failed on prod output
	fmt.Println("Answer Problem 2:", problem2(seeds, maps))
	// fmt.Println("Answer Problem 2:", problem2(___))
}

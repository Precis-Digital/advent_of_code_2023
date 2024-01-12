import re
import math
from collections import Counter
from math import gcd


def parse_input(f):
    galaxy_positions = set()

    for r, row in enumerate(f):
        for c, cell in enumerate(row):
            if cell == "#":
                galaxy_positions.add((r, c))
    return galaxy_positions, (r+1, c+1)


def get_pairs(array: list[tuple]):
    N = len(array)
    for i in range(N):
        for j in range(i+1, N):
            yield array[i], array[j]
    
def manhattan_distance(a: tuple[int, int], b: tuple[int, int]):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def problem1(galaxy_positions, shape, expansion_rate=1):
    # print(sorted(list(galaxy_positions)))
    print(shape)
    columns_with_no_galaxy = set(range(shape[1]))
    rows_with_no_galaxy = set(range(shape[0]))

    for r, c in galaxy_positions:
        columns_with_no_galaxy.discard(c)
        rows_with_no_galaxy.discard(r)

    new_galaxy_positions = set()
    for pos in list(galaxy_positions):
        r,c = pos
        number_of_rows_with_no_galaxy_less_than_r = len([r_ for r_ in rows_with_no_galaxy if r_ < r])
        number_of_columns_with_no_galaxy_less_than_c = len([c_ for c_ in columns_with_no_galaxy if c_ < c])
        new_galaxy_positions.add((r + (expansion_rate - 1)*number_of_rows_with_no_galaxy_less_than_r, c + (expansion_rate - 1)*number_of_columns_with_no_galaxy_less_than_c))


    galaxy_positions = new_galaxy_positions
    # print(sorted(list(galaxy_positions)))
    pairs = list(get_pairs(list(galaxy_positions)))
    
    # compute sum of shortest distances
    sum_of_shortest_distances = 0
    for a, b in pairs:
        sum_of_shortest_distances += manhattan_distance(a, b)
        # print(a, b, manhattan_distance(a, b))
    return sum_of_shortest_distances

def problem2(galaxy_positions, shape):
    return problem1(galaxy_positions, shape, expansion_rate=1_000_000)

    

def main(fpath: str):
    with open(fpath, 'r') as f:
        galaxy_positions, shape = parse_input(f)
        

    print('Problem 1: ', problem1(galaxy_positions, shape)) #9545480
    print('Problem 2: ', problem2(galaxy_positions, shape)) # 406725732046
    return 0


if __name__ == '__main__':
    import sys
    fpath = sys.argv[1]
    print("fpath:", fpath)
    main(fpath=fpath)
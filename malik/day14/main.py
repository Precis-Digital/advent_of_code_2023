import re
import math
from collections import Counter
from math import gcd
from functools import cache



def parse_input(f):
    outputs = []

    for r, row in enumerate(f.readlines()):
        row = row.strip()
        for c, cell in enumerate(row):
            if cell != ".": 
                outputs.append((r, c, cell))
    print("Shape:", r+1, c+1)
    return outputs, (r+1, c+1)


def get_movement_vector(direction: str):
    if direction == "N":
        return (-1, 0)
    if direction == "S":
        return (1, 0)
    if direction == "W":
        return (0, -1)
    if direction == "E":
        return (0, 1)
    


def calculate_load_and_new_position(cells: list[tuple[int, int, str]], shape: tuple[int], direction: str):
    group_idx = 1 if direction in ("N", "S") else 0
    reverse = -1 if direction in ("S", "E") else 1

    cells_sorted_by_column = sorted(cells, key=lambda x: (x[group_idx], x[1 - group_idx]))[::reverse]

    columns = {} 
    for cell in cells_sorted_by_column:
        columns.setdefault(cell[group_idx], []).append(cell)


    # print(columns)

    max_load = shape[0] if direction in ("N", "S") else shape[1]
    # print("max_load:", max_load)

    total_load = 0
    new_positions = []

    for idx in sorted(columns.keys()):
        column = columns[idx]
        load = max_load
        # print(idx, column)
        for idx, cell in enumerate(column):
            # print(load, cell)
            if cell[2] == "O":
                total_load += load
                if direction in ("N"):
                    new_positions.append((max_load - load, cell[1], cell[2]))
                elif direction in ("S"):
                    new_positions.append((load - 1, cell[1], cell[2]))
                elif direction in ("W"):
                    new_positions.append((cell[0], max_load - load, cell[2]))
                elif direction in ("E"):
                    new_positions.append((cell[0], load - 1, cell[2]))
                load -= 1
            if cell[2] == "#":
                new_positions.append((cell[0], cell[1], cell[2]))
                # the load for the next rock is equivalent to the "load" for the block -1
                if direction in ("N", "W"):
                    load = max_load - cell[1- group_idx] - 1
                else:
                    load = cell[1- group_idx]
    return total_load, new_positions



def visualize(cells: list[tuple[int, int, str]], shape: tuple[int]):
    grid = [["." for _ in range(shape[1])] for _ in range(shape[0])]
    for cell in cells:
        grid[cell[0]][cell[1]] = cell[2]
    for row in grid:
        print("".join(row))
    print("")


def problem1(cells, shape):
    load, _ = calculate_load_and_new_position(cells=cells, shape=shape, direction="N")
    return load


        


def find_longest_cycle(observations: list[tuple]) -> tuple[int, int]:
    """
    takes an array of observations and returns the longest cycle length and the index of the first observation in the cycle
    """



    for i in range(len(observations)):
        for j in range(i+1, len(observations)):
            if observations[i] == observations[j]:
                return j - i, i


def problem2(cells, shape):


    
    def calc_north_load(positions_: list[tuple[int, int, str]], shape_: tuple[int]):
        total_load = 0
        max_load = shape_[0]
        load = max_load
        for cell in positions_:
            if cell[2] == "O":
                total_load += max_load - cell[0]
        return total_load

    print("init visualization ==========")
    visualize(cells, shape)

    

    
    positions = cells

    north_loads = []
    load_coords = []

    # sample the data for 1000 spins
    print("sampling")
    for ii in range(1000):
        if ii % 80 == 0:
            print("sampling", ii)
        loads = []
        for direction in ["N", "W", "S", "E"]:
            load, positions = calculate_load_and_new_position(cells=positions, shape=shape, direction=direction)
            loads.append(load)
            # print(direction, calc_north_load(positions, shape))
            # visualize(positions, shape)
        # print("===========")
        north_load = calc_north_load(positions, shape)
        north_loads.append(north_load)
        load_coords.append(tuple(loads))
        # print("north_load:", north_load, len([p for p in positions if p[2] == "O"]))
        # print(loads)
        # visualize(positions, shape)
        
    print("calculating cycle data")
    cycle_length, start = find_longest_cycle(observations=load_coords)
    print("cycle_length:", cycle_length, "start:", start)
    north_load_cycle = north_loads[start:(start + cycle_length)]
    print("cycle",   north_load_cycle)
    # expected after 65 for 7
    return north_load_cycle[(1000000000 - 1- start)%cycle_length]



def main(fpath: str):
    with open(fpath, 'r') as f:
        cells, shape = parse_input(f)
        
    # print('Problem 1: ', problem1(cells, shape)) #109833
    print('Problem 2: ', problem2(cells, shape))  
    return 0


if __name__ == '__main__':
    import sys
    fpath = sys.argv[1]
    print("fpath:", fpath)
    main(fpath=fpath)
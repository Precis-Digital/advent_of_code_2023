import re
import math
from collections import Counter
from math import gcd
from functools import cache




def parse_input(f):
    # print(f.read().strip())
    # pass

    items = {}
    for r, row in enumerate(f):
        row = row.strip()
        for c, cell in enumerate(row):
            if cell != ".":
                items[(r, c)] = cell
    return items, (r + 1, c + 1)

def print_visited_tiles(visited_tiles, shape, items):
    for r in range(shape[0]):
        for c in range(shape[1]):
            if (r, c) in items:
                print(items[(r, c)], end="")
            elif (r, c) in visited_tiles:
                print("X", end="")
            else:
                print(".", end="")
        print()


def problem1(input_, init_beam = ((0, 0), (0, 1))):
    items, shape = input_
    active_beams = []
    active_beams.append(init_beam)
    visited_beams = set()
    visited_tiles = set()
    i = 0
    while active_beams:
        if i % 1000 == 0 and i > 0:
            print(i, len(active_beams), len(visited_tiles))
            # print_visited_tiles(visited_tiles, shape, items)
        i += 1
        beam_pos, beam_dir = active_beams.pop()
        if (beam_pos, beam_dir) in visited_beams:
            continue
        if beam_pos[0] < 0 or beam_pos[0] >= shape[0] or beam_pos[1] < 0 or beam_pos[1] >= shape[1]:
            continue
        # print(beam_pos, beam_dir)
        visited_tiles.add(beam_pos)
        visited_beams.add((beam_pos, beam_dir))
        item = items.get(beam_pos, None)
        if item == "/":
            x,y = beam_dir
            new_beam_dir = (-y, -x)
            new_beam_pos = (beam_pos[0] + new_beam_dir[0], beam_pos[1] + new_beam_dir[1])
            active_beams.append((new_beam_pos, new_beam_dir))
        elif item == "\\":
            x,y = beam_dir
            new_beam_dir = (y, x)
            new_beam_pos = (beam_pos[0] + new_beam_dir[0], beam_pos[1] + new_beam_dir[1])
            active_beams.append((new_beam_pos, new_beam_dir))
        elif item == "|" and beam_dir[1] != 0:
            new_beam_dir_1 = (-1, 0)
            new_beam_dir_2 = (1, 0)
            new_beam_pos_1 = (beam_pos[0] + new_beam_dir_1[0], beam_pos[1] + new_beam_dir_1[1])
            new_beam_pos_2 = (beam_pos[0] + new_beam_dir_2[0], beam_pos[1] + new_beam_dir_2[1])
            active_beams.append((new_beam_pos_1, new_beam_dir_1))
            active_beams.append((new_beam_pos_2, new_beam_dir_2))
        elif item == "-" and beam_dir[0] != 0:
            new_beam_dir_1 = (0, -1)
            new_beam_dir_2 = (0, 1)
            new_beam_pos_1 = (beam_pos[0] + new_beam_dir_1[0], beam_pos[1] + new_beam_dir_1[1])
            new_beam_pos_2 = (beam_pos[0] + new_beam_dir_2[0], beam_pos[1] + new_beam_dir_2[1])
            active_beams.append((new_beam_pos_1, new_beam_dir_1))
            active_beams.append((new_beam_pos_2, new_beam_dir_2))
        else:
            new_beam_pos = (beam_pos[0] + beam_dir[0], beam_pos[1] + beam_dir[1])
            active_beams.append((new_beam_pos, beam_dir))

    # print_visited_tiles(visited_tiles, shape, items)
    return len(visited_tiles)



def problem2(input_):
    items, shape = input_

    max_tiles = 0

    for c in range(shape[1]):
        init_beam = ((0, c), (1, 0))
        visited_tiles = problem1(input_, init_beam)
        max_tiles = max(max_tiles, visited_tiles)

        init_beam = ((shape[0] - 1, c), (-1, 0))
        visited_tiles = problem1(input_, init_beam)
        max_tiles = max(max_tiles, visited_tiles)
    
    for r in range(shape[0]):
        init_beam = ((r, 0), (0, 1))
        visited_tiles = problem1(input_, init_beam)
        max_tiles = max(max_tiles, visited_tiles)

        init_beam = ((r, shape[1] - 1), (0, -1))
        visited_tiles = problem1(input_, init_beam)
        max_tiles = max(max_tiles, visited_tiles)

    return max_tiles

def main(fpath: str):
    with open(fpath, 'r') as f:
        input_ = parse_input(f)
    
    _, shape = input_
    print("shape", shape, "area", shape[0] * shape[1])

    print('Problem 1: ', problem1(input_))  #8116
    print('Problem 2: ', problem2(input_))  
    return 0


if __name__ == '__main__':
    import sys
    fpath = sys.argv[1]
    print("fpath:", fpath)
    main(fpath=fpath)
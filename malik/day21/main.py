


from __future__ import annotations

import re
import math
from collections import Counter, deque
from math import gcd
from functools import cache
import heapq
from dataclasses import dataclass, asdict, field

from enum import Enum


def get_neighbors(node, walls, shape):
    for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        neighbor = (node[0] + direction[0], node[1] + direction[1])
        if neighbor not in walls and 0 <= neighbor[0] < shape[0] and 0 <= neighbor[1] < shape[1]:
            yield neighbor


def print_graph(walls, shape, visited_nodes_with_distances):
    for r in range(shape[0]):
        for c in range(shape[1]):
            if (r, c) in walls:
                print("#", end="")
            elif (r, c) in visited_nodes_with_distances:
                print(visited_nodes_with_distances[(r, c)], end="")
            else:
                print(".", end="")
        print()


def parse_input(f):
    walls = set()
    start_node = None
    for r, row in enumerate(f):
        row = row.strip()
        for c, cell in enumerate(row):
            if cell == "S":
                start_node = (r, c)
            elif cell == "#":
                walls.add((r, c))
    return walls, start_node, (r + 1, c + 1)
            

def problem1(input_):
    walls, start_node, shape = input_
    print(walls)
    print(start_node)
    print(shape)
    max_steps = 64
    MAX_DISTANCE = 100000000

    min_distances = {
        start_node: 0
    }
    queue = []
    heapq.heappush(queue, (0, start_node))
    visited = set()

    while queue:
        distance, node = heapq.heappop(queue)
        print(distance, node, min_distances.get(node, MAX_DISTANCE))
        if node in visited:
            continue
        visited.add(node)

        if distance == max_steps:
            continue

        for neighbor in get_neighbors(node, walls, shape):
            d = min_distances.get(node, MAX_DISTANCE)
            new_distance_to_neighbor = d + 1
            current_min_distance_to_neighbor = min_distances.get(neighbor, MAX_DISTANCE)
            if new_distance_to_neighbor < current_min_distance_to_neighbor:
                min_distances[neighbor] = new_distance_to_neighbor
            if neighbor not in visited:
                heapq.heappush(queue, (new_distance_to_neighbor, neighbor))

    print(visited)
    print(len(visited))

    print_graph(walls, shape, min_distances)

    count_of_nodes = 0
    for node, distance in min_distances.items():
        if (max_steps - distance) % 2 == 0:
            count_of_nodes += 1
    return count_of_nodes

def problem2(input_):
    pass

def main(fpath: str):
    def get_input():
        with open(fpath, 'r') as f:
            input_ = parse_input(f)
            return input_

    print('Problem 1: ', problem1(get_input()))
    print('Problem 2: ', problem2(get_input()))
    return 0


if __name__ == '__main__':
    import sys
    fpath = sys.argv[1]
    print("fpath:", fpath)
    main(fpath=fpath)


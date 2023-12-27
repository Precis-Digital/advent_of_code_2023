import re
import math
from collections import Counter
from math import gcd
from functools import cache
import heapq




def parse_input(f):
    grid = []
    for row in f:
        row = row.strip()
        grid.append(list(map(int, row)))
            
    return grid, (len(grid), len(grid[0]))



def get_neighbors(node, shape):

    pos, direction, steps_in_direction = node

    candidate_positions = [] 
    for new_direction in [(0,1), (1, 0), (-1, 0), (0, -1)]:
        new_pos = (pos[0] + new_direction[0], pos[1] + new_direction[1])
        if new_direction == direction:
            new_steps_in_direction = steps_in_direction + 1
        else:
            new_steps_in_direction = 1

        # cant go over the edge
        if new_pos[0] < 0 or new_pos[0] >= shape[0] or new_pos[1] < 0 or new_pos[1] >= shape[1]:
            continue

        # cant go backwards
        if new_direction == (-direction[0], -direction[1]):
            continue

        # cant go more than 3 steps in one direction
        if new_steps_in_direction > 3:
            continue

        candidate_positions.append((new_pos, new_direction, new_steps_in_direction))

    return candidate_positions


def test_get_neighbors():
    shape = (4, 4)
    node = ((1,1), (0, 1), 1)
    print("node:", node, "shape:", shape, "neighbors:", get_neighbors(node=node, shape=shape))

    node = ((1,1), (1, 0), 1)
    print("node:", node, "shape:", shape, "neighbors:", get_neighbors(node=node, shape=shape))

    node = ((1,1), (0, 1), 2)
    print("node:", node, "shape:", shape, "neighbors:", get_neighbors(node=node, shape=shape))

    node = ((1,1), (0, 1), 3)
    print("node:", node, "shape:", shape, "neighbors:", get_neighbors(node=node, shape=shape))

def djikstras(grid, shape):

    # the node should be a tuple of (position, direction, number_of_steps_in_this_direction)
    
    # the start node starts at the origin and goes right
    start_pos = ((0,0), (0, 1), 1)

    default_distance = 100000000
    dist = {}
    dist[start_pos] = 0

    heap = []
    heapq.heappush(heap, (0, start_pos))
    
    visited = set()

    # run until you've visited all nodes
    while True:
        if len(visited) % 1000 == 0 and len(visited) > 0:
            print(len(visited), len(dist))
        # node = min((d for d in dist if d not in visited), key=dist.get)
        node = heapq.heappop(heap)[1]
        # print("node:", node)
        if node[0] == (shape[0] - 1, shape[1] - 1):
            return dist[node]
        if node in visited:
            continue
        for neighbor in get_neighbors(node, shape):
            neighbor_pos, _, _ = neighbor
            cost = dist[node]
            new_cost = cost + grid[neighbor_pos[0]][neighbor_pos[1]]
            if new_cost < dist.get(neighbor, default_distance):
                dist[neighbor] = new_cost
            
            heapq.heappush(heap, (new_cost, neighbor))

        visited.add(node)
    
        # update cost in heap for all items
        # heap = [(dist.get(path[-1], default_distance), path) for (cost, path) in heap]


def problem1(input_):
    grid, shape = input_
    return djikstras(grid=grid, shape=shape)

def problem2(input_):
    pass

def main(fpath: str):
    with open(fpath, 'r') as f:
        input_ = parse_input(f)
        grid, shape = input_
        print("shape:", shape)  

    test_get_neighbors()
    print('Problem 1: ', problem1(input_))  #8116
    # print('Problem 2: ', problem2(input_))  
    return 0


if __name__ == '__main__':
    import sys
    fpath = sys.argv[1]
    print("fpath:", fpath)
    main(fpath=fpath)
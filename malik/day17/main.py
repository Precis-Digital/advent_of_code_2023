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


def get_neighbors_ultra_crucible(node, shape):
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
            # print("going backwards")
            continue

        # cant go more than 10 steps in one direction
        if new_steps_in_direction > 10:
            # print("too many steps")
            continue

        # ultra crucible must move minmum of 4 steps in a direction
        if steps_in_direction < 4 and new_direction != direction:
            # print("not enough steps")
            continue

        # if starting a new direction, check to see if you will go over the edge
        if new_direction != direction:
            min_pos_r = pos[0] + 4 * new_direction[0]
            min_pos_c = pos[1] + 4 * new_direction[1]
            if min_pos_r < 0 or min_pos_r >= shape[0] or min_pos_c < 0 or min_pos_c >= shape[1]:
                # print("going over the edge")
                continue
            # print("skipped")

        # print("appending", new_pos, new_direction, new_steps_in_direction)
        candidate_positions.append((new_pos, new_direction, new_steps_in_direction))

    return candidate_positions


def test_get_neighbors():
    shape = (4, 4)
    node = ((1,1), (0, 1), 1)
    print("node:", node, "shape:", shape, "neighbors:", get_neighbors(node=node, shape=shape))
    print("ultra", "node:", node, "shape:", shape, "neighbors:", get_neighbors_ultra_crucible(node=node, shape=shape))

    node = ((1,1), (1, 0), 1)
    print("node:", node, "shape:", shape, "neighbors:", get_neighbors(node=node, shape=shape))
    print("ultra", "node:", node, "shape:", shape, "neighbors:", get_neighbors_ultra_crucible(node=node, shape=shape))
    
    node = ((1,1), (0, 1), 2)
    print("node:", node, "shape:", shape, "neighbors:", get_neighbors(node=node, shape=shape))
    print("ultra", "node:", node, "shape:", shape, "neighbors:", get_neighbors_ultra_crucible(node=node, shape=shape))
    
    node = ((1,1), (0, 1), 3)
    print("node:", node, "shape:", shape, "neighbors:", get_neighbors(node=node, shape=shape))
    print("ultra", "node:", node, "shape:", shape, "neighbors:", get_neighbors_ultra_crucible(node=node, shape=shape))
    
    print("=====================================")
    node = ((1,1), (0, 1), 4)
    shape = (10, 10)
    print("ultra", "node:", node, "shape:", shape, "neighbors:", get_neighbors_ultra_crucible(node=node, shape=shape))

    print("=====================================")
    node = ((1,1), (0, 1), 9)
    shape = (10, 10)
    print("ultra", "node:", node, "shape:", shape, "neighbors:", get_neighbors_ultra_crucible(node=node, shape=shape))

    print("=====================================")
    node = ((1,1), (0, 1), 10)
    shape = (10, 10)
    
    print("ultra", "node:", node, "shape:", shape, "neighbors:", get_neighbors_ultra_crucible(node=node, shape=shape))

def djikstras(grid, shape, neighbors_function):

    # the node should be a tuple of (position, direction, number_of_steps_in_this_direction)
    
    # the start node starts at the origin and goes right

    # spent 2 hours not realizing it can move right or down... just assumed right
    start_pos1 = ((0,0), (0, 1), 1)
    start_pos2 = ((0,0), (1, 0), 1)

    default_distance = 100000000
    dist = {}
    dist[start_pos1] = 0
    dist[start_pos2] = 0


    heap = []
    heapq.heappush(heap, (dist[start_pos1], start_pos1))
    heapq.heappush(heap, (dist[start_pos2], start_pos2))
    
    visited = set()

    # run until you've visited all nodes
    while heap:
        if len(visited) % 100000 == 0:
            print(len(visited), len(dist))
        # node = min((d for d in dist if d not in visited), key=dist.get)
        cost, node = heapq.heappop(heap)
        # print("node:", node)
        if node[0] == (shape[0] - 1, shape[1] - 1):
            print(">>>>>", dist[node], node)
        if node in visited:
            continue
        visited.add(node)

        for neighbor in neighbors_function(node, shape):
            # if node[2] < 4:
            #     assert neighbor[2] == node[2] + 1
            #     # print(node, "neighbor:", neighbor)

            # if node[2] == 10:
            #     assert neighbor[2] == 1
            neighbor_pos, _, _ = neighbor
            new_cost = cost + grid[neighbor_pos[0]][neighbor_pos[1]]
            if new_cost < dist.get(neighbor, default_distance):
                dist[neighbor] = new_cost
            
            heapq.heappush(heap, (new_cost, neighbor))
        

    


def problem1(input_):
    grid, shape = input_
    return djikstras(grid=grid, shape=shape, neighbors_function=get_neighbors)

def problem2(input_):
    grid, shape = input_
    return djikstras(grid=grid, shape=shape, neighbors_function=get_neighbors_ultra_crucible)

def main(fpath: str):
    with open(fpath, 'r') as f:
        input_ = parse_input(f)
        grid, shape = input_
        print("shape:", shape)  

    test_get_neighbors()
    # print('Problem 1: ', problem1(input_))  # 668
    print('Problem 2: ', problem2(input_))  # 789 (is too high)
    return 0


if __name__ == '__main__':
    import sys
    fpath = sys.argv[1]
    print("fpath:", fpath)
    main(fpath=fpath)
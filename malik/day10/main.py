import re
import math
from collections import Counter
from math import gcd


def parse_input(f):
    graph = {}
    starting_position = None
    for r, row in enumerate(f):
        for c, cell in enumerate(row):
            if cell == '.':
                continue
            elif cell == '|':
                graph[(r, c)] = [(r-1, c), (r+1, c)]
            elif cell == '-':
                graph[(r, c)] = [(r, c-1), (r, c+1)]
            elif cell == '7':
                graph[(r, c)] = [(r, c-1), (r+1, c)]
            elif cell == "J":
                graph[(r, c)] = [(r, c-1), (r-1, c)]
            elif cell == "L":
                graph[(r, c)] = [(r, c+1), (r-1, c)]
            elif cell == "F":
                graph[(r, c)] = [(r, c+1), (r+1, c)]
            elif cell == "S":
                starting_position = (r, c)
                graph[starting_position] = []

    # connect starting node to the graph
    for candidate_node in [(starting_position[0] - 1, starting_position[1]), (starting_position[0] + 1, starting_position[1]), (starting_position[0], starting_position[1] - 1), (starting_position[0], starting_position[1] + 1)]:
        if candidate_node in graph:
            if starting_position in graph[candidate_node]:
                graph[starting_position].append(candidate_node)
    return graph, starting_position
        
def problem1(graph, starting_pos):
    print(graph)
    print(starting_pos)

    # implemet breadth first search to determine distance from starting position to all other nodes
    
    furthest_distance = 0
    nodes = [(starting_pos, 0)]
    visited = set()
    while nodes:
        node, distance = nodes.pop(0)
        if distance > furthest_distance:
            furthest_distance = distance
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                nodes.append((neighbor, distance + 1))
    return furthest_distance


def problem2():
    pass

    


def main(fpath: str):
    with open(fpath, 'r') as f:
        graph, starting_pos = parse_input(f)
        

    print('Problem 1: ', problem1(graph, starting_pos))
    print('Problem 2: ', problem2())
    return 0


if __name__ == '__main__':
    import sys
    fpath = sys.argv[1]
    print("fpath:", fpath)
    main(fpath=fpath)
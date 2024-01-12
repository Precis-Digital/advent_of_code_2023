import re
import math
from collections import Counter
from math import gcd


def parse_input(f):
    graph = {}
    land_points = set()
    starting_position = None
    for r, row in enumerate(f):
        for c, cell in enumerate(row):
            if cell == '.':
                land_points.add((r, c))
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
    return graph, starting_position, land_points, (r, c)


def bfs(graph, starting_pos)  -> (int, set[tuple[int, int]]):
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
    return furthest_distance, visited


def is_vertical_node(node, graph):
    return graph[node] != [(node[0], node[1] -1), (node[0], node[1] + 1)]

def is_horizontal_node(node, graph):
    return graph[node] != [(node[0] - 1, node[1]), (node[0] + 1, node[1])]

def is_L_node(node, graph):
    return graph[node] ==[(node[0], node[1] + 1), (node[0] - 1, node[1])]

def is_7_node(node, graph):
    return graph[node] ==[(node[0], node[1] - 1), (node[0] + 1, node[1])]

def problem1(graph, starting_pos):

    # implemet breadth first search to determine distance from starting position to all other nodes

    furthest_distance, _ = bfs(graph, starting_pos)
    return furthest_distance


def problem2(graph, starting_pos, land_points, shape):
# """
#     TODO, check the case for 5,5 in the example input
#     But you have it mostly right, you just need to adjust the edge code to include any point not in the graph
# """

    _, visited = bfs(graph, starting_pos)

    num_enclosed = 0
    for point in sorted(list(land_points) + [node for node in graph if node not in visited]):

        # move diagonally to the bottom right from the starting position until you hit the wall

        r,c = point
        intersection_count = 0
        while r <= shape[0] and c <= shape[1]:
            node = (r, c)
            if node in visited:
                # if the point of intersection is a corner, but both edges of the corner are above or below the ray then it should count
                if is_7_node(node, graph) or is_L_node(node, graph):
                    pass
                else:
                    intersection_count += 1
            r += 1
            c += 1

        if intersection_count % 2 == 1:
            num_enclosed += 1

        # print(point, intersection_count)

        # intersections_right = len(list(filter(lambda x : x[0] == point[0] and x[1] > point[1], edges)))
        # intersections_left = len(list(filter(lambda x : x[0] == point[0] and x[1] < point[1], edges)))
        # print(point, intersections_left, intersections_right)
        
        # if intersections_right == 0 or intersections_left == 0:
        #     continue
        # if intersections_right % 2 == 1 or intersections_left % 2 == 1:
            
        #     num_enclosed += 1
    return num_enclosed

    


def main(fpath: str):
    with open(fpath, 'r') as f:
        graph, starting_pos, land_points, shape = parse_input(f)
        

    print('Problem 1: ', problem1(graph, starting_pos))
    print('Problem 2: ', problem2(graph, starting_pos, land_points, shape))
    return 0


if __name__ == '__main__':
    import sys
    fpath = sys.argv[1]
    print("fpath:", fpath)
    main(fpath=fpath)
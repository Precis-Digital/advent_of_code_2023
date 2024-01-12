import re
import math
from collections import Counter
from math import gcd
from functools import cache
import heapq



def parse_input(f):
    output = []
    pattern = re.compile(r'(R|L|U|D) (\d+) \(([\#a-z0-9]+)\)')
    for row in f:
        row = row.strip()
        matches = re.match(pattern=pattern, string=row)
        if matches:
            direction, distance, name = matches.groups()
            row = (direction, int(distance), name)
            output.append(row)
        else:
            # print("row:", row)
            raise ValueError("row did not match pattern")
    return output


def draw_coordinates(coordinates, shape, interior_coordinate=[]):
    grid = [['.' for _ in range(shape[1])] for _ in range(shape[0])]
    for coordinate in coordinates:
        grid[coordinate[0]][coordinate[1]] = '#'
    for coordinate in interior_coordinate:
        grid[coordinate[0]][coordinate[1]] = '*'
    for row in grid:
        print(''.join(row))


def fill_polygon(coordinates, shape, start_coordinate):
    unvisited = set([start_coordinate])
    visited = set(coordinates)
    while unvisited:
        coordinate = unvisited.pop()
        visited.add(coordinate)
        for (dx, dy) in [(xx, yy) for xx in [-1, 0, 1] for yy in [-1, 0, 1]]:
            neighbor = (coordinate[0] + dx, coordinate[1] + dy)
            # print("neighbor:", neighbor)
            if neighbor not in visited:
                unvisited.add(neighbor)
    return visited

def find_coordinate_in_perimeter(coordinates, shape) -> tuple[int, int]:
    """
    find a row where there's an even number of coordinates and none are adjacent
    then the point must lie between those 2 coordinates
    """

    mem = {}

    for coordinate in coordinates:
        row, column = coordinate
        mem.setdefault(row, [])
        mem[row].append(column)    
    # print(mem)
    for row, columns in mem.items():
        if len(columns) % 2 == 0:
            columns.sort()
            for i in range(1, len(columns)):
                if columns[i] - columns[i-1] > 1:
                    return (row, columns[i-1] + 1)


def calculate_center_of_mass(coordinates):
    """
    https://en.wikipedia.org/wiki/Center_of_mass
    """
    x = sum([coordinate[0] for coordinate in coordinates])
    y = sum([coordinate[1] for coordinate in coordinates])
    return (x / len(coordinates), y / len(coordinates))

def sort_counterclockwise(points):
    
    # Step 1: Find the center
    mean_x, mean_y = calculate_center_of_mass(points)
    
    def angle_from_mean(point):
        return math.atan2(point[1] - mean_y, point[0] - mean_x)

    # Step 3: Sort the points by the angle
    points_sorted = sorted(points, key=angle_from_mean)
    return points_sorted

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def grid_corners(upper_left_point: tuple[int, int], in_direction: str, out_direction: str) -> list[tuple[int, int]]:
    """
    Given the upper left point of a grid, return the coordinates of the 4 corners
    """
    upper_right_point = (upper_left_point[0], upper_left_point[1] + 1)
    lower_left_point = (upper_left_point[0] + 1, upper_left_point[1])
    lower_right_point = (upper_left_point[0] + 1, upper_left_point[1] + 1)
    if (in_direction, out_direction) in set([('R', 'D'), ('D', 'R'), ('L', 'U'), ('U', 'L')]):
        return [upper_right_point, lower_left_point]
    return [
        upper_left_point, lower_right_point
    ]

def shoelace_algorithm(coordinates):
    """
    https://en.wikipedia.org/wiki/Shoelace_formula
    """

    # the coordinates are already sorted...
    counter_clockwise_coordinates = coordinates
    x = [coordinate[0] for coordinate in counter_clockwise_coordinates]
    y = [coordinate[1] for coordinate in counter_clockwise_coordinates]
    
    # perimiter use the l2 distance
    perimeter = sum([math.sqrt((x[i] - x[i+1])**2 + (y[i] - y[i+1])**2) for i in range(len(counter_clockwise_coordinates) - 1)])
    print("perimeter:", perimeter)
    return 0.5 * abs(sum([x[i] * y[i+1] - x[i+1] * y[i] for i in range(len(counter_clockwise_coordinates) - 1)]))

def find_border(coordinates, shape, in_graph, out_graph):
    center_of_mass = calculate_center_of_mass(coordinates)
    print("center_of_mass:", center_of_mass)
    border = []
    for idx, coordinate in enumerate(coordinates):
        in_direction = in_graph[coordinate][1]
        out_direction = out_graph[coordinate][1]
        corners = grid_corners(coordinate, in_direction, out_direction)
        if not border:
            # this is essentially a guess since there are some edge cases where this doesn't work
            corner_furtherst_from_center = max(corners, key=lambda x: distance(x, center_of_mass))
            print("corner_furtherst_from_center:", corner_furtherst_from_center)
            border.append(corner_furtherst_from_center)
        else:
            prior_border = border[-1]
            prior_border_x, prior_border_y = prior_border
            if in_direction in ('R', 'L'):
                new_border = next(filter(lambda x: x[0] == prior_border_x, corners))
                border.append(new_border)
            else:
                new_border = next(filter(lambda x: x[1] == prior_border_y, corners))
                border.append(new_border)
    return border

def test_shoelace_algorithm():
    A = [2,7]
    B = [10,1]
    C = [8,6]
    D = [11,7]
    E = [7,10]
    #Define a polygon as being a list of vertices, (on anticlockwise order)
    polygon = list(map(tuple, [A,B,C,D,E]))
    print(shoelace_algorithm(polygon))

def problem1(input_):
    rows = input_
    total_perimeter = sum([row[1] for row in rows])
    print("total_perimeter:", total_perimeter)

    coordinates = [(0,0)]

    for row in rows:
        direction, distance, name = row
        if direction == 'R':
            for i in range(distance):
                coordinates.append((coordinates[-1][0], coordinates[-1][1] + 1))
        elif direction == 'L':
            for i in range(distance):
                coordinates.append((coordinates[-1][0], coordinates[-1][1] - 1))
        elif direction == 'U':
            for i in range(distance):
                coordinates.append((coordinates[-1][0] - 1, coordinates[-1][1]))
        elif direction == 'D':
            for i in range(distance):
                coordinates.append((coordinates[-1][0] + 1, coordinates[-1][1]))
        else:
            raise ValueError("direction not recognized")
    
    min_x = min([coordinate[0] for coordinate in coordinates])
    max_x = max([coordinate[0] for coordinate in coordinates])
    min_y = min([coordinate[1] for coordinate in coordinates])
    max_y = max([coordinate[1] for coordinate in coordinates])

    def shift_coordinates(coordinate):
        return (coordinate[0] - min_x, coordinate[1] - min_y)
    
    coordinates = list(map(shift_coordinates, coordinates))

    shape = shift_coordinates((max_x + 1, max_y + 1))

    interior_coordinate = find_coordinate_in_perimeter(coordinates, shape)
    print("interior_coordinate:", interior_coordinate)
    all_visited_cells = fill_polygon(coordinates, shape, interior_coordinate)
    print("all_visited_cells:", )

    draw_coordinates(coordinates, shape, list(all_visited_cells.difference(coordinates)))
    # sorted_coordinates = sorted(coordinates, key=lambda x: (x[1], x[0]))
    # print("sorted_coordinates:", sorted_coordinates)
    # print(coordinates)
    return len(all_visited_cells)


def solution(rows: list[tuple[str, int, str]]):

    out_graph = {} # from_coordinate -> (to_coordinate, direction)
    in_graph = {} # to_coordinate -> (from_coordinate, direction)
    coordinates = [(0,0)]
    from_coordinate = (0,0)


    base_distance  = 0
    for row in rows:
        direction, distance, name = row
        base_distance += distance
        print("direction:", direction, distance, name)
        if direction == 'R':
            to_coordinate = (from_coordinate[0], from_coordinate[1] + distance )
            out_graph[from_coordinate] = (to_coordinate, direction)
            in_graph[to_coordinate] = (from_coordinate, direction)
            coordinates.append(to_coordinate)
        elif direction == 'L':
            to_coordinate = (from_coordinate[0], from_coordinate[1] - distance )
            out_graph[from_coordinate] = (to_coordinate, direction)
            in_graph[to_coordinate] = (from_coordinate, direction)
            coordinates.append(to_coordinate)
        elif direction == 'U':
            to_coordinate = (from_coordinate[0] - distance, from_coordinate[1])
            out_graph[from_coordinate] = (to_coordinate, direction)
            in_graph[to_coordinate] = (from_coordinate, direction)
            coordinates.append(to_coordinate)
        elif direction == 'D':
            to_coordinate = (from_coordinate[0] + distance, from_coordinate[1])
            out_graph[from_coordinate] = (to_coordinate, direction)
            in_graph[to_coordinate] = (from_coordinate, direction)
            coordinates.append(to_coordinate)
        else:
            raise ValueError("direction not recognized")
        
        from_coordinate = to_coordinate
        

    outer_border = find_border(coordinates, (0,0), in_graph=in_graph, out_graph=out_graph)
    return shoelace_algorithm(outer_border)

def problem1_shoelace_algorithm(input_):
    rows = input_
    total_perimeter = sum([row[1] for row in rows])
    print("total_perimeter:", total_perimeter)
    return solution(rows)



def problem2(input_):
    rows = input_
    new_rows = []
    for row in rows: 
        _, _, hex_color = row
        direction_code = int(hex_color[-1])
        hex_color = hex_color[1:-1]
        distance = int(hex_color, 16)
        direction = None
        if direction_code == 0:
            direction = 'R'
        elif direction_code == 1:
            direction = 'D'
        elif direction_code == 2:
            direction = 'L'
        elif direction_code == 3:
            direction = 'U'
        new_rows.append((direction, distance, ""))
    
    return solution(new_rows)

    

def main(fpath: str):
    with open(fpath, 'r') as f:
        input_ = parse_input(f)

    test_shoelace_algorithm()

    print('Problem 1: ', problem1_shoelace_algorithm(input_))  
    print('Problem 2: ', problem2(input_))
    return 0


if __name__ == '__main__':
    import sys
    fpath = sys.argv[1]
    print("fpath:", fpath)
    main(fpath=fpath)
import re
import math
from collections import Counter
from math import gcd

def lcm(a, b):
    """Calculate the least common multiple of two integers a and b."""
    return abs(a*b) // gcd(a, b)

def lcm_set(numbers):
    """Calculate the LCM of a set of numbers."""
    current_lcm = numbers[0]
    for number in numbers[1:]:
        current_lcm = lcm(current_lcm, number)
    return current_lcm


def parse_input(f):
    instructions = f.readline().strip()
    graph = {}
    f.readline()
    for row in f:
        # sample string "AAA = (BBB, CCC)"
        matches = re.findall(r'\w\w\w', row)
        graph[matches[0]] = (matches[1], matches[2])
    return instructions, graph

def problem1(instructions, graph, starting_node_filter = lambda x: x == 'AAA', ending_node_filter = lambda x: x == 'ZZZ'):
    # starting_node = 'AAA'
    # ending_node = 'ZZZ'

    current_nodes = [node for node in filter(starting_node_filter, graph)]
    print(current_nodes)
    steps = 0
    number_of_instructions = len(instructions)
    while True:

        # if steps % 100000 == 0 :
        #     print(f"step {steps}", current_nodes)
        
        if all(ending_node_filter(node) for node in current_nodes):
            # print(current_nodes)
            return steps
        instruction = instructions[steps % number_of_instructions]
        instruction_index = 1 if instruction == 'R' else 0
        for i in range(len(current_nodes)):
            current_nodes[i] = graph[current_nodes[i]][instruction_index]
        
        steps += 1

        if steps > 1000000000:
            print("breaking after 1000 steps")
            break


def problem2(instructions, graph):
    starting_nodes = [node for node in filter(lambda x: x.endswith('A'), graph)]
    shortest_paths = []
    for node in starting_nodes:
        shortest_path = problem1(instructions, graph, starting_node_filter = lambda x: x == node, ending_node_filter = lambda x: x.endswith('Z'))
        shortest_paths.append(shortest_path)

    return lcm_set(shortest_paths)

    


def main(fpath: str):
    with open(fpath, 'r') as f:
        instructions, graph = parse_input(f)

    print('Problem 1: ', problem1(instructions, graph))
    print('Problem 2: ', problem2(instructions=instructions, graph=graph))
    return 0


if __name__ == '__main__':
    import sys
    fpath = sys.argv[1]
    print("fpath:", fpath)
    main(fpath=fpath)
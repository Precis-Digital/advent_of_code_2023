import dataclasses
import itertools
import re
from math import lcm
from random import random
from threading import Thread

print_progress = False

re_end_line = re.compile(r'\r?\n?$')
re_instructions = re.compile(r'([LR]+)')
re_node_def = re.compile(r'(\w{3}) = \((\w{3}), (\w{3})\)')


class Node:
    name: str
    left: str
    right: str
    first: bool
    last: bool
    next_node: list['Node']
    last_direction_node: 'Node'
    end_node_indexes: set[int]

    def __init__(self,
                 name: str,
                 left: str,
                 right: str):
        self.name = name
        self.left = left
        self.right = right
        self.first = self.name[2] == 'A'
        self.last = self.name[2] == 'Z'
        self.next_node = []
        self.end_node_indexes = set()

    def pre_navigate(self,
                     *,
                     step: int,
                     network: 'Network',
                     bool_directions: list[bool]):
        self.next_node.append(network[self.left]
                              if step == 2 or self.left != 'ZZZ'
                              else None)
        self.next_node.append(network[self.right]
                              if step == 2 or self.right != 'ZZZ'
                              else None)
        if step == 2:
            node = self
            for index, bool_direction in enumerate(bool_directions):
                node = self.next_node[bool_direction]
                if node.last:
                    self.end_node_indexes.add(index + 1)

            self.last_direction_node = node

    def full_navigate(self,
                      *,
                      network: 'Network') -> tuple[set['Node'], 'Node', int]:
        node = self
        nodes: set['Node'] = {node}
        num_steps = 0
        for bool_direction in itertools.cycle(network.bool_directions):
            node = node.next_node[bool_direction]
            nodes.add(node)
            num_steps += 1
            if node.last:
                break
        return nodes, node, num_steps


class Network:
    directions: str
    bool_directions: list[bool]

    network: dict[str, Node]
    navigation_step = 0

    def __init__(self,
                 *,
                 directions: str):
        self.directions = directions
        self.len_directions = len(self.directions)
        self.bool_directions = [direction == 'R'
                                for direction in self.directions]
        # self.bool_directions = [random() < .5
        #                         for direction in self.directions]

        self.network = {}

    @property
    def next_direction(self):
        self.navigation_step += 1
        return self.bool_directions[(self.navigation_step - 1) % self.len_directions]

    def add_from_node_def(self,
                          *,
                          node_def: str):
        try:
            name, left, right = re_node_def.match(node_def).groups()
            self.network[name] = Node(name=name, left=left, right=right)
        except:
            pass

    def navigate(self,
                 *,
                 step: int) -> int:
        ending_nodes = []
        for node in self.network.values():
            node.pre_navigate(network=self,
                              step=step,
                              bool_directions=self.bool_directions)
            if step == 2 and node.end_node_indexes:
                ending_nodes.append(node)
                if print_progress:
                    print(f" Ending steps fro node {node.name}")
                    print(f"  {node.end_node_indexes}")

        if step == 1:
            node = self.network['AAA']
            while node:
                node = node.next_node[self.next_direction]
            return self.navigation_step
        else:
            navigation_nodes = [node
                                for node in self.network.values()
                                if node.first]
            if print_progress:
                print(f" Navigation Nodes")
                print(f"  {[node.name for node in navigation_nodes]}")
            full_navigations = [node.full_navigate(network=self)
                                for node in navigation_nodes]
            num_steps = [num_steps
                         for full_navigation_set, node, num_steps in full_navigations]

            if print_progress:
                print(f" Num Steps for each navigation node")
                print(f"  {num_steps}")

            return lcm(*num_steps)

    def __getitem__(self, item):
        return self.network[item]


def solve(*,
          step: int):
    print('*' * 20, f"Step {step}")

    with (open('input.txt', 'r') as input_file):
        directions = re_instructions.match(input_file.readline()).group(1)
        network = Network(directions=directions)

        for game_line in input_file:
            network.add_from_node_def(node_def=game_line)

    result = network.navigate(step=step)

    print('*' * 20, f"Step {step}", result)


if __name__ == '__main__':
    solve(step=1)
    solve(step=2)

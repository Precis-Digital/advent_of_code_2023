


from __future__ import annotations

import re
import math
from collections import Counter
from math import gcd
from functools import cache
import heapq
from dataclasses import dataclass, asdict, field

from enum import Enum

class Pulse(Enum):
    HIGH = 1
    LOW = 0

BUTTON_NODE = 'button'
BROADCASTER_NODE = 'broadcaster'



# @dataclass
# class ButtonModule:
#     """
#     There is a single button module (named button). When it receives a pulse, it sends a pulse to the broadcast module.
#     """
#     node_id: str = BUTTON_NODE
#     state: int = 0
#     target_modules: tuple[str] = [BROADCASTER_NODE]

@dataclass
class BroadcastModule:
    """
    There is a single broadcast module (named broadcaster). When it receives a pulse, it sends the same pulse to all of its destination modules.
    """
    node_id: str
    state: int #make 0
    target_modules: tuple[str]

    def update_target_modules(self, target: str):
        tuple(list(self.target_modules).append(target))

    def process_input(self, pulse: Pulse, source: str) -> list[tuple[str, Pulse]]:
        return [(target, pulse) for target in self.target_modules]


@dataclass
class FlipFlodModule:
    """
    Flip-flop modules (prefix %) are either on or off; they are initially off. 
    If a flip-flop module receives a high pulse, it is ignored and nothing happens. 
    However, if a flip-flop module receives a low pulse, it flips between on and off. 
    If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse
    """
    node_id: str
    state: int# 0 is off and 1 is on
    target_modules: tuple[str]

    def _flip(self):
        self.state = 1 - self.state

    def update_target_modules(self, target: str):
        tuple(list(self.target_modules).append(target))

    def process_input(self, pulse: Pulse, source: str) -> list[tuple[str, Pulse]]:
        if pulse == Pulse.HIGH:
            return []
        if pulse == Pulse.LOW:
            self._flip()
        if self.state == 1:
            return [(target, Pulse.HIGH) for target in self.target_modules]
        else:
            return [(target, Pulse.LOW) for target in self.target_modules]


@dataclass
class ConjuctionModule:
    """
    remember the type of the most recent pulse received from each of their connected input modules; 
    they initially default to remembering a low pulse for each input. When a pulse is received, the conjunction module first updates its memory for that input. 
    Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.
    """
    node_id: str
    _state: dict[str, int]
    target_modules: tuple[str]

    @property
    def state(self):
        return tuple(v for _,v in  sorted(self._state.items(), key=lambda x: x[0]))

    def _update_state(self, pulse: Pulse, source: str):
        self._state[source] = pulse

    def add_source_node(self, source: str):
        self._state[source] = Pulse.LOW

    def update_target_modules(self, target: str):
        tuple(list(self.target_modules).append(target))

    def process_input(self, pulse: Pulse, source: str) -> list[tuple[str, Pulse]]:
        self._update_state(pulse, source)
        if all(pulse == Pulse.HIGH for pulse in self._state.values()):
            return [(target, Pulse.LOW) for target in self.target_modules]
        else:
            return [(target, Pulse.HIGH) for target in self.target_modules]


@dataclass
class NullModule:
    """
    Null Modules are dead ends. They do not send pulses to any other modules.
    """
    node_id: str
    state: int
    target_modules: tuple[str]

    def update_target_modules(self, target: str):
        tuple(list(self.target_modules).append(target))

    def process_input(self, pulse: Pulse, source: str) -> list[tuple[str, Pulse]]:
        return []
    
ModuleType = BroadcastModule | FlipFlodModule | ConjuctionModule


@dataclass
class Graph:
    graph: dict[str, ModuleType]

    def add_node(self, node_id: str, node: ModuleType):
        self.graph[node_id] = node

    def get_node(self, node_id: str) -> ModuleType:
        return self.graph.get(node_id, NullModule(node_id, state=0, target_modules=[]))

    def get_graph_state(self):
        return tuple((node_id, node.state) for node_id, node in sorted(self.graph.items(), key=lambda x: x[0]))
    
    def initialize_conjuction_nodes(self):
        """ update all conjuction modules so they have correct inout"""
        for node_id, node in self.graph.items():
            for target in node.target_modules:
                target_module = self.graph.get(target)
                if isinstance(target_module, ConjuctionModule):
                    target_module.add_source_node(node_id)

    def initialize_null_nodes(self):
        """ update all conjuction modules so they have correct inout"""
        nodes = list(self.graph.values())[:]
        for node in nodes:
            for target in node.target_modules:
                target_module = self.graph.get(target)
                if target_module is None:
                    self.add_node(target, NullModule(target, state=0, target_modules=[]))


    def __hash__(self) -> int:
        return hash(self.get_graph_state())

def parse_input(f):

    graph = Graph(graph={})

    for row in f:
        row = row.strip()
        node, target_string = row.split(" -> ")
        if "," in target_string:
            target_nodes = list(map(lambda x: x.strip(), target_string.split(",")))
        else:
            target_nodes = [target_string]
        
        if node == "broadcaster":
            module = BroadcastModule(node, state=0, target_modules=target_nodes)
            graph.add_node(node, module)
        elif node.startswith("%"):
            node = node[1:]
            module = FlipFlodModule(node, state=0, target_modules=target_nodes)
            graph.add_node(node, module)
        elif node.startswith("&"):
            node = node[1:]
            module = ConjuctionModule(node, _state={}, target_modules=target_nodes)
            graph.add_node(node, module)

    # print(graph)
    graph.initialize_conjuction_nodes()
    graph.initialize_null_nodes()
    # print(graph)
    return graph



def run_simulation(graph: Graph, pulse: Pulse, stop_condition= None) -> Graph:
    """
    Run one simulation
    """

    # print(graph.get_graph_state())
    queue = []
    queue.append((BUTTON_NODE, BROADCASTER_NODE, pulse))
    # heapq.heappush(queue, ((1, (0, )), )

    visited_graph = set()
    high_pulse_count = 0
    low_pulse_count = 0

    # for k,v in graph.graph.items():
    #     print(f">>>> Node:{k:<11} Module:{v}")

    while queue:
        source_node_id, target_node_id, pulse = queue.pop(0) #BFS
        if stop_condition is not None and (target_node_id, pulse) == stop_condition:
            return graph, high_pulse_count, low_pulse_count, True
        if pulse == Pulse.HIGH:
            high_pulse_count += 1
        else:
            low_pulse_count += 1

        # print(source_node_id, " -- ", pulse, "->", target_node_id)
        # for k,v in graph.graph.items():
        #     print(f">>>> Node:{k:<11} Module:{v}")


        # if (target_node_id, pulse, graph) in visited_graph:
        #     print("cycle detected", source_node_id, target_node_id, pulse)
        #     # for l in visited_graph:
        #     #     print(l)
        #     break



        node = graph.get_node(node_id=target_node_id)

        # insert the nodes in reverse order so that they are popped in the correct order
        for new_target_node_id, new_pulse  in node.process_input(pulse=pulse, source=source_node_id):
            # print("adding", target_node_id, pulse, graph)
            # heapq.heappush(queue, ((target_node_id, new_target_node_id, new_pulse))
            queue.append((target_node_id, new_target_node_id, new_pulse))
        
        # print("adding", target_node_id, pulse, graph)
        # visited_graph.add((target_node_id, pulse, graph))
        
    return graph, high_pulse_count, low_pulse_count, False


def problem1(input_):
    """"

    Plan... need to do a few things...

    1. need to be able to run through one run of the simulation which should  take as input a (graph, state) -> (graph, state, high pulse count, low pulse count)
    2. run the simulate mulltiple times until the state is repeated. It's not necessarily the case it will return to the starting condition I guess!!! similar to an earlier problem
    3. based on that you should have the cycle length and the starting index of the first cycle and then can compute how many pulses you will encounter afte some number of cycle

    """
    graph = input_
    print()
    for k,v in graph.graph.items():
        print(f">>>> Node:{k:<11} Module:{v}")

    # print("graph state: ", graph.get_graph_state())

    # states = set()
    # states.add(graph)
    # print(states)

    total_high_pulse_count = 0
    total_low_pulse_count = 0

    for _ in range(1000):
        graph, high_pulse_count, low_pulse_count, _ = run_simulation(graph=graph, pulse=Pulse.LOW)
        total_high_pulse_count += high_pulse_count
        total_low_pulse_count += low_pulse_count
        # print("graph state: ", graph.get_graph_state())
        # print("high pulse count: ", high_pulse_count)
        # print("low pulse count: ", low_pulse_count)
    return total_high_pulse_count * total_low_pulse_count
    

    

def problem2(input_):
    graph = input_

    total_high_pulse_count = 0
    total_low_pulse_count = 0

    visited_graph = set()
    print(graph)
    # return
    for i in range(1, 1000000001):
        # print("button pressed", i)
        if i % 10000 == 0:
            print("i:", i)
        graph, high_pulse_count, low_pulse_count, stop = run_simulation(graph=graph, pulse=Pulse.LOW, stop_condition= ('rx', Pulse.LOW))
        # if graph in visited_graph:
        #     print("cycle detected")
        #     break
        # visited_graph.add(graph)
        # print(visited_graph)
        total_high_pulse_count += high_pulse_count
        total_low_pulse_count += low_pulse_count
        # print("graph state: ", graph.get_graph_state())
        # print("high pulse count: ", high_pulse_count)
        # print("low pulse count: ", low_pulse_count)
        if stop:
            return i
    

def main(fpath: str):
    with open(fpath, 'r') as f:
        input_ = parse_input(f)

    print('Problem 1: ', problem1(input_))  
    print('Problem 2: ', problem2(input_))
    return 0


if __name__ == '__main__':
    import sys
    fpath = sys.argv[1]
    print("fpath:", fpath)
    main(fpath=fpath)


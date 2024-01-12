from __future__ import annotations

import re
import math
from collections import Counter
from math import gcd
from functools import cache
import heapq
from dataclasses import dataclass, asdict


@dataclass
class Status:
    accepted: bool


@dataclass
class Workflow:
    node: str

@dataclass
class PartRange:
    x: tuple[int, int]
    m: tuple[int, int]
    a: tuple[int, int]
    s: tuple[int, int]

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class Rule:
    expression: tuple[str, str, int]
    if_true: Workflow | Rule | Status
    if_false: Workflow | Rule | Status

    def evaluate_expression(self, part):
        field, op, value = self.expression
        part_value = part[field]

        if op == '<':
            return part[field] < value
        elif op == '>':
            return part[field] > value
        else:
            raise ValueError(f'operator not recognized {self.expression, part}')
        
    def get_neighbors(self, part_range) -> list[tuple[PartRange, Rule | Workflow | Status]]:
        field, op, value = self.expression
        part_field_lb, part_field_ub = part_range[field]

        if op == '<':
            # if the part range is less than the value, then we know that the part range is true
            if part_field_ub < value:
                return [(part_range, self.if_true)]
            # if the part range is greater than the value, then we know that the part range is false
            elif part_field_lb >= value:
                return [(part_range, self.if_false)]
            # if the part range is in between the value, then we need to split the part range into two parts
            else:
                false_dict = asdict(part_range)
                false_dict.update({field: (value, part_field_ub)})
                true_dict = asdict(part_range)
                true_dict.update({field: (part_field_lb, value - 1)})
                return [
                    (PartRange(**true_dict), self.if_true),
                    (PartRange(**false_dict), self.if_false)
                ]
        elif op == '>':
            # if the part range is less than the value, then we know that the part range is false
            if part_field_ub <= value:
                return [(part_range, self.if_false)]
            # if the part range is greater than the value, then we know that the part range is true
            elif part_field_lb > value:
                return [(part_range, self.if_true)]
            # if the part range is in between the value, then we need to split the part range into two parts
            else:
                false_dict = asdict(part_range)
                false_dict.update({field: (part_field_lb, value)})
                true_dict = asdict(part_range)
                true_dict.update({field: (value + 1, part_field_ub)})

                # print(false_dict, true_dict)
                return [
                    (PartRange(**true_dict), self.if_true),
                    (PartRange(**false_dict), self.if_false)
                ]



def parse_condition(s):
    if '<' in s:
        return s.split('<', 1)[0], '<', int(s.split('<', 1)[1])
    elif '>' in s:
        return s.split('>', 1)[0], '>', int(s.split('>', 1)[1])
    else:
        raise ValueError(s)

def parse_recursive_rule(s):
    if s == 'A':
        return Status(True)
    elif s == 'R':
        return Status(False)
    elif '<' not in s and '>' not in s:
        return Workflow(s)
    
    condition, rest = s.split(':', 1)
    true_str, false_str = rest.split(',', 1)
    true_rule = parse_recursive_rule(true_str)
    false_rule = parse_recursive_rule(false_str)
    
    return Rule(parse_condition(condition), true_rule, false_rule)

def parse_input(f) -> tuple[dict[str, Rule], list[dict[str, int]]]:
    
    # exract workflows

    workflows = {}
    parts = []
    for row in f:
        row = row.strip()
        if row == '':
            break
        workflow_id, rest = row.split('{', 1)
        rest = rest.replace('}', '')
        rule = parse_recursive_rule(rest)
        workflows[workflow_id] = rule

    for row in f:
        row = row.strip()
        matches = re.findall(r'(\d+)', row)
        part = {c: int(x) for c, x in zip('xmas', matches)}
        assert len(part) == 4
        parts.append(part)

    return workflows, parts

def get_part_status(workflows, part):
    stack = []
    stack.append(workflows['in'])

    while True:
        action: Rule | Workflow | Status = stack.pop(0)
        print(action)
        if isinstance(action, Status):
            return action.accepted
        elif isinstance(action, Workflow):
            stack.append(workflows[action.node])
        elif isinstance(action, Rule):
            if action.evaluate_expression(part):
                stack.append(action.if_true)
            else:
                stack.append(action.if_false)
        else:
            raise ValueError(action)


def test_get_part_status(workflows):
    part = {'x': 787, 'm': 2655, 'a': 1222, 's': 2876}
    assert get_part_status(workflows, part) == True, 'This part should be accepted on sample input'
    print("=========================")

    part = {'x': 0, 'm': 0, 'a': 2006, 's': 537}
    print(">>>", get_part_status(workflows, part))

    # >>>> part range: PartRange(x=(480, 810), m=(0, 4000), a=(1849, 2594), s=(434, 818)) action: Status(accepted=True)
    # >>>> part range: PartRange(x=(480, 810), m=(0, 4000), a=(1849, 2594), s=(0, 433)) action: Status(accepted=False)
    print("=========================")
    print(get_part_status(workflows, {"x": 480, "m": 0, "a": 1849, "s": 43}))

def problem1(input_):
    workflows, parts = input_
    return sum(sum(part.values()) for part in parts if get_part_status(workflows, part))


def problem2(input_):
    """
    Two ideas... one can you reverse the tree and then find out what rules satisfy the accept state

    so taking this for example

    {x=2127,m=1623,a=2188,s=1013}: in -> px -> rfg -> A


    go backwards from that A

    x > 2440, False => x <= 2440
    s < 537, False =>  s >= 537
    m > 2090, False => m <= 2090
    a < 2006, False => a >= 2006
    s < 1351, True =>  s < 1351

    so any part with these ranges will work: 

    x = [0, 2440]
    m = [0. 2090]
    a = [2006, 4000]
    s = [537, 1350]

    all of these land in this node

     ------------

    other approach is to just split on sub ranges start with range x: [0, 4000], m: [0, 4000]... and that each node, compute the valid sub range and when you hit an "A" state append to a list of acceptable part ranges

    this seems like the most efficient approach since it only requires one forward pass of the graph and both have some "bookkeeping" requirements so i dont save any time there
    
    """
    ActionType = Rule | Workflow | Status

    workflows, _ = input_
    stack = []
    stack.append((PartRange(x=(1, 4000), m=(1, 4000), a=(1, 4000), s=(1, 4000)), Workflow('in')))
    accepted_part_ranges: list[PartRange] = []

    while stack:
        part_range, action = stack.pop()
        print(">>>>", "part range:", part_range, "action:", action)
        if isinstance(action, Status):
            if action.accepted:
                accepted_part_ranges.append(part_range)
                # return
            continue
        elif isinstance(action, Workflow):
            stack.append((part_range, workflows[action.node]))
        elif isinstance(action, Rule):
            for neighbor in action.get_neighbors(part_range):
                print(">>>>>>>>>>>neighbor:", neighbor)
                stack.append(neighbor)
        else:
            raise ValueError(action)
    
    # print("accepted_part_ranges:", accepted_part_ranges)
    total = 0
    for range in accepted_part_ranges:
        range_product = 1
        for range in asdict(range).values():
            range_product *= (range[1] - range[0] + 1)
        total += range_product
    return total

def main(fpath: str):
    with open(fpath, 'r') as f:
        input_ = parse_input(f)

    test_get_part_status(input_[0])
    # print('Problem 1: ', problem1(input_))  
    print('Problem 2: ', problem2(input_))
    return 0


if __name__ == '__main__':
    import sys
    fpath = sys.argv[1]
    print("fpath:", fpath)
    main(fpath=fpath)

131744025564668
167409079868000
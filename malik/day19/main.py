from __future__ import annotations

import re
import math
from collections import Counter
from math import gcd
from functools import cache
import heapq
from dataclasses import dataclass




@dataclass
class Status:
    accepted: bool


@dataclass
class Workflow:
    node: str

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
        action: Rule | Workflow | Status = stack.pop()
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


def problem1(input_):
    workflows, parts = input_
    return sum(sum(part.values()) for part in parts if get_part_status(workflows, part))


def problem2(input_):
    pass
    

def main(fpath: str):
    with open(fpath, 'r') as f:
        input_ = parse_input(f)

    test_get_part_status(input_[0])
    print('Problem 1: ', problem1(input_))  
    print('Problem 2: ', problem2(input_))
    return 0


if __name__ == '__main__':
    import sys
    fpath = sys.argv[1]
    print("fpath:", fpath)
    main(fpath=fpath)
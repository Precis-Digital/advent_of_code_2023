import re
import math
from collections import Counter
from math import gcd
from functools import cache


def extract_groups(record: str) -> list[str]:
    groups = re.findall(r'([\?\#?]+|\#+)', record)
    return groups

def convert_groups_to_contig_group_estimates(groups: list[str]) -> list[int]:
    contig_group_estimates = []
    for group in groups:
        if '?' in group:
            contig_group_estimates.append(0)
        elif group.startswith('#'):
            contig_group_estimates.append(len(group))
    return contig_group_estimates

def parse_input(f) -> list[tuple[str, list[int]]]:
    rows = []
    for line in f:
        condition_record, contig_group =  line.split()
        contig_group = [int(x) for x in contig_group.split(',')]
        rows.append((condition_record, contig_group))
    return rows


def is_valid_state(condition_record: str, contig_group: list[int]) -> bool:
    """"
    can be optimized further for example this, case "########????"  for [3, 2, 1], reports as valid.. but should not be

    but you should be able to eliminate any cases where the prefix run is greater than the
    """

    groups = extract_groups(condition_record)
    contig_group_estimates = convert_groups_to_contig_group_estimates(groups)

    for a, b in zip(contig_group_estimates, contig_group):
        # the next group includes a ? and therefore the total is unknown
        # if a < b:
        if a == 0:
            return True
        if a != b:
            return False
    return True

def is_done_state(condition_record: str, contig_group: list[int]) -> bool:
    return '?' not in condition_record

def is_answer_state(condition_record: str, contig_group: list[int]) -> bool:
    groups = extract_groups(condition_record)
    contig_group_estimates = convert_groups_to_contig_group_estimates(groups)
    return contig_group_estimates == contig_group

    
def tests():
    a = "##..##..##" 
    b = [2, 2, 2]
    print(a, b, is_valid_state(a, b))

    a = "????..##..##" 
    b = [2, 2, 2]
    print(a, b, is_valid_state(a, b))

    a = "?..##..##" 
    b = [2, 2, 2]
    print(a, b, is_valid_state(a, b))

    a = "#..??..##" 
    b = [2, 2, 2]
    print(a, b, is_valid_state(a, b))


def dfs(condition_record, contig_group):
    curent_state = [condition_record]
    valid_states = set()
    num_states = 0

    while curent_state:
        num_states += 1
        state = curent_state.pop()        

        if not is_valid_state(state, contig_group):
            continue


        if is_done_state(state, contig_group):
            if is_answer_state(state, contig_group):
                valid_states.add(state)
            continue

        # generate next states
        index = state.find('?')
        new_string_dot = state[:index] + "." + state[index+1:]
        new_string_hash = state[:index] + "#" + state[index+1:]
        curent_state.append(new_string_dot)
        curent_state.append(new_string_hash)
    # print("num_states", num_states)
    return valid_states



def problem1(records: list[tuple[str, list[int]]]) -> int:
    total = 0
    for condition_record, contig_group in records:
        valid_states = dfs(condition_record, contig_group)
        total += len(valid_states)
    return total


@cache
def get_solution_count(condition_record, contig_group, num_in_current_group=0):
    # print(condition_record, contig_group, num_in_current_group)

    # so you've reached all valid stats
    if len(contig_group) == 0:
        # if there are still hashes left then it's not a valid solution
        if '#' in condition_record:
            return 0
        return 1
    
    if len(condition_record) == 0 and len(contig_group) > 0:
        return 0
    
    for s in condition_record:
        if s == '#':
            num_in_current_group += 1
            return get_solution_count(condition_record[1:], contig_group, num_in_current_group)
        elif s == '.':
            if num_in_current_group == 0:
                return get_solution_count(condition_record[1:], contig_group, 0)
            elif num_in_current_group == contig_group[0]:
                return get_solution_count(condition_record[1:], tuple(list(contig_group)[1:]), 0)  
            else:
                return 0
        elif s == '?':
            return get_solution_count("." + condition_record[1:], contig_group, num_in_current_group) + get_solution_count("#" + condition_record[1:], contig_group, num_in_current_group)
        
    
def problem1dymanic(records: list[tuple[str, list[int]]]) -> int:
    total = 0
    for condition_record, contig_group in records:
        total += get_solution_count(condition_record +".", tuple(contig_group))
    return total

def problem2(records: list[tuple[str, list[int]]]) -> int:
    """
    looked up the solution from the internet that it required using dynamic programming

    did my own implementation of the solution based on the basic idea...
    """
    total = 0
    for condition_record, contig_group in records:
        print(condition_record, contig_group)
        new_condition_record = "?".join(condition_record for _ in range(5))
        new_contig_group = contig_group * 5
        total += get_solution_count(new_condition_record +".", tuple(new_contig_group))
    return total
    

def main(fpath: str):
    with open(fpath, 'r') as f:
        records = parse_input(f)
        
    print("tests------------------")
    tests()
    print("tests------------------")
    # print('Problem 1: ', problem1(records)) #7195
    print('Problem 1(DP): ', problem1dymanic(records)) #7195
    print('Problem 2: ', problem2(records)) 
    return 0


if __name__ == '__main__':
    import sys
    fpath = sys.argv[1]
    print("fpath:", fpath)
    main(fpath=fpath)
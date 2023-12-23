import re
import math
from collections import Counter
from math import gcd


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


def problem2(records: list[tuple[str, list[int]]]) -> int:
    return -1
    total = 0
    i, n = 0, len(records)
    for condition_record, contig_group in records:
        print('starting', i, n)
        new_record, new_contig_group ='?'.join([condition_record for _ in range(5)]), contig_group*5
        valid_states = dfs(new_record, new_contig_group)
        print(len(valid_states), new_record, new_contig_group)
        total += len(valid_states)
        i += 1

    return total
    

def main(fpath: str):
    with open(fpath, 'r') as f:
        records = parse_input(f)
        
    print("tests------------------")
    tests()
    print("tests------------------")
    print('Problem 1: ', problem1(records)) #7195
    print('Problem 2: ', problem2(records)) 
    return 0


if __name__ == '__main__':
    import sys
    fpath = sys.argv[1]
    print("fpath:", fpath)
    main(fpath=fpath)
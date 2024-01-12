import re
import math
from collections import Counter
from math import gcd
from functools import cache



def parse_input(f) -> list[tuple[list[str], list[str]]]:
    output = []
    rows = []
    columns = []
    for row in f:
        row = row.strip()
        if row == '':
            output.append((rows, columns))
            rows = []
            columns = []
            continue
        if not columns:
            columns = ["" for _ in range(len(row))]
        rows.append(row)
        for i, cell in enumerate(row):
            columns[i] += cell
    output.append((rows, columns))
    return output



def get_reflection_point(rows, allow_smudge=False, debug=False):

    @cache
    def row_equal(a, b, allow_smudge=False) -> tuple[bool, bool]:
        """
        returns is_equal, is_smudge
        """

        if a==b:
            return True, False
        elif allow_smudge:
            diff = 0
            for i,s in enumerate(a):
                if s != b[i]:
                    diff += 1
                    if diff > 1:
                        return False, True
            if diff == 1:
                return True, True
            if diff == 0:
                return True, False
            return False, False
        
        return False, False


    if debug: print(rows)

    N = len(rows)
    for i in range(N - 1):
        # found a center reflection
        smudge_budget = 0
        is_equal, is_smudge = row_equal(rows[i], rows[i+1], allow_smudge=allow_smudge)
        if is_equal:
            if debug: print("found a center reflection", i, rows[i], rows[i+1])
            j,k = i, i+1
            while j >= 0 and k < N:
                
                is_equal, is_smudge = row_equal(rows[j], rows[k], allow_smudge=allow_smudge)
                if debug: print("j, k", j, k, rows[j], rows[k], is_equal, is_smudge)
                if not is_equal:
                    break
                
                if is_smudge:    
                    smudge_budget += 1
                    if smudge_budget > 1:
                        break
                
                if (j == 0 or k == (N -1)):
                    if allow_smudge and smudge_budget == 0:
                        break
                    return i
                j -= 1
                k += 1

    return -1


def problem1(grids: list[tuple[list[str], list[str]]]) -> int:
    score = 0
    for g in grids:
        
        rows, columns = g
        
        row_reflection = get_reflection_point(rows)
        column_reflection = get_reflection_point(columns)

        if row_reflection != -1:
            score += (row_reflection + 1) * 100

        if column_reflection != -1:
            score += (column_reflection + 1)

        # print("="*10, len(rows), len(columns), row_reflection, column_reflection, score)
    return score



def problem2(grids):
    score = 0
    for g in grids:
        
        rows, columns = g
        
        row_reflection = get_reflection_point(rows, allow_smudge=True, debug=False)
        column_reflection = get_reflection_point(columns, allow_smudge=True, debug=False)

        if row_reflection != -1:
            score += (row_reflection + 1) * 100

        if column_reflection != -1:
            score += (column_reflection + 1)

        # print("="*10, len(rows), len(columns), row_reflection, column_reflection, score)
    return score


def main(fpath: str):
    with open(fpath, 'r') as f:
        output = parse_input(f)
        
    print('Problem 1: ', problem1(output)) #27664
    print('Problem 2: ', problem2(output[:]))  # 33991
    return 0


if __name__ == '__main__':
    import sys
    fpath = sys.argv[1]
    print("fpath:", fpath)
    main(fpath=fpath)
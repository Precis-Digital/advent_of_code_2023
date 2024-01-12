import re
import math
from collections import Counter
from math import gcd
from functools import cache

def hash_algorithm(s: str) -> int:
    current_value = 0
    for c in s:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256
    return current_value



def parse_input(f):
    return f.read().strip().split(",")


def problem1(input_):
    total = 0
    for step in input_:
        total += hash_algorithm(step)
    return total

def problem2(input_):
    boxes = {}
    i = 0
    for step in input_:
        i += 1
        # if i % 100 == 0:
        #     print(i, len(input_))
        if "=" in step:
            label, value = step.split("=")
            value = int(value)
            label_hash = hash_algorithm(label)

            if label_hash not in boxes:
                boxes[label_hash] = []
            
            found_lens = False
            for idx, (lens_label, lens_value) in enumerate(boxes[label_hash]):
                if lens_label == label:
                    found_lens = True
                    boxes[label_hash][idx] = (label, value)
                    break
            
            if not found_lens:
                boxes[label_hash].append((label, value))
        else:
            # remove lense
            label = step.replace("-", "")
            label_hash = hash_algorithm(label)
            if label_hash not in boxes:
                boxes[label_hash] = []

            boxes[label_hash] = [(lens_label, lens_value) for lens_label, lens_value in boxes[label_hash] if lens_label != label]

        # print(step)
        # for k in sorted(boxes.keys()):
        #     print(k, boxes[k])
    total = 0
    for k, v in boxes.items():
        for idx, (_, lens_value) in enumerate(v):
            total += (k + 1)  * (idx + 1) * lens_value
    return total

def main(fpath: str):
    with open(fpath, 'r') as f:
        input_ = parse_input(f)
        
    assert hash_algorithm("HASH") == 52
    print('Problem 1: ', problem1(input_)) #109833
    print('Problem 2: ', problem2(input_))  
    return 0


if __name__ == '__main__':
    import sys
    fpath = sys.argv[1]
    print("fpath:", fpath)
    main(fpath=fpath)
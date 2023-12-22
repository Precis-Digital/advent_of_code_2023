import re
import math
from collections import Counter
from math import gcd


def parse_input(f):
    return [list(map(int, row.split())) for row in f]
        


def predict_next_value(signal_history, go_backwards = False):
    deltas = [signal_history]
    while True:
        last_history = deltas[-1]
        new_history = [last_history[i+1] - last_history[i] for i in range(len(last_history) - 1) ]
        deltas.append(new_history)

        if all([x == 0 for x in new_history]):
            break
    
    if go_backwards:
        # print("-----")
        prediction = 0
        N = len(deltas)
        for i in range(N):
            prediction = deltas[N - i - 1][0] - prediction
            # print(prediction)
        return prediction
    else:
        prediction = 0
        N = len(deltas)
        for i in range(N):
            prediction += deltas[N - i - 1][-1]
        return prediction
        


def problem1(signal_hisories):
    return sum(predict_next_value(sh) for sh in signal_hisories)
        

def problem2(signal_hisories):
    return sum(predict_next_value(sh, go_backwards=True) for sh in signal_hisories)

    


def main(fpath: str):
    with open(fpath, 'r') as f:
        signal_hisories = parse_input(f)

    print('Problem 1: ', problem1(signal_hisories))
    print('Problem 2: ', problem2(signal_hisories))
    return 0


if __name__ == '__main__':
    import sys
    fpath = sys.argv[1]
    print("fpath:", fpath)
    main(fpath=fpath)
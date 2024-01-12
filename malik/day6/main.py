import re
import math

def parse_input(f) -> (list[int], list[int]):
    time_line = f.readline()
    times = list(map(int, re.findall(r'\d+', time_line)))
    
    distance_line = f.readline()
    distances = list(map(int, re.findall(r'\d+', distance_line)))
    
    return times, distances



def quadratic(a, b, c):
    # Applying the quadratic formula: x = (-b ± √(b²-4ac)) / 2a
    delta = b**2 - 4*a*c  # calculating the discriminant (b²-4ac)

    # Calculating the two possible solutions for x
    x1 = (-b + delta**0.5) / (2*a)
    x2 = (-b - delta**0.5) / (2*a)

    return x1, x2

def number_of_possible_solutions(t, d):
    a, b =  quadratic(1, -t, d + 1)
    x_min = min(a, b)
    x_max = max(a, b)
    a = math.ceil(x_min)
    b = math.floor(x_max)
    number_of_solutions = abs(b - a) + 1
    return number_of_solutions

def problem1(times, distances):
    answer = 1
    for t, d in zip(times, distances):
        answer *= number_of_possible_solutions(t, d)
    return answer

def problem2(times, distances):
    t = int(''.join(str(a) for a in times))
    d = int(''.join(str(a) for a in distances))
    return number_of_possible_solutions(t, d)

def main(fpath: str):
    with open(fpath, 'r') as f:
       times, distances = parse_input(f)

    print('Problem 1: ', problem1(times, distances))
    print('Problem 2: ', problem2(times, distances))
    return 0


if __name__ == '__main__':
    import sys
    fpath = sys.argv[1]
    print(fpath)
    main(fpath=fpath)
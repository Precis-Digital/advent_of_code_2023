import itertools
import re

print_progress = [False, False]

re_end_line = re.compile(r'\r?\n?$')
re_empty = re.compile(r'^\.+$')
re_galaxies = re.compile(r'(#)')

splice_step = [1, 1000000 - 1]


def solve(*,
          step: int):
    print('*' * 20, f"Step {step}")

    galaxies: dict[int, list[int]] = {}
    columns_galaxies: dict[int, list[int]] = {}
    with (open('input.txt', 'r') as input_file):
        y = 0
        num_galaxies = 0
        for line in input_file.read().splitlines():
            if re_empty.fullmatch(line):
                if print_progress[step - 1]:
                    print(f' empty {y}')
                y += splice_step[step - 1]
            else:
                for galaxy_match in re_galaxies.finditer(line):
                    x = galaxy_match.regs[0][0]
                    num_galaxies += 1
                    galaxies[num_galaxies] = [y, x]
                    columns_galaxies[x] = columns_galaxies.get(x, []) + [num_galaxies]
            y += 1

        galaxies_columns = list(sorted(columns_galaxies.keys()))
        if print_progress[step - 1]:
            print(' galaxies_columns', galaxies_columns)
        splice_sum = 0
        for index, x in enumerate(galaxies_columns):
            if index:
                splice = x - galaxies_columns[index - 1] - 1
                if print_progress[step - 1] and splice:
                    print(f' splice {x} = {splice}')
                splice_sum += splice * splice_step[step - 1]
                if splice_sum:
                    for galaxy in columns_galaxies[x]:
                        galaxies[galaxy][1] += splice_sum

        result = 0
        for (start, end) in list(itertools.combinations(range(1, num_galaxies + 1), 2)):
            start_y, start_x = galaxies[start]
            end_y, end_x = galaxies[end]
            result += abs(start_x - end_x) + abs(start_y - end_y)

    print('*' * 20, f"Step {step}", result)


if __name__ == '__main__':
    solve(step=1)
    solve(step=2)

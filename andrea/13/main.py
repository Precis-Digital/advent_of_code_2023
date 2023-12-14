import re

print_progress = [False, False]

re_only_one_difference = re.compile(r'^(.*?)(.)(.*) \1(?!\2).\3$')


def find_reflection_line(*,
                         step: int,
                         mirrors: list[list[str]]):
    mirrors_reflection = {}

    for index_mirror, mirror in enumerate(mirrors):
        prev_line = ''
        for index_line, line in enumerate(mirror):
            if prev_line:
                if line == prev_line:
                    matched = True
                    already_smudged = False
                elif step == 2 and re_only_one_difference.fullmatch(line + ' ' + prev_line):
                    matched = True
                    already_smudged = True
                else:
                    prev_line = line
                    continue

                if matched:
                    if step == 1 or already_smudged:
                        if all(mirror[before] == mirror[after]
                               for before, after in zip(range(index_line - 2, -1, -1),
                                                        range(index_line + 1, len(mirror)))):
                            assert (index_mirror + 1) not in mirrors_reflection

                            mirrors_reflection[index_mirror + 1] = index_line
                            break
                    else:
                        matched = True
                        for before, after in zip(range(index_line - 2, -1, -1),
                                                 range(index_line + 1, len(mirror))):
                            if mirror[before] == mirror[after]:
                                continue
                            if (not already_smudged
                                    and re_only_one_difference.fullmatch(mirror[before] + ' ' + mirror[after])):
                                already_smudged = True
                                continue
                            else:
                                matched = False
                                break
                        if matched and already_smudged:
                            assert (index_mirror + 1) not in mirrors_reflection

                            mirrors_reflection[index_mirror + 1] = index_line
                            break

            prev_line = line

    return mirrors_reflection


def solve(*,
          step: int):
    print('*' * 20, f"Step {step}")

    rows_mirrors = []

    with (open('input.txt', 'r') as input_file):
        for index_line, line in enumerate(input_file.read().splitlines()):
            if index_line == 0 or not line:
                mirror = []
                rows_mirrors.append(mirror)
                if not line:
                    continue

            mirror.append(line)

    columns_mirrors = []
    for index_mirror, mirror in enumerate(rows_mirrors):
        len_first_line = len(mirror[0])
        assert all(len(line) == len_first_line for line in mirror[1:])

        columns_mirrors.append([
            ''.join(line[index]
                    for line in mirror)
            for index in range(len(mirror[0]))
        ])

    mirrors_rows_reflection = find_reflection_line(step=step,
                                                   mirrors=rows_mirrors)

    mirrors_columns_reflection = find_reflection_line(step=step,
                                                      mirrors=columns_mirrors)

    if step == 2:
        for index_mirror, _ in enumerate(rows_mirrors):
            assert ((index_mirror + 1) in mirrors_rows_reflection
                    or (index_mirror + 1) in mirrors_columns_reflection)

    result = sum(mirrors_rows_reflection.values()) * 100 + sum(mirrors_columns_reflection.values())

    print('*' * 20, f"Step {step}", result)


if __name__ == '__main__':
    solve(step=1)
    solve(step=2)

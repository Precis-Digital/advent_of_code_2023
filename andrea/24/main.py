import functools

print_progress = [False, False]


def solve(*,
          step: int):
    print('*' * 20, f"Step {step}")

    with (open('input.txt', 'r') as input_file):
        for index_line, line in enumerate(input_file.read().splitlines()):
            pass

    result = 0

    print('*' * 20, f"Step {step}", result)


if __name__ == '__main__':
    solve(step=1)
    solve(step=2)

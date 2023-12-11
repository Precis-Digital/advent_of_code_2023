import re
from typing import Optional

print_progress = [False, False]

re_end_line = re.compile(r'\r?\n?$')

connection_points: dict[str, tuple[tuple[int, int], tuple[int, int]]] = {
    '|': ((-1, 0), (1, 0)),
    'L': ((-1, 0), (0, 1)),
    'J': ((-1, 0), (0, -1)),
    '-': ((0, -1), (0, 1)),
    '7': ((0, -1), (1, 0)),
    'F': ((0, 1), (1, 0))
}


def solve(*,
          step: int):
    print('*' * 20, f"Step {step}")

    result = 0
    matrix: dict[tuple[int, int], dict[tuple[int, int], tuple[int, int]]] = {}
    start_coords: Optional[tuple[int, int]] = None
    num_y = 0
    num_x = 0
    with (open('input.txt', 'r') as input_file):
        for y, line in enumerate(input_file.read().splitlines()):
            num_y += 1
            num_x = max(num_x, len(line))
            for x, cell in enumerate(line):
                if cell == 'S':
                    start_coords = (y, x)
                elif cell == '.':
                    matrix[(y, x)] = {}
                else:
                    (y1, x1), (y2, x2) = connection_points[cell]
                    matrix[(y, x)] = {
                        (y + y1, x + x1): (y + y2, x + x2),
                        (y + y2, x + x2): (y + y1, x + x1)}

    if start_coords is None:
        raise ValueError('Missing start point')

    entry_coords = start_coords

    for y, x in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        exit_coords = (start_coords[0] + y, start_coords[1] + x)
        if start_coords in matrix.get(exit_coords):
            num_steps = 1
            while exit_coords != start_coords:
                num_steps += 1
                entry_coords, exit_coords = (exit_coords, matrix[exit_coords][entry_coords])
            if step == 1:
                result = int(num_steps / 2)
            break

    print('*' * 20, f"Step {step}", result)


if __name__ == '__main__':
    solve(step=1)
    solve(step=2)

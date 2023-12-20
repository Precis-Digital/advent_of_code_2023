import re
from typing import Optional

print_progress = [False, False]

re_end_line = re.compile(r'\r?\n?$')

connection_points: dict[
    str, tuple[tuple[int, int], tuple[int, int], int, tuple[list[tuple[int, int]], list[tuple[int, int]]]]] = {
    '|': ((-1, 0), (1, 0), 0, ([(0, 1)], [(0, -1)])),
    'L': ((-1, 0), (0, 1), -1, ([], [(0, -1), (1, 0)])),
    'J': ((-1, 0), (0, -1), 1, ([(0, 1), (1, 0)], [])),
    '-': ((0, -1), (0, 1), 0, ([(-1, 0)], [(1, 0)])),
    '7': ((0, -1), (1, 0), 1, ([(-1, 0), (0, 1)], [])),
    'F': ((0, 1), (1, 0), -1, ([], [(-1, 0), (0, -1)]))
}

right_left_turns: dict[tuple[tuple[int, int], tuple[int, int]], tuple[int, tuple[list[tuple[int, int]], list[tuple[int, int]]]]] = {
    (entry_diff, exit_diff): (right_left, left_right_diffs)
    for entry_diff, exit_diff, right_left, left_right_diffs in connection_points.values()
}
right_left_turns.update({
    (exit_diff, entry_diff): (-right_left, tuple(reversed(left_right_diffs)))
    for entry_diff, exit_diff, right_left, left_right_diffs in connection_points.values()
})


def solve(*,
          step: int):
    print('*' * 20, f"Step {step}")

    result = 0
    matrix: dict[tuple[int, int], dict[
        tuple[int, int], tuple[tuple[int, int], int, tuple[list[tuple[int, int]], list[tuple[int, int]]]]]] = {}
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
                    (y1, x1), (y2, x2), right_left, left_right_diffs = connection_points[cell]
                    left_points = [(y + y_d, x + x_d)
                                   for y_d, x_d in left_right_diffs[0]]
                    right_points = [(y + y_d, x + x_d)
                                    for y_d, x_d in left_right_diffs[1]]
                    matrix[(y, x)] = {
                        (y + y1, x + x1): ((y + y2, x + x2), right_left, (left_points, right_points)),
                        (y + y2, x + x2): ((y + y1, x + x1), -right_left, (right_points, left_points))}

    if start_coords is None:
        raise ValueError('Missing start point')

    entry_coords = start_coords
    matrix_loop: dict[tuple[int, int], int] = {start_coords: 0}

    loop_right_left = 0
    for y, x in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        exit_coords = (start_coords[0] + y, start_coords[1] + x)
        if start_coords in matrix.get(exit_coords):
            first_exit_coords = exit_coords
            num_steps = 1
            while exit_coords != start_coords:
                matrix_loop[exit_coords] = 0
                num_steps += 1
                (entry_coords,
                 (exit_coords, right_left, left_right_points)) = (exit_coords, matrix[exit_coords][entry_coords])
                loop_right_left += right_left
            if step == 1:
                result = int(num_steps / 2)

            first_entry_coords = entry_coords

            matrix[start_coords] = {}
            (right_left, left_right_diffs) = right_left_turns[((first_entry_coords[0] - start_coords[0],
                                                                first_entry_coords[1] - start_coords[1]),
                                                               (first_exit_coords[0] - start_coords[0],
                                                                first_exit_coords[1] - start_coords[1])
                                                               )]
            left_points = [(start_coords[0] + y_d, start_coords[1] + x_d)
                           for y_d, x_d in left_right_diffs[0]]
            right_points = [(start_coords[0] + y_d, start_coords[1] + x_d)
                            for y_d, x_d in left_right_diffs[1]]

            matrix[start_coords] = {
                first_entry_coords: (first_exit_coords,
                                     right_left,
                                     (left_points, right_points)),
                first_exit_coords: (first_entry_coords,
                                    -right_left,
                                    (right_points, left_points))
            }

            loop_right_left += right_left

            right_turn_loop = loop_right_left > 0

            exit_coords = first_exit_coords
            entry_coords = start_coords
            while exit_coords != start_coords:
                (entry_coords,
                 (exit_coords,
                  right_left,
                  (left_points, right_points))) = (exit_coords, matrix[exit_coords][entry_coords])
                for left_coords in left_points:
                    if left_coords not in matrix_loop:
                        matrix_loop[left_coords] = -1 if right_turn_loop else 1
                for right_coords in right_points:
                    if right_coords not in matrix_loop:
                        matrix_loop[right_coords] = 1 if right_turn_loop else -1

            break

    num_inside = 0
    if step == 2:
        for y in range(num_y):
            inside = False
            for x in range(num_x):
                point = matrix_loop.get((y, x))
                if point is None:
                    if inside:
                        num_inside += 1
                        if print_progress[step - 1]:
                            print('+', end='')
                    else:
                        if print_progress[step - 1]:
                            print(' ', end='')
                elif point < 0:
                    inside = False
                    if print_progress[step-1]:
                        print('-', end='')
                elif point == 0:
                    if print_progress[step-1]:
                        print('0', end='')
                elif point > 0:
                    inside = True
                    num_inside += 1
                    if print_progress[step-1]:
                        print('+', end='')
            if print_progress[step-1]:
                print()
        result = num_inside

    print('*' * 20, f"Step {step}", result)


if __name__ == '__main__':
    solve(step=1)
    solve(step=2)

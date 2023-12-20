from itertools import pairwise
import re

print_progress = [False, False]

re_instruction = re.compile(r'^([RDLU]) (\d+) \((.+)\)$')

directions: dict[str, tuple[int, int]] = {
    'R': (1, 0),
    'D': (0, 1),
    'L': (-1, 0),
    'U': (0, -1)
}
color_directions: dict[str, str] = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U'
}


def solve(*,
          step: int,
          use_shoelace: bool = False):
    print('*' * 20, f"Step {step}")

    instructions: list[tuple[str, int]] = []
    with (open('input.txt', 'r') as input_file):
        for line in input_file.read().splitlines():
            direction, num_meters_str, color = re_instruction.fullmatch(line).groups()
            if step == 1:
                instructions.append((direction, int(num_meters_str)))
            else:
                num_meters = int(color[1:6], 16)
                direction = color_directions[color[6]]
                instructions.append((direction, num_meters))

    dig: dict[tuple[int, int], str] = {}

    def add_left_right():
        if x_add > 0:
            if not dig.get((x, y - 1)):
                dig[(x, y - 1)] = 'L'
            if not dig.get((x, y + 1)):
                dig[(x, y + 1)] = 'R'
        elif x_add < 0:
            if not dig.get((x, y - 1)):
                dig[(x, y - 1)] = 'R'
            if not dig.get((x, y + 1)):
                dig[(x, y + 1)] = 'L'
        elif y_add > 0:
            if not dig.get((x - 1, y)):
                dig[(x - 1, y)] = 'R'
            if not dig.get((x + 1, y)):
                dig[(x + 1, y)] = 'L'
        elif y_add < 0:
            if not dig.get((x - 1, y)):
                dig[(x - 1, y)] = 'L'
            if not dig.get((x + 1, y)):
                dig[(x + 1, y)] = 'R'
        else:
            raise ValueError(f"Invalid direction {direction} x,y change: {x_add},{y_add}")

    x = 0
    y = 0
    if use_shoelace:
        sum_a = 0
        sum_b = 0
        perimeter = 0
        coords: list[tuple[int, int]] = []
        for direction, num_meters in instructions:
            perimeter += num_meters
            x_add, y_add = directions[direction]
            x_new = x + x_add * num_meters
            y_new = y + y_add * num_meters
            coords.append((x_new,y_new))
            sum_a += x * y_new
            sum_b += y * x_new
            x = x_new
            y = y_new

        cubic_meters = int(abs(sum_a - sum_b) / 2 + perimeter / 2 + 1)
    else:
        for index_instruction, (direction, num_meters) in enumerate(instructions):
            x_add, y_add = directions[direction]
            for index_meter in range(num_meters):
                if index_meter == 0:
                    add_left_right()

                x += x_add
                y += y_add
                dig[(x, y)] = 'T'

                add_left_right()

        min_x = min(coords[0] for coords, hole in dig.items())
        max_x = max(coords[0] for coords, hole in dig.items())
        min_y = min(coords[1] for coords, hole in dig.items())
        max_y = max(coords[1] for coords, hole in dig.items())

        right_turn_loop = None

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                hole = dig.get((x, y))
                if hole:
                    if right_turn_loop is None:
                        right_turn_loop = hole == 'L'
                    if print_progress[step - 1]:
                        print(hole, end='')
                    # if hole == 'T':
                    #     print('#', end='')
                else:
                    if print_progress[step - 1]:
                        print(' ', end='')
            if print_progress[step - 1]:
                print()
        if print_progress[step - 1]:
            print()

        if print_progress[step - 1]:
            print(f"It is a {'right' if right_turn_loop else 'left'} turn loop")

        assert dig.get((0, 0), '') == 'T'

        cubic_meters = 0
        for y in range(min_y, max_y + 1):
            inside = False
            for x in range(min_x, max_x + 1):
                hole = dig.get((x, y))
                if hole is None:
                    if inside:
                        cubic_meters += 1
                    if print_progress[step - 1]:
                        if inside:
                            print('.', end='')
                        else:
                            print(' ', end='')
                elif hole == 'T':
                    inside = True
                    cubic_meters += 1
                    if print_progress[step - 1]:
                        print('#', end='')
                    continue
                elif hole == 'L':
                    if inside and not right_turn_loop:
                        cubic_meters += 1
                    if print_progress[step - 1]:
                        if inside and not right_turn_loop:
                            print('.', end='')
                        else:
                            print(' ', end='')
                    if inside and right_turn_loop:
                        inside = False
                elif hole == 'R':
                    if inside and right_turn_loop:
                        cubic_meters += 1
                    if print_progress[step - 1]:
                        if inside and right_turn_loop:
                            print('.', end='')
                        else:
                            print(' ', end='')
                    if inside and not right_turn_loop:
                        inside = False

            if print_progress[step - 1]:
                print()

    result = cubic_meters

    # if step == 1:
    #     assert result == 39194

    print('*' * 20, f"Step {step}", result)


if __name__ == '__main__':
    solve(step=1)
    solve(step=1, use_shoelace=True)
    solve(step=2, use_shoelace=True)

print_progress = [False, False]

coords_directions = {
    1: (1, 0),
    2: (0, 1),
    4: (-1, 0),
    8: (0, -1),
}

tiles_exit_directions = {
    1: {'-': (1,), '|': (2, 8), '/': (8,), '\\': (2,), '.': (1,)},
    2: {'-': (1, 4), '|': (2,), '/': (4,), '\\': (1,), '.': (2,)},
    4: {'-': (4,), '|': (2, 8), '/': (2,), '\\': (8,), '.': (4,)},
    8: {'-': (1, 4), '|': (8,), '/': (1,), '\\': (4,), '.': (8,)},
}


def solve(*,
          step: int):
    print('*' * 20, f"Step {step}")

    tiles: list[str] = []
    with (open('input.txt', 'r') as input_file):
        for index_line, line in enumerate(input_file.read().splitlines()):
            tiles.append(line)

    directions: list[list[int]]

    def light_beam(*,
                   coords: tuple[int, int],
                   entry_direction: int):
        while True:
            x, y = coords
            if x < 0 or y < 0:
                return
            try:
                if directions[y][x] & entry_direction:
                    return
            except IndexError:
                return
            directions[y][x] |= entry_direction
            tile = tiles[y][x]
            exit_directions = tiles_exit_directions[entry_direction][tile]
            entry_direction = exit_directions[0]
            coords = (x + coords_directions[entry_direction][0],
                      y + coords_directions[entry_direction][1])
            for exit_direction in exit_directions[1:]:
                light_beam(
                        coords=(x + coords_directions[exit_direction][0],
                                y + coords_directions[exit_direction][1]),
                        entry_direction=exit_direction)

    if step == 1:
        directions = [[0] * len(line)
                      for line in tiles]
        light_beam(coords=(0, 0),
                   entry_direction=1)

        if print_progress[step - 1]:
            print('\n'.join(''.join(hex(direction)[2]
                                    for direction in directions_y)
                            for directions_y in directions))

        result = sum([bool(direction)
                      for directions_y in directions
                      for direction in directions_y])
    else:
        result = 0
        for y in range(0, len(tiles)):
            directions = [[0] * len(line)
                          for line in tiles]
            light_beam(coords=(0, y),
                       entry_direction=1)
            result = max(result,
                         sum([bool(direction)
                              for directions_y in directions
                              for direction in directions_y]))

            directions = [[0] * len(line)
                          for line in tiles]
            light_beam(coords=(len(tiles[0]) - 1, y),
                       entry_direction=4)
            result = max(result,
                         sum([bool(direction)
                              for directions_y in directions
                              for direction in directions_y]))
        for x in range(0, len(tiles[0])):
            directions = [[0] * len(line)
                          for line in tiles]
            light_beam(coords=(x, 0),
                       entry_direction=2)
            result = max(result,
                         sum([bool(direction)
                              for directions_y in directions
                              for direction in directions_y]))

            directions = [[0] * len(line)
                          for line in tiles]
            light_beam(coords=(x, len(tiles) - 1),
                       entry_direction=8)
            result = max(result,
                         sum([bool(direction)
                              for directions_y in directions
                              for direction in directions_y]))

    print('*' * 20, f"Step {step}", result)


if __name__ == '__main__':
    solve(step=1)
    solve(step=2)

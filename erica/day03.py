import re
from functools import reduce

from utils.input_reader import read_input

PUZZLE_INPUT: list[str] = read_input("inputs/day03.txt").splitlines()


def get_all_coords_adjacent_to_symbols() -> tuple[list[tuple], dict]:
    directions = [(-1, -1), (1, 1), (1, -1), (-1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]

    adjacent_coords = []
    possible_gear = {}
    for y, line in enumerate(PUZZLE_INPUT):
        for x, character in enumerate(line):
            if not character.isdigit() and character != '.':
                for direction in directions:
                    adjacent_coords.append((y+direction[0], x+direction[1]))

            if character == "*":
                tmp_list = []
                for direction in directions:
                    tmp_list.append((y+direction[0], x+direction[1]))
                possible_gear[(x, y)] = tmp_list

    return adjacent_coords, possible_gear


def find_engine_parts(adjacent_coords: list[tuple], pos_gears) -> tuple[list[int], dict]:
    engine_part_list = []
    gears_dict = {}

    for y, line in enumerate(PUZZLE_INPUT):
        numbers_in_line = re.finditer(r'\d+', line)
        for number in numbers_in_line:
            number_start_index = number.start()
            number_end_index = number.end()
            for x in range(number_start_index, number_end_index):
                for gear in pos_gears:
                    if (y, x) in pos_gears[gear]:
                        gears_dict[gear] = gears_dict.get(gear, []) + [int(number.group())]
                if (y, x) in adjacent_coords:
                    engine_part_list.append(int(number.group()))
                    break

    return engine_part_list, gears_dict


coords_adjacent_to_symbols, maybe_gears = get_all_coords_adjacent_to_symbols()
engine_parts, gears = find_engine_parts(adjacent_coords=coords_adjacent_to_symbols, pos_gears=maybe_gears)
sum_gear_ratios = sum(reduce(lambda x, y: x * y, gear_values) for gear_values in gears.values() if len(gear_values) > 1)

print(f"Solution 1: {sum(engine_parts)}")
print(f"Solution 2: {sum_gear_ratios}")

# Solution 1: 533784
# Solution 2: 78826761

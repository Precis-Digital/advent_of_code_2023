import re
from collections import defaultdict

from shared import utils

LIMITS = {"red": 12, "green": 13, "blue": 14}


def main() -> None:
    games = utils.read_input_to_string().splitlines()
    sum_possible, power = 0, 0
    for i, game in enumerate(games):
        color_numbers = defaultdict(int)
        for subset in game.split(";"):
            matches = re.findall(r"(\d+)\s+(\w+)", subset)
            for match in matches:
                number, color = match
                if color in color_numbers:
                    color_numbers[color] = max(color_numbers[color], int(number))
                else:
                    color_numbers[color] = int(number)

        for color, number in color_numbers.items():
            if number > LIMITS[color]:
                break
        else:
            sum_possible += i + 1

        power += color_numbers["red"] * color_numbers["green"] * color_numbers["blue"]

    print(f"Part 1: {sum_possible}")
    print(f"Part 2: {power}")


if __name__ == "__main__":
    main()

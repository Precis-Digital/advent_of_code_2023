import re

from shared import utils

NUM_MAP = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

REGEX_NUMS = r"\d"
REGEX_LETTERS_NUMS = f"{'|'.join(NUM_MAP.keys())}|{REGEX_NUMS}"


def calibration_value(line: str, regex: str) -> int:
    matches = re.finditer(f"(?=({regex}))", line)
    digits = [match.group(1) for match in matches]
    first, last = digits[0], digits[-1]

    first = NUM_MAP[first] if first in NUM_MAP else first
    last = NUM_MAP[last] if last in NUM_MAP else last

    return int(f"{first}{last}")


def part1(lines: list[str]) -> int:
    return sum(calibration_value(line=line, regex=REGEX_NUMS) for line in lines)


def part2(lines: list[str]) -> int:
    return sum(calibration_value(line=line, regex=REGEX_LETTERS_NUMS) for line in lines)


def main() -> None:
    lines = utils.read_input_to_string().splitlines()

    print(f"Part 1: {part1(lines=lines)}")
    print(f"Part 2: {part2(lines=lines)}")


if __name__ == "__main__":
    main()

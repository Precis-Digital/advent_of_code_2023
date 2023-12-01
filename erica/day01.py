from utils.input_reader import read_input

puzzle_input = read_input("inputs/day01.txt").split("\n")

NUMBER_DICT = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def find_integer(calibration: str, reverse=False) -> str:
    calibration_iter = calibration[::-1] if reverse else calibration
    for value in calibration_iter:
        if value.isdigit():
            return value


def find_integer_or_spelled_out_number(calibration: str, reverse=False) -> str:
    calibration_iter = enumerate(calibration[::-1] if reverse else calibration)
    for i, value in calibration_iter:
        if value.isdigit():
            return value
        else:
            for spelled_out_number in NUMBER_DICT.keys():
                initial = -1 if reverse else 0
                if value == spelled_out_number[initial]:
                    length_of_spelled_out_number = len(spelled_out_number)
                    segment = (
                        calibration[i : i + length_of_spelled_out_number]
                        if not reverse
                        else calibration[::-1][i : i + length_of_spelled_out_number][
                            ::-1
                        ]
                    )
                    if segment == spelled_out_number:
                        return str(NUMBER_DICT[spelled_out_number])


def calculate_total(calibration_values: list[str], solution_function) -> int:
    """Calculate and print the total of the first and last numbers in each calibration string."""
    total = 0
    for calibration_value in calibration_values:
        first_number = solution_function(calibration_value)
        last_number = solution_function(calibration_value, reverse=True)
        total += int(first_number + last_number)
    return total


print(f"Solution 1: {calculate_total(puzzle_input, find_integer)}")
print(f"Solution 2: {calculate_total(puzzle_input, find_integer_or_spelled_out_number)}")

# Solution 1: 56042
# Solution 2: 55358

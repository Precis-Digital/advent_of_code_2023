import time


def open_file(file_name):
    with open(file_name, "r") as f:
        return f.read().splitlines()


SYMBOLS = ["/", "#", "@", "*", "-", "+", "&", "$", "%", "="]


def get_symbol_coordinates(lines):
    coordinates = []
    for y, line in enumerate(lines):
        for x, symbol in enumerate(line):
            if symbol in SYMBOLS:
                coordinates.append((x, y))
    return coordinates


def remove_symbols_from_lines(lines, ignore_symbol=None):
    new_lines = []
    for line in lines:
        new_line = []
        for symbol in line:
            if symbol in SYMBOLS and symbol != ignore_symbol:
                new_line.append(".")
            else:
                new_line.append(symbol)
        new_lines.append(new_line)

    return new_lines


def validate_number(number_coordinates, symbol_coordinates):
    is_valid = False
    for number_coordinate in number_coordinates:
        x, y = number_coordinate
        if (x - 1, y) in symbol_coordinates:
            is_valid = True
        elif (x + 1, y) in symbol_coordinates:
            is_valid = True
        elif (x, y - 1) in symbol_coordinates:
            is_valid = True
        elif (x, y + 1) in symbol_coordinates:
            is_valid = True
        elif (x - 1, y - 1) in symbol_coordinates:
            is_valid = True
        elif (x - 1, y + 1) in symbol_coordinates:
            is_valid = True
        elif (x + 1, y - 1) in symbol_coordinates:
            is_valid = True
        elif (x + 1, y + 1) in symbol_coordinates:
            is_valid = True

    return is_valid


def task_one(sample=False):
    start = time.time()
    if sample:
        lines = open_file("Sample.txt")
    else:
        lines = open_file("Input.txt")

    coordinates = get_symbol_coordinates(lines)
    lines_without_symbols = remove_symbols_from_lines(lines)

    validated_numbers = []

    for y, line in enumerate(lines_without_symbols):
        current_number_xes = []
        for x, character in enumerate(line):
            if character == ".":
                if current_number_xes:
                    is_valid = validate_number(
                        [(coordx, y) for coordx in current_number_xes], coordinates
                    )

                    if is_valid:
                        validated_numbers.append(
                            int(
                                "".join(
                                    [line[valid_x] for valid_x in current_number_xes]
                                )
                            )
                        )
                current_number_xes = []
            else:
                current_number_xes.append(x)

        if current_number_xes:
            is_valid = validate_number(
                [(coordx, y) for coordx in current_number_xes], coordinates
            )

            if is_valid:
                validated_numbers.append(
                    int("".join([line[valid_x] for valid_x in current_number_xes]))
                )

        current_number_xes = []

    answer = sum(validated_numbers)

    print(
        f"Task One - {round((time.time() - start) * 1000, 2)}ms - Solution: {answer}"
        + (" (sample)" if sample else "")
    )


def get_star_coordinates(lines):
    coordinates = []
    for y, line in enumerate(lines):
        for x, symbol in enumerate(line):
            if symbol == "*":
                coordinates.append((x, y))
    return coordinates


def determine_number_from_single_digit_coordinate(coordinate, line):
    x, y = coordinate

    number_characters = []

    iterator = 0

    # Go left first to find the start of the number
    while True:
        if line[x + iterator - 1] in [".", "*"] or x + iterator == 0:
            break
        iterator -= 1
    # Now we know the start of the number - iterate until we find the end
    while True:
        if x + iterator == len(line) or line[x + iterator] in [".", "*"]:
            break

        number_characters.append(line[x + iterator])
        iterator += 1
    return int("".join(number_characters))


def get_adjacent_numbers(star_coordinate, lines):
    x, y = star_coordinate
    adjacent_numbers = []

    minus_one_numbers = []
    equal_numbers = []
    plus_one_numbers = []

    if lines[y][x - 1] != ".":
        adjacent_number = determine_number_from_single_digit_coordinate(
            (x - 1, y), lines[y]
        )
        if adjacent_number not in equal_numbers:
            adjacent_numbers.append(adjacent_number)

        equal_numbers.append(adjacent_number)

    if lines[y][x + 1] != ".":
        adjacent_number = determine_number_from_single_digit_coordinate(
            (x + 1, y), lines[y]
        )
        if adjacent_number not in equal_numbers:
            adjacent_numbers.append(adjacent_number)

        equal_numbers.append(adjacent_number)

    if lines[y - 1][x] != ".":
        adjacent_number = determine_number_from_single_digit_coordinate(
            (x, y - 1), lines[y - 1]
        )
        if adjacent_number not in minus_one_numbers:
            adjacent_numbers.append(adjacent_number)

        minus_one_numbers.append(adjacent_number)

    if lines[y - 1][x - 1] != ".":
        adjacent_number = determine_number_from_single_digit_coordinate(
            (x - 1, y - 1), lines[y - 1]
        )
        if adjacent_number not in minus_one_numbers:
            adjacent_numbers.append(adjacent_number)

        minus_one_numbers.append(adjacent_number)

    if lines[y - 1][x + 1] != ".":
        adjacent_number = determine_number_from_single_digit_coordinate(
            (x + 1, y - 1), lines[y - 1]
        )
        if adjacent_number not in minus_one_numbers:
            adjacent_numbers.append(adjacent_number)

        minus_one_numbers.append(adjacent_number)

    if lines[y + 1][x - 1] != ".":
        adjacent_number = determine_number_from_single_digit_coordinate(
            (x - 1, y + 1), lines[y + 1]
        )
        if adjacent_number not in plus_one_numbers:
            adjacent_numbers.append(adjacent_number)

        plus_one_numbers.append(adjacent_number)

    if lines[y + 1][x + 1] != ".":
        adjacent_number = determine_number_from_single_digit_coordinate(
            (x + 1, y + 1), lines[y + 1]
        )
        if adjacent_number not in plus_one_numbers:
            adjacent_numbers.append(adjacent_number)

        plus_one_numbers.append(adjacent_number)

    if lines[y + 1][x] != ".":
        adjacent_number = determine_number_from_single_digit_coordinate(
            (x, y + 1), lines[y + 1]
        )
        if adjacent_number not in plus_one_numbers:
            adjacent_numbers.append(adjacent_number)

        plus_one_numbers.append(adjacent_number)

    return adjacent_numbers


def task_two(sample=False):
    start = time.time()
    if sample:
        lines = open_file("Sample.txt")
    else:
        lines = open_file("Input.txt")

    star_coordinates = get_star_coordinates(lines)
    lines_without_symbols = remove_symbols_from_lines(lines, "*")

    gears = []

    for star_coordinate in star_coordinates:
        adjacent_numbers = get_adjacent_numbers(star_coordinate, lines_without_symbols)
        if len(adjacent_numbers) == 2:
            gears.append((adjacent_numbers[0], adjacent_numbers[1]))

    gear_ratios = [gear[0] * gear[1] for gear in gears]

    answer = sum(gear_ratios)

    print(
        f"Task Two - {round((time.time() - start) * 1000, 2)}ms - Solution: {answer}"
        + (" (sample)" if sample else "")
    )


task_one(sample=True)
task_one()

task_two(sample=True)
task_two()

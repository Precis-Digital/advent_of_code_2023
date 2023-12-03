import re


def parse_and_fill_matrix(game_line: str,
                          row: int,
                          pattern: re.Pattern,
                          matrix: dict[tuple],
                          matrix_value=None):
    try:
        for match in pattern.finditer(game_line):
            start, end = match.span()
            if matrix_value is not None:
                if type(matrix_value) is type:
                    for col in range(start, end):
                        matrix[(row, col)] = matrix_value()
                else:
                    for col in range(start, end):
                        matrix[(row, col)] = matrix_value
            else:
                matrix[(row, start, end)] = match.group(1)

    except:
        print('', pattern.pattern)
        print('', game_line)
        raise


def solve_03_01():
    print('*' * 20, 'Step 1')
    re_number = re.compile(r'(\d+)')
    re_symbol = re.compile(r'([^0-9.\r\n]+)')

    symbols: dict[tuple] = {}
    numbers: dict[tuple] = {}

    with (open('input.txt', 'r') as input_file):
        row = 0
        for game_line in input_file:
            parse_and_fill_matrix(game_line, row, re_number, numbers)
            parse_and_fill_matrix(game_line, row, re_symbol, symbols, True)
            row += 1

    result = 0
    for (row, start, end), number in numbers.items():
        if symbols.get((row, start - 1)) or symbols.get((row, end)):
            result += int(number)
        else:
            for col in range(start - 1, end + 1):
                if (symbols.get((row - 1, col))
                        or symbols.get((row + 1, col))):
                    result += int(number)
                    break

    print('*' * 20, 'Step 1', result)


def add_number_to_gear(gears: dict[tuple],
                       coords: tuple,
                       number: int):
    if coords in gears:
        gears[coords].append(int(number))


def solve_03_02():
    print('*' * 20, 'Step 2')
    re_number = re.compile(r'(\d+)')
    re_gear = re.compile(r'(\*)')

    gears: dict[tuple] = {}
    numbers: dict[tuple] = {}

    with (open('input.txt', 'r') as input_file):
        row = 0
        for game_line in input_file:
            parse_and_fill_matrix(game_line, row, re_number, numbers)
            parse_and_fill_matrix(game_line, row, re_gear, gears, list)
            row += 1

    result = 0
    for (row, start, end), number in numbers.items():
        add_number_to_gear(gears, (row, start - 1), number)
        add_number_to_gear(gears, (row, end), number)
        for col in range(start - 1, end + 1):
            add_number_to_gear(gears, (row - 1, col), number)
            add_number_to_gear(gears, (row + 1, col), number)

    for (row, col), gear_numbers in gears.items():
        if len(gear_numbers) == 2:
            result += gear_numbers[0] * gear_numbers[1]
        else:
            print('', row + 1, col + 1, gear_numbers)

    print('*' * 20, 'Step 2', result)


if __name__ == '__main__':
    solve_03_01()
    solve_03_02()

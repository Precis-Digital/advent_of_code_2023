import re

re_end_line = re.compile(r'\r?\n?$')
re_winning = re.compile(r'\b(\d+)(?=\b[^:]*\|.*\b\1\b)')
re_digits = re.compile(r'\d(?=\s|$)')


def print_game_line(game_line: str,
                    winning_numbers: list[str]):
    print(game_line)
    replaced_game_line = game_line
    for index, number in enumerate(winning_numbers):
        replaced_game_line = re.sub(number.rjust(2) + r'(?=\s|$)',
                                    chr(65 + index).rjust(2),
                                    replaced_game_line)
    replaced_game_line = re_digits.sub(' ', re_digits.sub(' ', replaced_game_line))
    print(replaced_game_line)


def solve_04_01(print_progress: bool = False):
    print('*' * 20, 'Step 1')

    result = 0
    num_cards = 0
    with (open('input.txt', 'r') as input_file):
        for game_line in input_file:
            game_line = re_end_line.sub('', game_line)
            num_cards += 1
            winning_numbers = re_winning.findall(game_line)
            if print_progress:
                print_game_line(game_line, winning_numbers)
            num_winning_numbers = len(winning_numbers)
            if num_winning_numbers:
                result += int(2 ** (num_winning_numbers - 1))
            if print_progress:
                print(str(num_cards).rjust(5), str(num_winning_numbers).rjust(4))

    print('*' * 20, 'Step 1', result)


def solve_04_02(print_progress: bool = False):
    print('*' * 20, 'Step 1')

    num_cards = 0
    num_duplicate_cards = 0
    duplicate_next_lines = []
    card = 0
    with (open('input.txt', 'r') as input_file):
        for game_line in input_file:
            game_line = re_end_line.sub('', game_line)
            card += 1
            num_duplicate = duplicate_next_lines.pop(0) if len(duplicate_next_lines) else 0
            num_cards += 1
            num_duplicate_cards += num_duplicate
            winning_numbers = re_winning.findall(game_line)
            if print_progress:
                print_game_line(game_line, winning_numbers)
            num_winning_numbers = len(winning_numbers)
            times_card = num_duplicate + 1
            if num_winning_numbers:
                # result += int(2 ** (num_winning_numbers - 1)) * times_card
                duplicate_next_lines = [
                    duplicate_next_lines[index] + times_card
                    if index < len(duplicate_next_lines) and index < num_winning_numbers
                    else duplicate_next_lines[index] if index < len(duplicate_next_lines)
                    else times_card
                    for index in range(max(num_winning_numbers,
                                           len(duplicate_next_lines)))]
            if print_progress:
                print(str(card).rjust(5),
                      str(times_card).rjust(8),
                      str(num_winning_numbers).rjust(4),
                      str(num_duplicate_cards).rjust(10),
                      duplicate_next_lines)

    print('*' * 20, 'Step 2', num_cards + num_duplicate_cards)


if __name__ == '__main__':
    solve_04_01()
    solve_04_02()

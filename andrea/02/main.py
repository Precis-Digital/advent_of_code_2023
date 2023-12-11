import re


def solve_01():
    print('*' * 20, 'Step 1')
    bag = {'red': 12,
           'green': 13,
           'blue': 14}
    re_game = re.compile(r'Game (\d+)[;:] (.+)')
    re_extraction = re.compile(r'(\d+) (' + '|'.join(bag.keys()) + r')')
    with (open('input.txt', 'r') as input_file):
        result = 0
        for game_line in input_file:
            try:
                game_id, extractions = re_game.findall(game_line)[0]
                game_possible = True
                for extraction in extractions.split('; '):
                    for color_num, color in re_extraction.findall(extraction):
                        if int(color_num) > bag[color]:
                            game_possible = False
                            break
                    if not game_possible:
                        break
                if game_possible:
                    result += int(game_id)
            except:
                print(game_line)
                raise
        print('*' * 20, 'Step 1', result)


def solve_02():
    print('*' * 20, 'Step 2')
    colors = ['red',
              'green',
              'blue']
    re_game = re.compile(r'Game (\d+)[;:] (.+)')
    re_extraction = re.compile(r'(\d+) (' + '|'.join(colors) + r')')
    with (open('input.txt', 'r') as input_file):
        result = 0
        for game_line in input_file:
            try:
                bag = {color: 0 for color in colors}
                game_id, extractions = re_game.findall(game_line)[0]
                for extraction in extractions.split('; '):
                    for color_num, color in re_extraction.findall(extraction):
                        bag[color] = max(bag[color], int(color_num))
                game_power = 1
                for color in colors:
                    game_power *= bag[color]
                result += game_power
            except:
                print(game_line)
                raise
        print('*' * 20, 'Step 2', result)


if __name__ == '__main__':
    solve_01()
    solve_02()

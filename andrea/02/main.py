import re


def solve_02_01():
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


def solve_02_02():
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
    solve_02_01()
    solve_02_02()

# Output
# 
# ******************** Step 1
# ******************** Step 1 55090
# ******************** Step 2
#  Fail Single RE 2,one - 2,eight
#  2fourseven1oneights
#
#  Fail Single RE 4,two - 4,one
#  4one1eightzgcpkgbpgmsevenninetwonetk
#
#  Fail Single RE five,eight - five,two
#  fivebsvvnhgcp6jdqrcfreightwohfh
#
#  Fail Single RE nine,two - nine,one
#  ninebfour26fivetwonem
#
#  Fail Single RE 5,eight - 5,two
#  518sixeightwop
#
#  Fail Single RE 4,one - 4,eight
#  ssphtp472xjfvlvzdl9oneightg
#
#  Fail Single RE 3,eight - 3,two
#  q35bvblmmqhmnine5zeightwoj
#
#  Fail Single RE 1,two - 1,one
#  1threesix76tv4twonetgv
#
#  Fail Single RE eight,eight - eight,two
#  eighttwothree9247twoeightwoxsq
#
#  Fail Single RE 6,two - 6,one
#  6eight6two2threetwoneg
#
#  Fail Single RE 8,one - 8,eight
#  8zfgtfnxvjjxgptxkpkdb1gkndcsbgvzxgqg1oneightq
#
#  Fail Single RE four,eight - four,two
#  four6eightwokqz
#
#  Fail Single RE 3,eight - 3,two
#  nrzpqk3fivesldclpcbfmdtbbhpxonethreeeightwor
#
#  Fail Single RE 5,two - 5,one
#  pfvqrm54mhvzmqmgtwoneckj
#
#  Fail Single RE 6,two - 6,one
#  qvcxfrjgm6threetwoeighttwoneg
#
#  Fail Single RE 1,two - 1,one
#  1gdghnzhqlseveneightsixsevenmblqvjpxd8twonejm
#
#  Fail Single RE 1,two - 1,one
#  clrgvbgcbb1twonekgr
#
#  Fail Single RE 2,eight - 2,two
#  2ninexblcgmhxxceightwop
#
#  Fail Single RE eight,eight - eight,two
#  qdhfqqeightone3595one8eightwov
#
#  Fail Single RE 9,eight - 9,two
#  93twoeightwoff
#
#  Fail Single RE four,eight - four,two
#  mnthlsxffourfour6threezcqeightwosk
#
#  Fail Single RE five,one - five,eight
#  fivefour9bcslbnr9fourtwotnzqshcvoneightnz
#
#  Fail Single RE 5,one - 5,eight
#  5jlkfmtwoseventhreeoneightbsr
#
#  Fail Single RE 6,one - 6,eight
#  6oneighthlf
#
# ******************** Step 2 54845
#
# Process finished with exit code 0

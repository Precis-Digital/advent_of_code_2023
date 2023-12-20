import re


def solve_1():
    print('*' * 20, 'Step 1')
    re_digits = re.compile(r'(\d)')
    with open('input.txt', 'r') as input_file:
        result = 0
        for line in input_file:
            digits = re_digits.findall(line)
            try:
                result += int(digits[0]) * 10 + int(digits[-1])
            except:
                print(line)
                raise

        print('*' * 20, 'Step 1', result)


def solve_2():
    print('*' * 20, 'Step 2')
    eng_digits = ['zero',
                  'one',
                  'two',
                  'three',
                  'four',
                  'five',
                  'six',
                  'seven',
                  'eight',
                  'nine']
    dict_eng_digits = {}
    for index, key in enumerate(eng_digits):
        dict_eng_digits[key] = index
        dict_eng_digits[str(index)] = index
    re_first_digit = re.compile(r'(\d|' + '|'.join(eng_digits) + r')')
    re_last_digit = re.compile(r'.*(\d|' + '|'.join(eng_digits) + r')')
    with (open('input.txt', 'r') as input_file):
        result = 0
        for line in input_file:
            try:
                digits = re_first_digit.findall(line)
                single_re_result = (dict_eng_digits[digits[0]] * 10
                                    + dict_eng_digits[digits[-1]])
                split_re_result = (dict_eng_digits[re_first_digit.search(line)[1]] * 10
                                   + dict_eng_digits[re_last_digit.match(line)[1]])
                if single_re_result != split_re_result:
                    print('', f'Fail Single RE {digits[0]},{digits[-1]} - {re_first_digit.search(line)[1]}'
                              f',{re_last_digit.match(line)[1]}')
                    print('', line)
                result += split_re_result
            except:
                print(line)
                raise
        print('*' * 20, 'Step 2', result)


if __name__ == '__main__':
    solve_1()
    solve_2()

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
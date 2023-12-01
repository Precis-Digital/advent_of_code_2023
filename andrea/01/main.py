import re


def solve_01_1():
    re_digits = re.compile(r'(\d)')
    with open('input_01.txt', 'r') as input_file:
        result = 0
        for line in input_file:
            digits = re_digits.findall(line)
            try:
                result += int(digits[0]) * 10 + int(digits[-1])
            except:
                print(line)
                raise

        print(result)


def solve_01_2():
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
    with (open('input_01.txt', 'r') as input_file):
        result = 0
        for line in input_file:
            try:
                result += (dict_eng_digits[re_first_digit.search(line)[1]] * 10
                           + dict_eng_digits[re_last_digit.match(line)[1]])
            except:
                print(line)
                raise
        print(result)


if __name__ == '__main__':
    solve_01_1()
    solve_01_2()

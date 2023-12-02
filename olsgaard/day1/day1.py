import re

input = open("olsgaard\day1\input.txt", "r").read()



text_to_numbers = {"one": "o1e", "two": "t2o", "three": "t3e", "four": "f4r", "five": "f5e", "six": "s6x", "seven": "s7n", "eight": "e8t", "nine": "n9e"}


for key in text_to_numbers.keys():
    input = input.replace(key, text_to_numbers[key])

input = input.splitlines()

digits_only = []
for string in input:
    string = re.sub("\D", "", string)
    digits_only.append(string)

summed_numbers = 0

for number in digits_only:
    summed_numbers += int(number[0] + number[-1])

print(summed_numbers)




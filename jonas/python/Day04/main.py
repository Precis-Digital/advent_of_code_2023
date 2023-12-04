import time


def open_file(file_name):
    with open(file_name, "r") as f:
        return f.read().splitlines()


def extract_numbers(number_string):
    numbers = []

    for i in range(len(number_string)):
        if i % 3 == 0:
            number = number_string[1 * i : 1 * (i + 1) + 1]
            numbers.append(number.replace(" ", "0"))

    return numbers


def get_winning_numbers_count(line):
    card_numbers = line.split(": ")[1]

    winning_numbers = extract_numbers(card_numbers.split(" | ")[0])
    my_numbers = extract_numbers(card_numbers.split(" | ")[1])

    winning_count = len(set(winning_numbers).intersection(set(my_numbers)))

    return winning_count


def task_one(sample=False):
    start = time.time()
    if sample:
        lines = open_file("Sample.txt")
    else:
        lines = open_file("Input.txt")

    winning_numbers = [get_winning_numbers_count(line) for line in lines]
    solution = 0

    for winning_number_count in winning_numbers:
        card_value = 0
        for index in range(winning_number_count):
            if index == 0:
                card_value = 1
            else:
                card_value *= 2
        solution += card_value

    answer = solution

    print(
        f"Task One - {round((time.time() - start) * 1000, 2)}ms - Solution: {answer}"
        + (" (sample)" if sample else "")
    )


def task_two(sample=False):
    start = time.time()
    if sample:
        lines = open_file("Sample.txt")
    else:
        lines = open_file("Input.txt")

    winning_card_numbers_map = {
        card_num: 0
        for card_num in [
            int(card.split(": ")[0].replace("Card ", "")) for card in lines
        ]
    }

    cache = {}

    for index, card in reversed(list(enumerate(lines))):
        card_num = int(card.split(": ")[0].replace("Card ", ""))
        winning_numbers = get_winning_numbers_count(card)
        winning_card_numbers_map[card_num] += 1

        for i in range(winning_numbers):
            winning_card_numbers_map[card_num] += cache[card_num + i]
        cache[index] = winning_card_numbers_map[index + 1]

    answer = sum(winning_card_numbers_map.values())

    print(
        f"Task Two - {round((time.time() - start) * 1000, 2)}ms - Solution: {answer}"
        + (" (sample)" if sample else "")
    )


task_one(sample=True)
task_one()

task_two(sample=True)
task_two()

import re

from utils.input_reader import read_input

puzzle_input = read_input("inputs/day04.txt").split("\n")

pattern = r"Card\s*\d+"


def parse_cards(list_of_scratch_cards: list[str]) -> list[tuple]:
    cards = []
    for card in list_of_scratch_cards:
        card_number = re.search(pattern, card).group()
        card = card.replace(f"{card_number}: ", "")
        split_card_number = card.split(" | ")
        winning_numbers = [
            int(item) for item in split_card_number[0].split(" ") if item.isdigit()
        ]
        elfs_numbers = [
            int(item) for item in split_card_number[1].split(" ") if item.isdigit()
        ]
        cards.append((card_number, winning_numbers, elfs_numbers))
    return cards


def calculate_points_in_cards(cards: list[tuple]) -> int:
    points_per_card = []
    for card in cards:
        card_point = 0
        for elf_number in card[2]:
            if elf_number in card[1]:
                if card_point == 0:
                    card_point = 1
                else:
                    card_point = card_point * 2
        points_per_card.append(card_point)
    return sum(points_per_card)


def get_number_of_total_cards_after_scratched(cards: list[tuple]) -> int:
    card_count = {}
    for i, card in enumerate(cards):
        matches = 0
        if card_count.get(i):
            card_count[i] += 1
            multiplier = card_count.get(i)
        else:
            card_count[i] = 1
            multiplier = 1
        for elf_number in card[2]:
            if elf_number in card[1]:
                matches += 1
        for j in range(i + 1, (i + 1) + matches):
            if card_count.get(j):
                card_count[j] += 1 * multiplier
            else:
                card_count[j] = 1 * multiplier
    return sum(card_count.values())


parsed_cards = parse_cards(list_of_scratch_cards=puzzle_input)
print(f"Solution 1: {calculate_points_in_cards(cards=parsed_cards)}")
print(f"Solution 2: {get_number_of_total_cards_after_scratched(cards=parsed_cards)}")

# solution 1 32609
# solution 2 14624680

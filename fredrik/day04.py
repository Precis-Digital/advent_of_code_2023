import re
from collections import deque

from shared import utils

Card = set[int]


def parse_card(card: str) -> tuple[Card, Card]:
    numbers = re.findall(r"Card\s+\d+:\s+([\d\s|]+)", card)[0]
    winning, actual = numbers.split("|")
    return set(winning.split()), set(actual.split())


def get_score(matches: int) -> int:
    if matches == 0:
        return 0

    return 2 ** (matches - 1)


def scratch_cards(card_stack: deque[int], match_table: dict[int, int]) -> int:
    total_scratch_cards = 0
    while card_stack:
        card_nr = card_stack.popleft()
        total_scratch_cards += 1

        matches = match_table[card_nr]
        for i in range(1, matches + 1):
            card_stack.append(card_nr + i)

    return total_scratch_cards


def main() -> None:
    cards = utils.read_input_to_string().splitlines()
    score, match_table, card_stack = 0, {}, deque()
    for i, card in enumerate(cards):
        card_stack.append(i + 1)
        winning, actual = parse_card(card)
        match_table[i + 1] = len(winning & actual)
        score += get_score(matches=match_table[i + 1])

    total_scratch_cards = scratch_cards(card_stack=card_stack, match_table=match_table)

    print(f"Part 1: {score}")
    print(f"Part 2: {total_scratch_cards}")


if __name__ == "__main__":
    main()

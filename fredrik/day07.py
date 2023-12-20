from __future__ import annotations

import collections
import dataclasses
import enum
import functools

from shared import utils

BROADWAY_MAP = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}


@functools.total_ordering
class Card:
    def __init__(self, str_repr: str, /, jokers: bool = False) -> None:
        if value := BROADWAY_MAP.get(str_repr):
            self.value = 1 if jokers and str_repr == "J" else value
        else:
            self.value = int(str_repr)

    def __gt__(self, other: Card) -> bool:
        return self.value > other.value

    def __eq__(self, other: Card) -> bool:
        return self.value == other.value


class HandType(enum.Enum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0


@dataclasses.dataclass(frozen=True)
@functools.total_ordering
class Hand:
    bid: int
    cards: tuple[Card, ...]

    @functools.cached_property
    def type(self) -> HandType:
        counts = collections.Counter((card.value for card in self.cards))

        if (jokers := counts.pop(1, 0)) == 5:
            return HandType.FIVE_OF_A_KIND

        max_counts = max(counts.values()) + jokers if counts else 0
        key, count = counts.most_common()[0]

        counts[key] = count + jokers
        if max_counts == 5:
            return HandType.FIVE_OF_A_KIND

        if max_counts == 4:
            return HandType.FOUR_OF_A_KIND

        if max_counts == 3:
            if 2 in counts.values():
                return HandType.FULL_HOUSE

            return HandType.THREE_OF_A_KIND

        if max_counts == 2:
            if sorted(list(counts.values())) == [1, 2, 2]:
                return HandType.TWO_PAIR

            return HandType.ONE_PAIR

        return HandType.HIGH_CARD

    def __gt__(self, other: Hand) -> bool:
        if self.type is not other.type:
            return self.type.value > other.type.value

        for card1, card2 in zip(self.cards, other.cards):
            if card1 == card2:
                continue
            else:
                return card1 > card2


def parse_hands(data: str, jokers: bool = False) -> list[Hand]:
    hands = []
    for hand in data.splitlines():
        cards, bid = hand.split()
        cards = tuple(Card(card, jokers=jokers) for card in cards)
        hands.append(Hand(bid=int(bid), cards=cards))

    return hands


def calculate_winnings(hands: list[Hand]) -> int:
    total_winnings = 0
    for i, hand in enumerate(hands):
        total_winnings += hand.bid * (i + 1)

    return total_winnings


def part1(data: str) -> int:
    hands = sorted(parse_hands(data))
    return calculate_winnings(hands=hands)


def part2(data: str) -> int:
    hands = sorted(parse_hands(data, jokers=True))
    return calculate_winnings(hands=hands)


def main() -> None:
    data_raw = utils.read_input_to_string()
    total_winnings_part_1 = part1(data=data_raw)
    total_winnings_part_2 = part2(data=data_raw)

    print(f"Part 1: {total_winnings_part_1}")
    print(f"Part 2: {total_winnings_part_2}")


if __name__ == "__main__":
    main()

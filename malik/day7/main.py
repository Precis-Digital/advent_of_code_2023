import re
import math
from collections import Counter



def parse_input(f):
    hands = []
    for row in f:
        cards, bid = row.split()
        hands.append((cards, int(bid)))
    return hands

def hand_type_rank(hand):
    # given a hand returns an integer from 7 to 1 ranking the hand
    ctr = Counter(hand)
    # 5 of a kind
    if len(ctr) == 1:
        return 7
    
    if len(ctr) == 2:
        # 4 of a kind
        if 4 in ctr.values():
            return 6
        # Full house
        if 3 in ctr.values():
            return 5
    
    
    if len(ctr) == 3:
        # has 3 of a kind
        if 3 in ctr.values():
            return 4
        # has 2 pairs, there's at least one par and since there are only 3 unique cards, there must be 2 pairs
        if 2 in ctr.values():
            return 3
    
    # has to have at least one pair
    if len(ctr) == 4:
        return 2
    
    return 1
    
def hex_without_prefix(digit: int) -> str:
    return hex(digit)[2:].upper()

def convert_card_to_hex(card: str, use_jokers = False) -> str:
    mapping = {
        'A': 14,
        'K': 13,
        'Q': 12,
        'J': 11,
        'T': 10,
    }

    if use_jokers:
        mapping['J'] = 0

    if card in mapping:
        return hex_without_prefix(mapping[card])
    return hex_without_prefix(int(card))


def find_best_hand_with_jokers(hand):
    CARDS = 'AKQT98765432'
    best_score = hand_type_rank(hand)
    best_hand = hand
    if 'J' not in hand:
        return best_hand, best_score
    
    for card in CARDS:
        new_hand = hand.replace('J', card)
        new_scoe = hand_type_rank(new_hand)
        if new_scoe > best_score:
            best_score = new_scoe
            best_hand = new_hand
    return best_hand, best_score
 
def hand_rank(hand, use_jokers = False):

    output = []
    if use_jokers:
        _, hand_score = find_best_hand_with_jokers(hand)
    else:
        hand_score = hand_type_rank(hand)

    output.append(convert_card_to_hex(hand_score))
    for card in hand:
        output.append(convert_card_to_hex(card, use_jokers=use_jokers))
    return ''.join(output)


def test_hand_rank():
    print('AAAAA', hand_rank('AAAAA'))
    print('22222', hand_rank('22222'))

    print('AJJJJ', find_best_hand_with_jokers('AAAAJ'))
    print('QQQJA', find_best_hand_with_jokers('QQQJA'))
    print('32T3K', find_best_hand_with_jokers('32T3K'))

def problem1(hands: list[tuple[str, int]]):
    hands.sort(key=lambda x: hand_rank(x[0]), reverse=True)
    return sum((len(hands) - idx) * bid for idx, (_, bid) in enumerate(hands))

def problem2(hands):
    hands.sort(key=lambda x: hand_rank(x[0], use_jokers=True), reverse=True)
    return sum((len(hands) - idx) * bid for idx, (_, bid) in enumerate(hands))

def main(fpath: str):
    with open(fpath, 'r') as f:
       hands = parse_input(f)

    # print(hands)
    test_hand_rank()
    print('Problem 1: ', problem1(hands=hands))
    print('Problem 2: ', problem2(hands=hands))
    return 0


if __name__ == '__main__':
    import sys
    fpath = sys.argv[1]
    print(fpath)
    main(fpath=fpath)
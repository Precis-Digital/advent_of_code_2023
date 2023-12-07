import re

print_progress = False

re_end_line = re.compile(r'\r?\n?$')

cards = {1: ''.join(reversed('AKQJT98765432')),
         2: ''.join(reversed('AKQT98765432J')),
         'no_joker': ''.join(reversed('AKQT98765432'))}

re_hand_bid = re.compile(r'(.....) (\d+)')
re_couple_or_more = {1: re.compile(r'((.)\2+)'),
                     2: re.compile(r'(([^J])\2+)')}
re_jokers = re.compile(r'(J+)')

ranks = [1, 2, 2.2, 3, 3.2, 4, 5]


def solve_06(*,
             step: int):
    print('*' * 20, f"Step {step}")

    hands_bids = []
    with (open('input.txt', 'r') as input_file):
        for game_line in input_file:
            hand, bid = re_hand_bid.match(game_line).groups()
            hand_sorted = ''.join(sorted(hand, key=lambda card: cards[step].index(card)))
            hand_ranked = ''.join(str(cards[step].index(card)).zfill(2) for card in hand)
            couple_or_more = re_couple_or_more[step].findall(hand_sorted)
            jokers = len((re_jokers.findall(hand_sorted) or [''])[0]) if step == 2 else 0
            if couple_or_more:
                couple_or_more.sort(key=lambda match: len(match[0]),
                                    reverse=True)
                score = len(couple_or_more[0][0]) + jokers
                if len(couple_or_more) == 2:
                    score += len(couple_or_more[1][0]) / 10
            else:
                score = min(1 + jokers, 5)
            hands_bids.append((f"{ranks.index(score) + 1}{hand_ranked}", int(bid), hand, hand_sorted))

    hands_bids.sort(key=lambda hand_bid: hand_bid[0])

    result = 0
    for index, (hand_scored, bid, hand, hand_sorted) in enumerate(hands_bids):
        if print_progress:
            print(str(index).rjust(4), hand, hand_sorted, hand_scored, bid)
        result += (index + 1) * bid

    print('*' * 20, f"Step {step}", result)


if __name__ == '__main__':
    solve_06(step=1)
    solve_06(step=2)

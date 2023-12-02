import re

from utils.input_reader import read_input

puzzle_input = read_input("inputs/day02.txt").split("\n")
STONE_LIMITS = {"red": 12, "green": 13, "blue": 14}


def evaluate_rounds(rounds: list[str]) -> tuple[bool, dict[str, int]]:
    game_is_possible = True
    stones_needed = {"red": 0, "green": 0, "blue": 0}
    for game_round in rounds:
        for color, value in STONE_LIMITS.items():
            nr_stones_by_color = re.findall(fr'(\d+)\s+{color}', game_round)
            stones_by_round = sum([int(x) for x in nr_stones_by_color])
            stones_needed[color] = max(stones_needed[color], stones_by_round)
            if stones_by_round > value:
                game_is_possible = False
    return game_is_possible, stones_needed


def find_possible_games_and_power_of_stones(games: list[str]) -> tuple[list[int], list[int]]:
    possible_games = []
    power_of_stones = []
    for game in games:
        rounds_in_game = game.split(";")
        game_is_possible, max_dict = evaluate_rounds(rounds_in_game)

        prod = 1
        for value in max_dict.values():
            prod *= value
        power_of_stones.append(prod)

        if game_is_possible:
            game_key = game.split(":")[0].replace("Game ", "")
            possible_games.append(int(game_key))

    return possible_games, power_of_stones


possible_game_keys, power_of_stones_per_game = find_possible_games_and_power_of_stones(puzzle_input)
print(f"Solution 1: {sum(possible_game_keys)}")
print(f"Solution 2: {sum(power_of_stones_per_game)}")

# Solution 1: 2913
# Solution 2: 55593

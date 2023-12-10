import itertools

from shared import utils


def parse_histories(histories_raw: str) -> list[list[int]]:
    return [[int(n) for n in history.split()] for history in histories_raw.splitlines()]


def calculate_predictions(history: list[int]) -> int:
    current_row, next_row, rows = history, [], [history]
    while any(current_row):
        for val1, val2 in itertools.pairwise(current_row):
            next_row.append(val2 - val1)

        rows.append(next_row)
        current_row, next_row = next_row, []

    return sum(row[-1] for row in rows)


def main() -> None:
    histories_raw = utils.read_input_to_string()
    histories = parse_histories(histories_raw=histories_raw)
    preds1 = (calculate_predictions(history=history) for history in histories)
    preds2 = (calculate_predictions(history=history[::-1]) for history in histories)
    print(f"Part 1: {sum(prediction for prediction in preds1)}")
    print(f"Part 2: {sum(prediction for prediction in preds2)}")


if __name__ == "__main__":
    main()

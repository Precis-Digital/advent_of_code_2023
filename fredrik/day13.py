import dataclasses
import enum
import functools
import itertools
from typing import Self

from shared import utils

Candidate = tuple[int, ...]


class Orientation(enum.Enum):
    ROW = enum.auto()
    COL = enum.auto()


@dataclasses.dataclass
class Pattern:
    rows: tuple[str, ...]
    columns: tuple[str, ...]
    update_index: int = 0
    original_rows: tuple[str, ...] | None = None
    already_used_row_candidate: Candidate | None = None
    already_used_col_candidate: Candidate | None = None

    @classmethod
    def from_raw(cls, pattern_raw: str) -> Self:
        rows = tuple(pattern_raw.splitlines())
        columns = tuple("".join(row) for row in zip(*rows))
        return Pattern(rows=rows, columns=columns)

    def __post_init__(self) -> None:
        self.original_rows = self.rows
        self.original_columns = self.columns

    @property
    def width(self) -> int:
        return len(self.columns)

    @property
    def height(self) -> int:
        return len(self.rows)

    def update_smudge(self) -> None:
        self.rows = self.original_rows

        row_index2, row_index1 = divmod(self.update_index, self.height)
        old_row = self.rows[row_index1]
        old_char = old_row[row_index2]
        new_char = "#" if old_char == "." else "."
        new_row = old_row[:row_index2] + new_char + old_row[row_index2 + 1 :]

        self.rows = self.rows[:row_index1] + (new_row,) + self.rows[row_index1 + 1 :]
        self.columns = tuple("".join(row) for row in zip(*self.rows))
        self.update_index += 1

    @staticmethod
    @functools.cache
    def find_pairs(items: tuple[str, ...]) -> set[Candidate]:
        pairs = set()
        for i, item1 in enumerate(items):
            indicies = [j for j, item2 in enumerate(items) if item1 == item2]
            if len(indicies) > 1:
                for pair in itertools.combinations(indicies, r=2):
                    pairs.add(tuple(sorted(list(pair))))

        return pairs

    def find_reflection_number(self) -> int:
        row_pairs = self.find_pairs(items=self.rows)
        row_candidates = find_reflection_candidates(pairs=row_pairs)
        for candidate in row_candidates:
            if candidate == self.already_used_row_candidate:
                continue

            row_perfect = self.is_perfect_reflection(
                candidate=candidate, orientation=Orientation.ROW
            )

            if row_perfect:
                self.already_used_row_candidate = candidate
                return 100 * (candidate[1])

        col_pairs = self.find_pairs(items=self.columns)
        col_candidates = find_reflection_candidates(pairs=col_pairs)
        for candidate in col_candidates:
            if candidate == self.already_used_col_candidate:
                continue

            col_perfect = self.is_perfect_reflection(
                candidate=candidate, orientation=Orientation.COL
            )
            if col_perfect:
                self.already_used_col_candidate = candidate
                return candidate[1]

        raise ValueError("no perfect reflection")

    def is_perfect_reflection(
        self,
        candidate: Candidate,
        orientation: Orientation,
    ) -> bool:
        if orientation is Orientation.ROW:
            pairs_to_match = min(self.height - candidate[1] - 1, candidate[0])
            values = self.find_pairs(items=self.rows)
        elif orientation is Orientation.COL:
            pairs_to_match = min(self.width - candidate[1] - 1, candidate[0])
            values = self.find_pairs(items=self.columns)
        else:
            raise ValueError("Invalid orientation")

        for i in range(1, pairs_to_match + 1):
            next_pair = (candidate[0] - i, candidate[1] + i)

            if next_pair not in values:
                return False

        return True


def find_reflection_candidates(pairs: set[Candidate]) -> list[Candidate]:
    candidates = []
    for index1, index2 in pairs:
        if index2 - index1 == 1:
            candidates.append((index1, index2))

    return candidates


def parse_patterns(patterns_raw: str) -> list[Pattern]:
    patterns = []
    for pattern_raw in patterns_raw.split("\n\n"):
        patterns.append(Pattern.from_raw(pattern_raw=pattern_raw))

    return patterns


def part1(patterns: list[Pattern]) -> int:
    return sum(pattern.find_reflection_number() for pattern in patterns)


def part2(patterns: list[Pattern]) -> int:
    total = 0
    for pattern in patterns:
        while True:
            pattern.update_smudge()

            try:
                total += pattern.find_reflection_number()
            except ValueError:
                pass
            else:
                break

    return total


def main() -> None:
    patterns_raw = utils.read_input_to_string()
    patterns = parse_patterns(patterns_raw=patterns_raw)
    print(f"Part 1: {part1(patterns=patterns)}")
    print(f"Part 2: {part2(patterns=patterns)}")


if __name__ == "__main__":
    main()

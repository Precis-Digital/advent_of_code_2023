import dataclasses
import functools
from typing import Self

from shared import utils

POSSIBLE_DOT = {".", "?"}


@dataclasses.dataclass
class Record:
    damaged: str
    redundant: tuple[int, ...]

    @classmethod
    def from_raw(cls, record_raw: str) -> Self:
        damaged_record, redundant_record = record_raw.split(" ")
        redundant_record = tuple(map(int, redundant_record.split(",")))
        return cls(damaged=damaged_record, redundant=redundant_record)


def combination_impossible(damaged: str, redundant: tuple[int, ...]) -> bool:
    return (redundant and redundant[0] > len(damaged)) or (
        "#" in damaged and not redundant
    )


def handle_starts_with_broken(damaged: str, redundant: tuple[int, ...]) -> int:
    if redundant[0] > len(damaged.split(".")[0]):
        return 0

    if len(redundant) == 1:
        return get_combinations(damaged=damaged[redundant[0] :], redundant=())

    if redundant[0] >= len(damaged) or damaged[redundant[0]] not in POSSIBLE_DOT:
        return 0

    return get_combinations(
        damaged=damaged[redundant[0] + 1 :], redundant=redundant[1:]
    )


@functools.cache
def get_combinations(damaged: str, redundant: tuple[int, ...]) -> int:
    if not damaged:
        return 0 if redundant else 1

    if combination_impossible(damaged=damaged, redundant=redundant):
        return 0

    if damaged.startswith("."):
        return get_combinations(damaged=damaged[1:], redundant=redundant)

    if damaged.startswith("#"):
        return handle_starts_with_broken(damaged=damaged, redundant=redundant)

    if damaged.startswith("?"):
        operational = get_combinations(damaged=f".{damaged[1:]}", redundant=redundant)
        broken = get_combinations(damaged=f"#{damaged[1:]}", redundant=redundant)
        return operational + broken


def parse_records(records_raw: str) -> list[Record]:
    return [Record.from_raw(record_raw=record) for record in records_raw.splitlines()]


def part1(records: list[Record]) -> int:
    tot = 0
    for record in records:
        tot += get_combinations(damaged=record.damaged, redundant=record.redundant)

    return tot


def part2(records: list[Record]) -> int:
    tot = 0
    for record in records:
        damaged = "?".join(record.damaged for _ in range(5))
        tot += get_combinations(damaged=damaged, redundant=record.redundant * 5)

    return tot


def main() -> None:
    records_raw = utils.read_input_to_string()
    records = parse_records(records_raw=records_raw)

    print(f"Part 1: {part1(records=records)}")
    print(f"Part 2: {part2(records=records)}")


if __name__ == "__main__":
    main()

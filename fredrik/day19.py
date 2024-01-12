from __future__ import annotations

import collections
import dataclasses
import operator
import re
from typing import Any, Callable, Self

from shared import utils

OPERATORS = {">": operator.gt, "<": operator.lt}
RATING_PATTERN = r"x=(\d+),m=(\d+),a=(\d+),s=(\d+)"


@dataclasses.dataclass(frozen=True, slots=True)
class Condition:
    key: str
    operator: Callable[[int, int], bool]
    value: int
    destination: str

    @classmethod
    def from_string(cls, condition: str) -> Self:
        cond, destination = condition.split(":")
        key, operator_, value = cond[0], OPERATORS[cond[1]], int(cond[2:])
        return cls(key=key, operator=operator_, value=value, destination=destination)

    def check(self, part_rating: PartRating) -> bool:
        return self.operator(part_rating[self.key], self.value)


@dataclasses.dataclass(frozen=True, slots=True)
class PartRating:
    x: int
    m: int
    a: int
    s: int

    def __getitem__(self, item: str) -> int:
        return getattr(self, item)

    def sum(self) -> int:
        return self.x + self.m + self.a + self.s


@dataclasses.dataclass(frozen=True, slots=True)
class Workflow:
    conditions: list[Condition]
    catchall: str

    def process_part_rating(self, part_rating: PartRating) -> str:
        for condition in self.conditions:
            if condition.check(part_rating=part_rating):
                return condition.destination

        return self.catchall


@dataclasses.dataclass
class PartRatingState:
    x: tuple[int, int] = (1, 4000)
    m: tuple[int, int] = (1, 4000)
    a: tuple[int, int] = (1, 4000)
    s: tuple[int, int] = (1, 4000)

    @property
    def combinations(self) -> int:
        return (
            (self.x[1] - self.x[0] + 1)
            * (self.m[1] - self.m[0] + 1)
            * (self.a[1] - self.a[0] + 1)
            * (self.s[1] - self.s[0] + 1)
        )

    def copy(self) -> Self:
        new = type(self)()
        new.__dict__.update(self.__dict__)
        return new

    def __getitem__(self, item: str) -> int:
        return getattr(self, item)

    def __setitem__(self, item: str, value: Any) -> None:
        setattr(self, item, value)

    def split_by_condition(
        self, condition: Condition, /
    ) -> tuple[PartRatingState, PartRatingState]:
        true_state, false_state = self.copy(), self.copy()
        lower, upper = self[condition.key]

        if condition.operator == operator.gt:
            true_ = max(lower, condition.value + 1), max(upper, condition.value + 1)
            false_ = min(lower, condition.value), min(upper, condition.value)
        elif condition.operator == operator.lt:
            true_ = min(lower, condition.value - 1), min(upper, condition.value - 1)
            false_ = max(lower, condition.value), max(upper, condition.value)
        else:
            raise ValueError(f"Unknown operator: {condition.operator}")

        true_state[condition.key] = true_
        false_state[condition.key] = false_

        return true_state, false_state


def parse_input(input_raw: str) -> tuple[dict[str, Workflow], list[PartRating]]:
    workflows = {}
    part_ratings = []
    workflows_raw, part_ratings_raw = input_raw.split("\n\n")
    for workflow_raw in workflows_raw.splitlines():
        name, instructions = workflow_raw.rstrip("}").split("{")
        *conditions, catchall = instructions.split(",")
        conditions = [Condition.from_string(condition) for condition in conditions]
        workflows[name] = Workflow(conditions=conditions, catchall=catchall)

    for part_rating in part_ratings_raw.splitlines():
        x, m, a, s = re.findall(RATING_PATTERN, part_rating)[0]
        part_ratings.append(PartRating(x=int(x), m=int(m), a=int(a), s=int(s)))

    return workflows, part_ratings


def part1(workflows: dict[str, Workflow], part_ratings: list[PartRating]) -> int:
    part_ratings_sum = 0
    for part_rating in part_ratings:
        destination, workflow = "in", None
        while destination not in {"A", "R"}:
            workflow = workflows[destination]
            destination = workflow.process_part_rating(part_rating=part_rating)

        if destination == "A":
            part_ratings_sum += part_rating.sum()

    return part_ratings_sum


def part2(workflows: dict[str, Workflow]) -> int:
    combinations = 0
    queue = collections.deque([(PartRatingState(), "in")])

    while queue:
        current_state, workflow = queue.pop()

        if workflow == "A":
            combinations += current_state.combinations
            continue

        if workflow == "R":
            continue

        for condition in workflows[workflow].conditions:
            next_state, current_state = current_state.split_by_condition(condition)
            queue.append((next_state, condition.destination))

        queue.append((current_state, workflows[workflow].catchall))

    return combinations


def main() -> None:
    input_raw = utils.read_input_to_string()
    workflows, part_ratings = parse_input(input_raw=input_raw)

    print(f"Part 1: {part1(workflows=workflows, part_ratings=part_ratings)}")
    print(f"Part 2: {part2(workflows=workflows)}")


if __name__ == "__main__":
    main()

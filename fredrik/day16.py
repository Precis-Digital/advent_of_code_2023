from __future__ import annotations

import dataclasses
import enum
import functools
import itertools
from typing import Self

from shared import utils

Coordinate = tuple[int, int]


class Direction(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()


MIRRORS = {
    "/": {
        Direction.UP: Direction.RIGHT,
        Direction.DOWN: Direction.LEFT,
        Direction.LEFT: Direction.DOWN,
        Direction.RIGHT: Direction.UP,
    },
    "\\": {
        Direction.UP: Direction.LEFT,
        Direction.DOWN: Direction.RIGHT,
        Direction.LEFT: Direction.UP,
        Direction.RIGHT: Direction.DOWN,
    },
}

SPLITTERS = {
    "|": {
        Direction.UP: None,
        Direction.DOWN: None,
        Direction.LEFT: (Direction.UP, Direction.DOWN),
        Direction.RIGHT: (Direction.UP, Direction.DOWN),
    },
    "-": {
        Direction.UP: (Direction.LEFT, Direction.RIGHT),
        Direction.DOWN: (Direction.LEFT, Direction.RIGHT),
        Direction.LEFT: None,
        Direction.RIGHT: None,
    },
}


@dataclasses.dataclass
class Beam:
    position: Coordinate
    direction: Direction

    def move(self) -> None:
        if self.direction is Direction.UP:
            self.position = self.position[0], self.position[1] - 1
        elif self.direction is Direction.DOWN:
            self.position = self.position[0], self.position[1] + 1
        elif self.direction is Direction.LEFT:
            self.position = self.position[0] - 1, self.position[1]
        elif self.direction is Direction.RIGHT:
            self.position = self.position[0] + 1, self.position[1]
        else:
            raise ValueError(f"Unknown direction: {self.direction}")

    def reflect(self, mirror: str) -> None:
        self.direction = MIRRORS[mirror][self.direction]

    def split(self, splitter: str) -> tuple[Beam, Beam] | None:
        if (directions := SPLITTERS[splitter][self.direction]) is None:
            return None

        return Beam(self.position, directions[0]), Beam(self.position, directions[1])


@dataclasses.dataclass
class Contraption:
    grid: dict[Coordinate, str]
    seen: set[tuple[Coordinate, Direction]] = dataclasses.field(default_factory=set)

    @classmethod
    def from_raw(cls, contraption_raw: str) -> Self:
        grid = {}
        for y, line in enumerate(contraption_raw.splitlines()):
            for x, char in enumerate(line):
                grid[(x, y)] = char

        return Contraption(grid=grid)

    @property
    def energized(self) -> int:
        return len({coordinate for coordinate, _ in self.seen})

    @functools.cached_property
    def max_x(self) -> int:
        return max(x for x, _ in self.grid)

    @functools.cached_property
    def max_y(self) -> int:
        return max(y for _, y in self.grid)

    @functools.cached_property
    def edge_points(self) -> list[Coordinate]:
        edge_points = []

        for x in range(self.max_x + 1):
            edge_points.append((x, 0))
            edge_points.append((x, self.max_y))

        for y in range(self.max_y + 1):
            edge_points.append((0, y))
            edge_points.append((self.max_x, y))

        return edge_points

    def reset_seen(self) -> None:
        self.seen = set()

    def out_of_bounds(self, beam: Beam) -> bool:
        return beam.position not in self.grid

    def already_seen(self, beam: Beam) -> bool:
        return (beam.position, beam.direction) in self.seen

    def add_beam_to_seen(self, beam: Beam) -> None:
        self.seen.add((beam.position, beam.direction))

    def current_char(self, beam: Beam) -> str:
        return self.grid[beam.position]

    def trace_beam(self, beam: Beam) -> None:
        while True:
            if self.out_of_bounds(beam=beam) or self.already_seen(beam=beam):
                return

            self.add_beam_to_seen(beam=beam)

            if (current := self.current_char(beam=beam)) in MIRRORS:
                beam.reflect(mirror=current)

            elif current in SPLITTERS:
                if beams := beam.split(splitter=current):
                    for beam_ in beams:
                        self.trace_beam(beam=beam_)

                    return

            beam.move()


def part1(contraption: Contraption) -> int:
    contraption.trace_beam(beam=Beam(position=(0, 0), direction=Direction.RIGHT))
    return contraption.energized


def part2(contraption: Contraption) -> int:
    max_energized = 0
    for position, direction in itertools.product(contraption.edge_points, Direction):
        contraption.trace_beam(beam=Beam(position=position, direction=direction))
        max_energized = max(max_energized, contraption.energized)
        contraption.reset_seen()

    return max_energized


def main() -> None:
    contraption_raw = utils.read_input_to_string()
    contraption = Contraption.from_raw(contraption_raw)

    print(f"Part 1: {part1(contraption=contraption)}")
    print(f"Part 2: {part2(contraption=contraption)}")


if __name__ == "__main__":
    main()

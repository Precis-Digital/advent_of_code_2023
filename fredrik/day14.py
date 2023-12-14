import dataclasses
import enum
import functools
import itertools
from typing import Self

from shared import utils

Coordinate = tuple[int, int]


class Direction(enum.Enum):
    NORTH = enum.auto()
    WEST = enum.auto()
    SOUTH = enum.auto()
    EAST = enum.auto()


@dataclasses.dataclass
class Platform:
    grid: dict[Coordinate, str]

    @functools.cached_property
    def x_max(self) -> int:
        return max(x for x, _ in self.grid)

    @functools.cached_property
    def y_max(self) -> int:
        return max(y for _, y in self.grid)

    @property
    def total_load(self) -> int:
        total_load_ = 0
        for (x, y), char in self.grid.items():
            if char != "O":
                continue

            total_load_ += self.y_max - y + 1

        return total_load_

    @classmethod
    def from_raw(cls, platform_raw: str) -> Self:
        platform = {}
        for y, row in enumerate(platform_raw.splitlines()):
            for x, char in enumerate(row):
                platform[(x, y)] = char

        return cls(grid=platform)

    def tilt_north(self) -> None:
        for y, x in itertools.product(range(self.y_max + 1), range(self.x_max + 1)):
            if self.grid[(x, y)] != "O" or y == 0:
                continue

            steps = 1
            while True:
                if (new_y := y - steps) < 0 or self.grid[(x, new_y)] != ".":
                    new_y += 1
                    break

                steps += 1

            if new_y == y:
                continue

            self.grid[(x, new_y)] = "O"
            self.grid[(x, y)] = "."

    def tilt_south(self) -> None:
        for y, x in itertools.product(
            reversed(range(self.y_max + 1)), reversed(range(self.x_max + 1))
        ):
            if self.grid[(x, y)] != "O" or y == self.y_max:
                continue

            steps = 1
            while True:
                if (new_y := y + steps) > self.y_max or self.grid[(x, new_y)] != ".":
                    new_y -= 1
                    break

                steps += 1

            if new_y == y:
                continue

            self.grid[(x, new_y)] = "O"
            self.grid[(x, y)] = "."

    def tilt_west(self) -> None:
        for y, x in itertools.product(range(self.y_max + 1), range(self.x_max + 1)):
            if self.grid[(x, y)] != "O" or x == 0:
                continue

            steps = 1
            while True:
                if (new_x := x - steps) < 0 or self.grid[(new_x, y)] != ".":
                    new_x += 1
                    break

                steps += 1

            if new_x == x:
                continue

            self.grid[(new_x, y)] = "O"
            self.grid[(x, y)] = "."

    def tilt_east(self) -> None:
        for y, x in itertools.product(
            reversed(range(self.y_max + 1)), reversed(range(self.x_max + 1))
        ):
            if self.grid[(x, y)] != "O" or x == self.x_max:
                continue

            steps = 1
            while True:
                if (new_x := x + steps) > self.x_max or self.grid[(new_x, y)] != ".":
                    new_x -= 1
                    break

                steps += 1

            if new_x == x:
                continue

            self.grid[(new_x, y)] = "O"
            self.grid[(x, y)] = "."

    def tilt(self, direction: Direction) -> None:
        if direction == Direction.NORTH:
            self.tilt_north()
        elif direction == Direction.WEST:
            self.tilt_west()
        elif direction == Direction.SOUTH:
            self.tilt_south()
        elif direction == Direction.EAST:
            self.tilt_east()
        else:
            raise ValueError(f"Unknown direction: {direction}")


def part1(platform_raw: str) -> int:
    platform = Platform.from_raw(platform_raw=platform_raw)
    platform.tilt_north()
    return platform.total_load


def part2(platform_raw: str) -> int:
    cycles_to_complete = 1000000000
    platform = Platform.from_raw(platform_raw=platform_raw)
    seen = {}
    for i in range(cycles_to_complete):
        snapshot = platform.grid.copy()
        if snapshot in seen.values():
            offset = list(seen.values()).index(snapshot)
            cycle_length = i - offset
            break

        for direction in Direction:
            platform.tilt(direction=direction)

        seen[i] = snapshot
    else:
        raise RuntimeError("Did not find a cycle")

    position_within_cycle = (cycles_to_complete - offset) % cycle_length
    index = position_within_cycle + offset

    platform.grid = seen[index]
    return platform.total_load


def main() -> None:
    platform_raw = utils.read_input_to_string()

    print(f"Part 1: {part1(platform_raw=platform_raw)}")
    print(f"Part 2: {part2(platform_raw=platform_raw)}")


if __name__ == "__main__":
    main()

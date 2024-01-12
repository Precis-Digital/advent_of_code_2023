import collections
import dataclasses
import functools
from typing import Self

from shared import utils

Coordinate = tuple[int, int]


@dataclasses.dataclass(frozen=True)
class GardenPlot:
    map: dict[Coordinate, str]
    starting_point: Coordinate

    @classmethod
    def from_raw(cls, garden_raw: str) -> Self:
        garden_map, starting_point = {}, None
        for y, line in enumerate(garden_raw.splitlines()):
            for x, char in enumerate(line):
                if char == "S":
                    starting_point = (x, y)
                    garden_map[(x, y)] = "."
                else:
                    garden_map[(x, y)] = char

        return cls(map=garden_map, starting_point=starting_point)

    @functools.cached_property
    def side_length(self) -> int:
        return max(self.map.keys(), key=lambda c: c[0])[0] + 1

    def __getitem__(self, coord: Coordinate) -> str:
        return self.map[(coord[0] % self.side_length, coord[1] % self.side_length)]

    def calculate_reachable(
        self,
        steps: int = 64,
        infinite: bool = False,
    ) -> int:
        queue = collections.deque([State(position=self.starting_point, steps=0)])

        seen, reachable = set(), 0

        while queue:
            current = queue.popleft()

            if current in seen:
                continue

            seen.add(current)

            if current.steps == steps:
                reachable += 1
                continue

            for neighbor in utils.cardinal_adjacent_indices(current.position):
                if not infinite and neighbor not in self.map:
                    continue

                if self[neighbor] != "#" and current.steps < steps:
                    queue.append(State(position=neighbor, steps=current.steps + 1))

        return reachable


@dataclasses.dataclass(frozen=True, slots=True)
class State:
    position: Coordinate
    steps: int


@dataclasses.dataclass
class Quadratic:
    a: int
    b: int
    c: int

    def __call__(self, x: int) -> int:
        return self.a * x**2 + self.b * x + self.c

    @classmethod
    def from_points(cls, p1: Coordinate, p2: Coordinate, p3: Coordinate) -> Self:
        (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3

        a_numerator = x1 * (y3 - y2) + x2 * (y1 - y3) + x3 * (y2 - y1)
        a_denominator = (x1 - x2) * (x1 - x3) * (x2 - x3)
        a = a_numerator / a_denominator

        b = (y2 - y1) / (x2 - x1) - a * (x1 + x2)
        c = y1 - a * x1**2 - b * x1

        return cls(a=int(a), b=int(b), c=int(c))


def part1(garden: GardenPlot) -> int:
    return garden.calculate_reachable()


def part2(garden: GardenPlot) -> int:
    required_steps = 26501365
    edge_distance = int((garden.side_length - 1) / 2)
    distances = [edge_distance + garden.side_length * i for i in range(3)]
    main_axis_grids = int((required_steps - edge_distance) / garden.side_length)

    points = []
    for i, steps in enumerate(distances):
        reached = garden.calculate_reachable(steps=steps, infinite=True)
        points.append((i, reached))

    quadratic = Quadratic.from_points(*points)
    return quadratic(x=main_axis_grids)


def main() -> None:
    garden_raw = utils.read_input_to_string()
    garden = GardenPlot.from_raw(garden_raw)

    print(f"Part 1: {part1(garden=garden)}")
    print(f"Part 2: {part2(garden=garden)}")


if __name__ == "__main__":
    main()

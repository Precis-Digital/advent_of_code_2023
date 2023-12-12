import dataclasses
import functools
import itertools
import math
from typing import Self

from shared import utils

Coordinate = tuple[int, int]

PIPES = {
    "|": ((0, 1), (0, -1)),
    "-": ((1, 0), (-1, 0)),
    "L": ((0, -1), (1, 0)),
    "J": ((0, -1), (-1, 0)),
    "7": ((0, 1), (-1, 0)),
    "F": ((0, 1), (1, 0)),
}


@dataclasses.dataclass
class Field:
    starting_point: Coordinate
    field: dict[Coordinate, str]
    main_loop: set[Coordinate] = dataclasses.field(default_factory=set)
    inside: set[Coordinate] = dataclasses.field(default_factory=set)
    visited_history: set[Coordinate] = dataclasses.field(default_factory=set)

    @functools.cached_property
    def max_x(self) -> int:
        return max(self.field.keys(), key=lambda point: point[0])[0]

    @functools.cached_property
    def max_y(self) -> int:
        return max(self.field.keys(), key=lambda point: point[1])[1]

    @functools.cached_property
    def min_x(self) -> int:
        return min(self.field.keys(), key=lambda point: point[0])[0]

    @functools.cached_property
    def min_y(self) -> int:
        return min(self.field.keys(), key=lambda point: point[1])[1]

    def clear_cached_properties(self) -> None:
        del self.max_x, self.max_y, self.min_x, self.min_y  # noqa

    @classmethod
    def parse_field(cls, field_raw: str) -> Self:
        starting_point, field = (), {}
        for y, line in enumerate(field_raw.splitlines()):
            for x, char in enumerate(line):
                point = (x, y)
                field[point] = char
                if char == "S":
                    starting_point = point

        return cls(field=field, starting_point=starting_point)

    def insert_empty_space(self) -> None:
        for x1, x2 in itertools.pairwise(range(self.min_x, self.max_x + 1)):
            for y in range(self.min_y, self.max_y + 1):
                point1, points2 = (x1, y), (x2, y)
                midpoint = ((x1 + x2) / 2, y)

                if can_connect_horizontally(
                    left=self.field[point1], right=self.field[points2]
                ):
                    self.field[midpoint] = "-"
                    self.main_loop.add(midpoint)
                else:
                    self.field[midpoint] = " "

        for x in range(self.min_x, self.max_x + 1):
            for y1, y2 in itertools.pairwise(range(self.min_y, self.max_y + 1)):
                point1, points2 = (x, y1), (x, y2)
                midpoint = (x, (y1 + y2) / 2)

                if can_connect_vertically(
                    top=self.field[point1], bottom=self.field[points2]
                ):
                    self.field[midpoint] = "|"
                    self.main_loop.add(midpoint)
                else:
                    self.field[midpoint] = " "

        self.field = {(int(p[0] * 2), int(p[1] * 2)): v for p, v in self.field.items()}
        self.main_loop = {(int(p[0] * 2), int(p[1] * 2)) for p in self.main_loop}

        self.clear_cached_properties()

        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                point = (x, y)
                if point not in self.field:
                    left, right = self.field[(x - 1, y)], self.field[(x + 1, y)]
                    bottom, top = self.field[(x, y - 1)], self.field[(x, y + 1)]
                    if can_connect_horizontally(left=left, right=right):
                        self.field[point] = "-"
                        self.main_loop.add(point)
                    elif can_connect_vertically(bottom=bottom, top=top):
                        self.field[point] = "|"
                        self.main_loop.add(point)
                    else:
                        self.field[point] = " "

    def find_next_from_start(self) -> Coordinate:
        candidate_points = utils.adjacent_indices(index=self.starting_point)
        for candidate_point in candidate_points:
            if candidate_point not in self.field:
                continue

            if (pipe := self.field[candidate_point]) == ".":
                continue

            for connection in PIPES[pipe]:
                if (
                    connect_point(point=candidate_point, offset=connection)
                    == self.starting_point
                ):
                    return candidate_point

    def traverse_loop(self, point: Coordinate) -> None:
        while point != self.starting_point:
            self.main_loop.add(point)
            connections = PIPES[self.field[point]]
            for connection in connections:
                new_point = connect_point(point=point, offset=connection)
                if new_point not in self.main_loop and self.field[new_point] != ".":
                    if new_point == self.starting_point and len(self.main_loop) == 1:
                        continue

                    point = new_point
                    break

    def get_furthest_distance(self) -> int:
        return math.ceil(len(self.main_loop) / 2)

    def trace_enclosed_tiles(self, point: Coordinate) -> None:
        if point in self.visited_history:
            return

        points, visited = {point}, set()
        outside = False
        touched_main_loop = False
        while points:
            current_point = points.pop()
            visited.add(current_point)
            for neighbor in find_neighbors(point=current_point):
                if neighbor in visited:
                    continue

                if neighbor in self.main_loop:
                    touched_main_loop = True
                    continue

                if neighbor not in self.field:
                    outside = True
                    continue

                points.add(neighbor)

        if not outside and touched_main_loop:
            self.inside.update(visited)

        self.visited_history.update(visited)

    def calculate_enclosed_area(self) -> int:
        self.insert_empty_space()

        for point in (point for point in self.field if point not in self.main_loop):
            self.trace_enclosed_tiles(point=point)

        return len([point for point in self.inside if self.field[point] != " "])


def can_connect_horizontally(left: str, right: str) -> bool:
    if left in {" ", ".", "|", "J", "7"}:
        return False

    if right in {" ", ".", "|", "L", "F"}:
        return False

    return True


def can_connect_vertically(top: str, bottom: str) -> bool:
    if top in {" ", ".", "-", "L", "J"}:
        return False

    if bottom in {" ", ".", "-", "7", "F"}:
        return False

    return True


def connect_point(point: Coordinate, offset: tuple[int, int]) -> Coordinate:
    return point[0] + offset[0], point[1] + offset[1]


def find_neighbors(point: Coordinate) -> set[Coordinate]:
    return {
        (point[0] + 1, point[1]),
        (point[0] - 1, point[1]),
        (point[0], point[1] + 1),
        (point[0], point[1] - 1),
    }


def main() -> None:
    field_raw = utils.read_input_to_string()
    field = Field.parse_field(field_raw=field_raw)

    point = field.find_next_from_start()
    field.traverse_loop(point=point)
    furthest_distance = field.get_furthest_distance()
    enclosed_area = field.calculate_enclosed_area()

    print(f"Part 1: {furthest_distance}")
    print(f"Part 2: {enclosed_area}")


if __name__ == "__main__":
    main()

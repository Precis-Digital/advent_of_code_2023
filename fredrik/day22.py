import copy
import dataclasses
import functools
from typing import Self

from shared import utils

type Coordinate = tuple[int, ...]
X, Y, Z = 0, 1, 2


@dataclasses.dataclass
class Brick:
    coord1: Coordinate
    coord2: Coordinate

    @functools.cached_property
    def main_axis(self) -> int | None:
        if self.coord1[X] != self.coord2[X]:
            return X

        if self.coord1[Y] != self.coord2[Y]:
            return Y

        if self.coord1[Z] != self.coord2[Z]:
            return Z

        return None

    @property
    def lowest_point(self) -> int:
        return min(self.coord1[Z], self.coord2[Z])

    @property
    def occupies(self) -> set[Coordinate]:
        if self.main_axis is None:
            return {self.coord1}

        start, end = sorted([self.coord1[self.main_axis], self.coord2[self.main_axis]])
        occupied = set()
        for index in range(start, end + 1):
            coord = list(self.coord1)
            coord[self.main_axis] = index
            occupied.add(tuple(coord))

        return occupied

    def __lt__(self, other: Self) -> bool:
        return self.lowest_point < other.lowest_point

    def fall(self) -> None:
        self.coord1 = (self.coord1[X], self.coord1[Y], self.coord1[Z] - 1)
        self.coord2 = (self.coord2[X], self.coord2[Y], self.coord2[Z] - 1)


def parse_bricks(snapshot: str) -> list[Brick]:
    bricks = []
    for line in snapshot.splitlines():
        coord1, coord2 = line.split("~")
        coord1 = tuple(int(coord) for coord in coord1.split(","))
        coord2 = tuple(int(coord) for coord in coord2.split(","))
        bricks.append(Brick(coord1=coord1, coord2=coord2))

    return bricks


@dataclasses.dataclass
class CubeGrid:
    bricks: list[Brick]
    occupied: set[Coordinate]

    @classmethod
    def from_bricks(cls, bricks: list[Brick]) -> Self:
        occupied = set()
        for brick in bricks:
            occupied |= brick.occupies

        return cls(bricks=bricks, occupied=occupied)

    def can_fall(self, brick: Brick) -> bool:
        if brick.lowest_point == 1:
            return False

        for cube in brick.occupies:
            fallen_cube = (cube[X], cube[Y], cube[Z] - 1)
            if fallen_cube in self.occupied and fallen_cube not in brick.occupies:
                return False

        return True

    def fall(self, brick: Brick) -> None:
        self.occupied -= brick.occupies
        brick.fall()
        self.occupied |= brick.occupies

    def start_gravity(self) -> int:
        fallen_bricks = 0
        for brick in sorted(self.bricks):
            has_fallen = False
            while self.can_fall(brick=brick):
                self.fall(brick)
                has_fallen = True

            if has_fallen:
                fallen_bricks += 1

        return fallen_bricks


def part1(grid: CubeGrid) -> int:
    tot = 0
    for removed_brick in grid.bricks:
        tmp_grid = grid.from_bricks(
            [brick for brick in grid.bricks if brick != removed_brick]
        )

        for brick in tmp_grid.bricks:
            if tmp_grid.can_fall(brick=brick):
                break

        else:
            tot += 1

    return tot


def part2(grid: CubeGrid) -> int:
    tot = 0

    for removed_brick in grid.bricks:
        tmp_grid = grid.from_bricks(
            [copy.deepcopy(brick) for brick in grid.bricks if brick != removed_brick]
        )

        tot += tmp_grid.start_gravity()
    return tot


def main() -> None:
    snapshot_raw = utils.read_input_to_string()
    bricks = parse_bricks(snapshot_raw)

    grid = CubeGrid.from_bricks(bricks)
    grid.start_gravity()

    print(f"Part 1: {part1(grid=grid)}")
    print(f"Part 2: {part2(grid=grid)}")


if __name__ == "__main__":
    main()

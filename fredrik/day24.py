import dataclasses
import decimal
import functools
import itertools
from typing import Self

from shared import utils

type Coefficients2D = tuple[float, float]


@dataclasses.dataclass
class Hail:
    x: int
    y: int
    z: int
    dx: int
    dy: int
    dz: int

    @functools.cached_property
    def slope_2d(self) -> float:
        return self.coefficents_2d()[0]

    def coefficents_2d(self) -> Coefficients2D:
        slope = self.dy / self.dx
        intercept = self.y - slope * self.x
        return slope, intercept

    def intersections_2d(self, other: Self) -> tuple[float, float] | None:
        slope1, intercept1 = self.coefficents_2d()
        slope2, intercept2 = other.coefficents_2d()

        if slope1 == slope2:
            return None

        x = (intercept2 - intercept1) / (slope1 - slope2)
        y = slope1 * x + intercept1
        return x, y


def parse_hail(hail_raw: str) -> list[Hail]:
    hail_list = []
    for line in hail_raw.splitlines():
        x, y, z, dx, dy, dz = line.replace(" @", ",").split(", ")
        hail_list.append(Hail(int(x), int(y), int(z), int(dx), int(dy), int(dz)))
    return hail_list


def part1(hail: list[Hail]) -> int:
    collisions = 0

    for hail1, hail2 in itertools.combinations(hail, 2):
        if (intersection := hail1.intersections_2d(hail2)) is not None:
            x, y = intersection
            if (
                400000000000000 >= x >= 200000000000000
                and 400000000000000 >= y >= 200000000000000
            ):
                if hail1.x > x and hail1.dx > 0:
                    continue

                if hail2.x > x and hail2.dx > 0:
                    continue

                if hail1.x < x and hail1.dx < 0:
                    continue

                if hail2.x < x and hail2.dx < 0:
                    continue

                collisions += 1

    return collisions


def decimal_coefficients(coefficients: list[list[int]]) -> list[list[decimal.Decimal]]:
    return [
        [decimal.Decimal(coefficient) for coefficient in row] for row in coefficients
    ]


def decimal_constants(constants: list[int]) -> list[decimal.Decimal]:
    return [decimal.Decimal(constant) for constant in constants]


def gaussian_elimination(
    coefficients: list[list[int]], constants: list[int]
) -> list[decimal.Decimal]:
    n = len(coefficients)

    coefficients = decimal_coefficients(coefficients=coefficients)
    constants = decimal_constants(constants=constants)

    for i in range(n):
        pivot = coefficients[i][i]
        for j in range(i + 1, n):
            factor = coefficients[j][i] / pivot
            for k in range(n):
                coefficients[j][k] -= factor * coefficients[i][k]
            constants[j] -= factor * constants[i]

    solution = [decimal.Decimal(0)] * n
    for i in range(n - 1, -1, -1):
        solution[i] = constants[i]
        for j in range(i + 1, n):
            solution[i] -= coefficients[i][j] * solution[j]
        solution[i] /= coefficients[i][i]

    return solution


def part2(hail: list[Hail]) -> int:
    coefficients_xy, coefficients_xz = [], []
    constants_xy, constants_xz = [], []

    for hail1, hail2 in itertools.pairwise(hail[:5]):
        coefficients_xy.append(
            [
                hail2.dy - hail1.dy,
                hail2.x - hail1.x,
                hail1.dx - hail2.dx,
                hail1.y - hail2.y,
            ]
        )

        coefficients_xz.append(
            [
                hail2.dz - hail1.dz,
                hail2.x - hail1.x,
                hail1.dx - hail2.dx,
                hail1.z - hail2.z,
            ]
        )

        constants_xy.append(
            hail2.x * hail2.dy
            - hail2.y * hail2.dx
            - hail1.x * hail1.dy
            + hail1.y * hail1.dx
        )

        constants_xz.append(
            hail2.x * hail2.dz
            - hail2.z * hail2.dx
            - hail1.x * hail1.dz
            + hail1.z * hail1.dx
        )

    solution_xy = gaussian_elimination(coefficients_xy, constants_xy)
    solution_xz = gaussian_elimination(coefficients_xz, constants_xz)
    x, _, y, _ = tuple(map(round, solution_xy))
    _, _, z, _ = tuple(map(round, solution_xz))

    return x + y + z


def main() -> None:
    decimal.getcontext().prec = 100
    hail_raw = utils.read_input_to_string()
    hail = parse_hail(hail_raw=hail_raw)

    print(f"Part 1: {part1(hail=hail)}")
    print(f"Part 2: {part2(hail=hail)}")


if __name__ == "__main__":
    main()

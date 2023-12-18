import dataclasses
import itertools
from typing import Self

from shared import utils

Vertex = tuple[int, int]

DIRECTION_MAP = {"0": "R", "1": "D", "2": "L", "3": "U"}


@dataclasses.dataclass
class Trench:
    vertices: list[Vertex]
    length: int

    @property
    def area(self) -> int:
        interior_area = shoelace_formula(vertices=self.vertices)
        edge_area = self.length / 2 + 1
        return int(interior_area + edge_area)

    @classmethod
    def from_instructions(cls, instructions: list[str]) -> Self:
        current = (0, 0)
        vertices = [current]
        edge_length = 0
        for step in instructions:
            direction, distance, *_ = step.split()
            if direction == "D":
                current = (current[0], current[1] + int(distance))
            elif direction == "U":
                current = (current[0], current[1] - int(distance))
            elif direction == "R":
                current = (current[0] + int(distance), current[1])
            elif direction == "L":
                current = (current[0] - int(distance), current[1])

            vertices.append(current)
            edge_length += int(distance)

        return cls(vertices=vertices, length=edge_length)

    @classmethod
    def from_rbg_instructions(cls, rgb_instructions: list[str]) -> Self:
        instructions = []
        for step in rgb_instructions:
            *_, rgb = step.split()
            distance, direction = int(rgb[2:-2], base=16), DIRECTION_MAP[rgb[-2]]
            instructions.append(f"{direction} {distance}")

        return cls.from_instructions(instructions)


def shoelace_formula(vertices: list[Vertex]) -> int:
    sum1 = sum2 = 0
    for vertex1, vertex2 in itertools.pairwise(vertices):
        sum1 += vertex1[0] * vertex2[1]
        sum2 += vertex1[1] * vertex2[0]

    sum1 += vertices[-1][0] * vertices[0][1]
    sum2 += vertices[-1][1] * vertices[0][0]

    return int(abs(sum1 - sum2) / 2)


def main() -> None:
    instructions = utils.read_input_to_string().splitlines()
    trench = Trench.from_instructions(instructions=instructions)
    trench_rgb = Trench.from_rbg_instructions(rgb_instructions=instructions)

    print("Part 1:", trench.area)
    print("Part 2:", trench_rgb.area)


if __name__ == "__main__":
    main()

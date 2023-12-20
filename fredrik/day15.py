import dataclasses
import enum
import re

from shared import utils


class OperationCharacter(enum.Enum):
    EQUALS = "="
    DASH = "-"


@dataclasses.dataclass
class Lens:
    label: str
    operation: OperationCharacter
    focal_length: int | None = None

    def __post_init__(self) -> None:
        self.focal_length = int(self.focal_length) if self.focal_length else None
        self.operation = OperationCharacter(self.operation)

    @property
    def box(self) -> int:
        return holiday_hash(self.label)

    @property
    def partial_focusing_power(self) -> int:
        return (self.box + 1) * self.focal_length


def holiday_hash(string: str, /) -> int:
    current_value = 0
    for char in string:
        current_value += ord(char)
        current_value *= 17
        current_value = current_value % 256

    return current_value


def parse_sequence(sequence: str) -> list[str]:
    return sequence.split(",")


def parse_step(step: str) -> Lens:
    pattern = r"^([a-zA-Z]+)(=|-)?(\d)?$"
    match = re.match(pattern, step)
    return Lens(*(group for group in match.groups() if group is not None))


def part1(sequence: list[str]) -> int:
    return sum([holiday_hash(step) for step in sequence])


def part2(sequence: list[str]) -> int:
    boxes = {i: [] for i in range(256)}
    for step in sequence:
        lens = parse_step(step=step)
        if lens.operation is OperationCharacter.DASH:
            boxes[lens.box] = [
                old_lens for old_lens in boxes[lens.box] if old_lens.label != lens.label
            ]

        elif lens.operation is OperationCharacter.EQUALS:
            for i, old_lens in enumerate(boxes[lens.box]):
                if old_lens.label == lens.label:
                    boxes[lens.box][i] = lens
                    break
            else:
                boxes[lens.box].append(lens)
        else:
            raise ValueError(f"Invalid operation {lens.operation}")

    total_focusing_power = 0
    for box in boxes.values():
        for j, lens in enumerate(box):
            total_focusing_power += (j + 1) * lens.partial_focusing_power

    return total_focusing_power


def main() -> None:
    sequence_raw = utils.read_input_to_string()
    sequence = parse_sequence(sequence=sequence_raw)

    print(f"Part 1: {part1(sequence=sequence)}")
    print(f"Part 2: {part2(sequence=sequence)}")


if __name__ == "__main__":
    main()

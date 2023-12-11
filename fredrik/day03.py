import dataclasses
import functools

from shared import utils

Coordinate = tuple[int, int]


@dataclasses.dataclass
class BaseEntry:
    occupies: set[Coordinate] = dataclasses.field(default_factory=set)

    @functools.cached_property
    def adjacent_indices(self) -> set[tuple[int, int]]:
        indices = set()
        for index in self.occupies:
            indices.update(utils.adjacent_indices(index=index))

        return indices


@dataclasses.dataclass
class Part(BaseEntry):
    number: int | None = None

    def __hash__(self) -> int:
        return hash(self.number)


@dataclasses.dataclass
class Gear(BaseEntry):
    def __hash__(self) -> int:
        return hash(next(iter(self.occupies)))


@dataclasses.dataclass
class SchematicParser:
    current_part: Part = dataclasses.field(default_factory=Part)
    current_number_text: str = ""
    parts_registry: list[Part] = dataclasses.field(default_factory=list)
    symbols_registry: list[Coordinate] = dataclasses.field(default_factory=list)
    gear_registry: list[Gear] = dataclasses.field(default_factory=list)

    def new_part(self) -> None:
        if not self.current_part_is_empty:
            self.current_part.number = int(self.current_number_text)

        self.current_part = Part()
        self.current_number_text = ""

    @property
    def current_part_is_empty(self) -> bool:
        return not self.current_number_text

    @functools.cached_property
    def parts(self) -> set[Part]:
        return set(self.parts_registry)

    @functools.cached_property
    def symbols(self) -> set[tuple[int, int]]:
        return set(self.symbols_registry)

    def calculate_part_sum(self) -> int:
        part_sum = 0
        for part in self.parts:
            if self.symbols.intersection(part.adjacent_indices):
                part_sum += part.number

        return part_sum

    def calculate_gear_ratio_sum(self) -> int:
        gear_ratio_sum = 0
        for gear in self.gear_registry:
            adjacent_parts = []
            for part in self.parts:
                if gear.occupies.intersection(part.adjacent_indices):
                    adjacent_parts.append(part)

            if len(adjacent_parts) == 2:
                gear_ratio_sum += adjacent_parts[0].number * adjacent_parts[1].number

        return gear_ratio_sum

    def parse(self, schematic: str) -> None:
        for y, row in enumerate(schematic.splitlines()):
            self.new_part()
            for x, char in enumerate(row):
                if char.isdigit():
                    self.current_number_text += char
                    self.current_part.occupies.add((x, y))
                    self.parts_registry.append(self.current_part)
                else:
                    if char != ".":
                        self.symbols_registry.append((x, y))

                    if char == "*":
                        self.gear_registry.append(Gear(occupies={(x, y)}))

                    if not self.current_part_is_empty:
                        self.new_part()


def main() -> None:
    data = utils.read_input_to_string()

    schematic_parser = SchematicParser()
    schematic_parser.parse(schematic=data)

    part_sum = schematic_parser.calculate_part_sum()
    gear_ratio_sum = schematic_parser.calculate_gear_ratio_sum()

    print(f"Part 1: {part_sum}")
    print(f"Part 2: {gear_ratio_sum}")


if __name__ == "__main__":
    main()

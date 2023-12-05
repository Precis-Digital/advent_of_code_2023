import dataclasses
import itertools

from shared import utils


@dataclasses.dataclass(frozen=True, slots=True)
class RangeOffset:
    range: range
    offset: int

    def __contains__(self, key: int) -> bool:
        return key in self.range


@dataclasses.dataclass
class RangeMap:
    ranges: list[RangeOffset] = dataclasses.field(default_factory=list)

    def _get_from_int(self, key: int) -> int:
        for range_ in self.ranges:
            if key in range_:
                return key + range_.offset
        return key

    def _get_from_range(self, key: range) -> list[range]:
        ranges = []
        for map_range in self.ranges:
            if overlap := range_overlap(map_range.range, key):
                ranges.append(combined_range(overlap, map_range.offset))

        return ranges

    def _get_from_ranges(self, key: list[range]) -> list[range]:
        ranges = []
        for map_range, key_range in itertools.product(self.ranges, key):
            if overlap := range_overlap(map_range.range, key_range):
                ranges.append(combined_range(overlap, map_range.offset))

        return ranges

    def __getitem__(self, key: int | list[range]) -> int | list[range]:
        if isinstance(key, int):
            return self._get_from_int(key)

        if isinstance(key, range):
            return self._get_from_range(key)

        if isinstance(key, list):
            return self._get_from_ranges(key)

        return NotImplemented


@dataclasses.dataclass
class Alamanac:
    seeds: list[int] = dataclasses.field(default_factory=list)
    seed_ranges: list[range] = dataclasses.field(default_factory=list)
    maps: list[RangeMap] = dataclasses.field(default_factory=list)

    def set_seeds(self, seeds_raw: str) -> None:
        self.seeds = list(map(int, seeds_raw.split(":")[1].split()))
        seed_ranges = itertools.batched(self.seeds, 2)
        self.seed_ranges = [
            range(seed_range[0], seed_range[0] + seed_range[1])
            for seed_range in seed_ranges
        ]

    def traverse_maps[T: (int, range)](self, initial: list[T], /) -> list[T]:
        result = initial
        for map_ in self.maps:
            result = [map_[key] for key in result]

        return result

    def get_min_location_numbers_from_seeds(self) -> int:
        return min(self.traverse_maps(self.seeds))

    def get_min_location_numbers_from_seed_ranges(self) -> int:
        location_ranges = flatten_list(self.traverse_maps(self.seed_ranges))
        return get_smallest_range_start(location_ranges)


def get_smallest_range_start(ranges: list[range], /) -> int:
    return min(range_.start for range_ in ranges)


def range_overlap(range1: range, range2: range, /) -> range:
    return range(max(range1.start, range2.start), min(range1.stop, range2.stop) + 1)


def flatten_list[T](list_: list[list[T]], /) -> list[T]:
    return [item for row in list_ for item in row]


def combined_range(overlap: range, offset: int) -> range:
    return range(overlap.start + offset, overlap.stop + offset)


def parse_alamanac(almanac_raw: str) -> Alamanac:
    seeds_raw, *maps_raw = almanac_raw.split("\n\n")
    alamanac = Alamanac()
    alamanac.set_seeds(seeds_raw=seeds_raw)

    for section in maps_raw:
        range_map = RangeMap()
        for line in section.splitlines():
            if "map" in line:
                continue

            destination, source, length = tuple(map(int, line.split()))
            offset = destination - source
            range_ = range(source, source + length)
            range_map.ranges.append(RangeOffset(range=range_, offset=offset))

        alamanac.maps.append(range_map)

    return alamanac


def main() -> None:
    almanac_raw = utils.read_input_to_string()
    alamanac = parse_alamanac(almanac_raw=almanac_raw)
    location_part1 = alamanac.get_min_location_numbers_from_seeds()
    location_part2 = alamanac.get_min_location_numbers_from_seed_ranges()

    print(f"Part 1: {location_part1}")
    print(f"Part 2: {location_part2}")


if __name__ == "__main__":
    main()

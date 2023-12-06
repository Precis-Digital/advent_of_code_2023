import dataclasses
import math

from shared import utils


@dataclasses.dataclass
class Race:
    time: int
    record: int

    def find_roots(self) -> tuple[float, float]:
        sqrt_term = math.sqrt((-self.time / 2) ** 2 - self.record)
        return self.time / 2 - sqrt_term, self.time / 2 + sqrt_term

    def ways_to_beat_record(self) -> int:
        roots = self.find_roots()
        lower, upper = min(roots), max(roots)
        lower = lower if not lower.is_integer() else lower + 1
        upper = upper if not upper.is_integer() else upper - 1
        return math.floor(upper) - math.ceil(lower) + 1


def parse_race_data(data: str) -> list[Race]:
    times, records = data.splitlines()
    times = list(map(int, times.split()[1:]))
    records = list(map(int, records.split()[1:]))

    races = []
    for time, record in zip(times, records):
        races.append(Race(time=time, record=record))

    return races


def parse_long_race_data(data: str) -> Race:
    time, record = data.splitlines()
    time = int("".join(time.split()[1:]))
    record = int("".join(record.split()[1:]))
    return Race(time=time, record=record)


def main() -> None:
    data_raw = utils.read_input_to_string()
    races = parse_race_data(data=data_raw)

    nr_of_record_breaks = [race.ways_to_beat_record() for race in races]
    part1 = math.prod(nr_of_record_breaks)

    race = parse_long_race_data(data=data_raw)
    part2 = race.ways_to_beat_record()

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()

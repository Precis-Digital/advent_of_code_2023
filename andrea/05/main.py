import re

re_end_line = re.compile(r'\r?\n?$')

re_seeds_or_map_name = re.compile(r'^(?:(seeds)|(\w+)-to-(\w+) map):|^(\d+) (\d+) (\d+)')

re_digits = re.compile(r'\s+(\d+)')
re_ranges = re.compile(r'\s+(\d+)\s+(\d+)')
re_map_ranges = re.compile(r'^(\d+) (\d+) (\d+)')

print_progress = False


class SeedMap:
    def __init__(self,
                 *,
                 from_name: str,
                 to_name: str):
        self.from_name = from_name
        self.to_name = to_name
        self.ranges = []
        self.ranges_alternative = []

    def add_range(self,
                  *,
                  dst_start: int,
                  src_start: int,
                  range_len: int):
        self.ranges.append((src_start,
                            src_start + range_len - 1,
                            dst_start - src_start))

    def test_ranges_intersect(self):
        for index, (start, end, offset) in enumerate(self.ranges):
            for next_index, (start_next, end_next, offset_next) in enumerate(self.ranges[index + 1:]):
                if (start <= start_next <= end
                        or start <= end_next <= end
                        or start <= start_next <= end_next <= end
                        or start_next <= start <= end_next
                        or start_next <= end <= end_next
                        or start_next <= start <= end <= end_next):
                    print(f" Overlap Source {self.from_name}: {start}, {end} - {start_next}, {end_next}")

        for index, (start, end, offset) in enumerate(self.ranges):
            start += offset
            end += offset
            for next_index, (start_next, end_next, offset_next) in enumerate(self.ranges[index + 1:]):
                start_next += offset_next
                end_next += offset_next
                if (start <= start_next <= end
                        or start <= end_next <= end
                        or start <= start_next <= end_next <= end
                        or start_next <= start <= end_next
                        or start_next <= end <= end_next
                        or start_next <= start <= end <= end_next):
                    print(f" Overlap Dest {self.from_name}: {start}, {end} - {start_next}, {end_next}")

    def map(self,
            *,
            seed: int,
            seed_maps: dict,
            size_same_result: int = None) -> (int, int):

        if print_progress:
            print(f"{self.from_name.rjust(12)} {str(seed).rjust(12)}", end='')
        for (start, end, offset) in self.ranges:
            if start <= seed <= (seed if end is None else end):
                seed += offset
                if end is not None:
                    if size_same_result is None:
                        size_same_result = end - seed + 1
                    else:
                        size_same_result = min(size_same_result, end - seed + 1)
                break
        if self.to_name in seed_maps:
            return seed_maps[self.to_name].map(seed=seed,
                                               seed_maps=seed_maps,
                                               size_same_result=size_same_result)
        else:
            if print_progress:
                print(f"{self.to_name.rjust(12)} {str(seed).rjust(12)}")
            return seed, size_same_result

    def map_from_range(self,
                       *,
                       seeds: list,
                       seeds_as_range: bool):
        if seeds_as_range:
            lowest_location = None
            while seeds:
                start_seed, end_seed = seeds[0]
                for (start, end, offset) in self.ranges:
                    if end_seed < start:
                        seeds.pop(0)
                        break
                    elif start_seed > end:
                        continue
                    if start <= start_seed:
                        if lowest_location is None:
                            lowest_location = start_seed + offset
                        else:
                            lowest_location = min(lowest_location,
                                                  start_seed + offset)
                    else:
                        if lowest_location is None:
                            lowest_location = start + offset
                        else:
                            lowest_location = min(lowest_location,
                                                  start + offset)

                    if end_seed > end:
                        seeds[0] = (end + 1, end_seed)
                    else:
                        seeds.pop(0)
                        break

            return lowest_location

    def map_final_range(self,
                        seed_maps: dict,
                        input_range: tuple) -> list[tuple]:

        self.ranges.sort(key=lambda range_tuple: range_tuple[0])

        input_start, input_end, input_offset = input_range
        input_start_offset = input_start + input_offset
        input_end_offset = 0 if input_end is None else input_end + input_offset
        output_ranges = []
        for (start, end, offset) in self.ranges:
            if input_start_offset < start:
                if input_end_offset is None or input_end_offset >= start:
                    # cut beginning of input range
                    if self.to_name in seed_maps:
                        if print_progress:
                            print(f"   {self.from_name} forward cut beginning of input range",
                                  (input_start,
                                   start - 1 - input_offset,
                                   input_offset))
                        output_ranges.extend(
                                seed_maps[self.to_name].map_final_range(
                                        seed_maps=seed_maps,
                                        input_range=(input_start,
                                                     start - 1 - input_offset,
                                                     input_offset)))
                    else:
                        if print_progress:
                            print(f"   {self.from_name} pass through cut beginning of input range",
                                  (input_start,
                                   start - 1 - input_offset,
                                   input_offset))
                        output_ranges.append((input_start,
                                              start - 1 - input_offset,
                                              input_offset))
                    input_start_offset = start
                    input_start = input_start_offset - input_offset
                else:
                    # whole of input range
                    if self.to_name in seed_maps:
                        if print_progress:
                            print(f"   {self.from_name} forward whole input range",
                                  (input_start,
                                   input_end,
                                   input_offset))
                        output_ranges.extend(
                                seed_maps[self.to_name].map_final_range(
                                        seed_maps=seed_maps,
                                        input_range=(input_start,
                                                     input_end,
                                                     input_offset)))
                    else:
                        if print_progress:
                            print(f"   {self.from_name} pass through whole of input range",
                                  (input_start,
                                   input_end,
                                   input_offset))
                        output_ranges.append((input_start,
                                              input_end,
                                              input_offset))
                    return output_ranges

            if start <= input_start_offset <= (input_start_offset if end is None else end):
                if end is None or (input_end_offset is not None
                                   and input_end_offset <= end):
                    # capture whole input range
                    if self.to_name in seed_maps:
                        if print_progress:
                            print(f"   {self.from_name} capture and forward whole input range",
                                  (input_start,
                                   input_end,
                                   input_offset + offset))
                        output_ranges.extend(
                                seed_maps[self.to_name].map_final_range(
                                        seed_maps=seed_maps,
                                        input_range=(input_start,
                                                     input_end,
                                                     input_offset + offset)))
                    else:
                        if print_progress:
                            print(f"   {self.from_name} capture whole input range",
                                  (input_start,
                                   input_end,
                                   input_offset + offset))
                        output_ranges.append((input_start,
                                              input_end,
                                              input_offset + offset))
                    return output_ranges
                else:
                    # cut beginning of input range
                    if self.to_name in seed_maps:
                        if print_progress:
                            print(f"   {self.from_name} capture, forward and cut beginning of input range",
                                  (input_start,
                                   end - input_offset,
                                   input_offset + offset))
                        output_ranges.extend(
                                seed_maps[self.to_name].map_final_range(
                                        seed_maps=seed_maps,
                                        input_range=(input_start,
                                                     end - input_offset,
                                                     input_offset + offset))
                        )
                    else:
                        if print_progress:
                            print(f"   {self.from_name} capture and cut beginning of input range",
                                  (input_start,
                                   end - input_offset,
                                   input_offset + offset))
                        output_ranges.append((input_start,
                                              end - input_offset,
                                              input_offset + offset))
                    input_start_offset = end + 1
                    input_start = input_start_offset - input_offset
                    continue

        # whole of input range
        if self.to_name in seed_maps:
            if print_progress:
                print(f"   {self.from_name} forward whole input range",
                      (input_start,
                       input_end,
                       input_offset))
            output_ranges.extend(
                    seed_maps[self.to_name].map_final_range(
                            seed_maps=seed_maps,
                            input_range=(input_start,
                                         input_end,
                                         input_offset)))
        else:
            if print_progress:
                print(f"   {self.from_name} pass through whole of input range",
                      (input_start,
                       input_end,
                       input_offset))
            output_ranges.append((input_start,
                                  input_end,
                                  input_offset))

        return output_ranges

    def build_complete_ranges(self,
                              *,
                              seeds: list,
                              seeds_as_range: bool,
                              seed_maps: dict):
        if seeds_as_range:
            ranges = [(start, end, 0)
                      for start, end in seeds]
        else:
            ranges = [(seed, seed, 0)
                      for seed in seeds]
        ranges.sort(key=lambda range_tuple: range_tuple[0])

        self.ranges = []

        for (start, end, offset) in ranges:
            if print_progress:
                print(f"  Start map final Range", (start, end, offset))
            self.ranges.extend(
                    seed_maps[self.from_name].map_final_range(
                            seed_maps=seed_maps,
                            input_range=(start, end, offset)))


def solve_05(*,
             step: int,
             seeds_as_range=False,
             alternative=False):
    print('*' * 20, f"Step {step}{' Alternative' if alternative else ''}")

    seeds = None
    seed_maps: dict[str, SeedMap] = {}
    seed_map = None

    with (open('input.txt', 'r') as input_file):
        for game_line in input_file:
            seeds_or_map_name = re_seeds_or_map_name.findall(game_line)
            if seeds_or_map_name:
                seeds_name, from_name, to_name, dst_start, src_start, range_len = seeds_or_map_name[0]
                if seeds_name:
                    if seeds_as_range:
                        seeds = [(int(start), int(start) + int(length) - 1)
                                 for start, length in re_ranges.findall(game_line)]
                        seeds.sort(key=lambda range_tuple: range_tuple[0])
                    else:
                        seeds = [int(seed) for seed in re_digits.findall(game_line)]
                        seeds.sort()

                    if print_progress:
                        print(f" Seeds: {seeds}")
                elif from_name and to_name:
                    seed_map = seed_maps[from_name] = SeedMap(from_name=from_name,
                                                              to_name=to_name)
                else:
                    seed_map.add_range(dst_start=int(dst_start),
                                       src_start=int(src_start),
                                       range_len=int(range_len))

    for seed_map in seed_maps.values():
        seed_map.test_ranges_intersect()

    if alternative:
        seed_map = SeedMap(from_name='seed', to_name='location')
        seed_map.build_complete_ranges(seeds=seeds,
                                       seeds_as_range=seeds_as_range,
                                       seed_maps=seed_maps)
        if print_progress:
            print(f" Complete Range by start")
            for complete_range in seed_map.ranges:
                print("  ", complete_range, complete_range[0] + complete_range[2])
            print(f" Complete Range by effect")
            complete_ranges_sorted_by_effect = [*seed_map.ranges]
            complete_ranges_sorted_by_effect.sort(
                    key=lambda range_tuple: range_tuple[0] + range_tuple[2])
            for complete_range in complete_ranges_sorted_by_effect:
                print("  ", complete_range, complete_range[0] + complete_range[2])
    else:
        seed_map = seed_maps['seed']

    if seeds_as_range:
        lowest_location = None
        if alternative:
            lowest_location = seed_map.map_from_range(seeds=seeds,
                                                      seeds_as_range=seeds_as_range)
        else:
            for index, (start, end) in enumerate(seeds):
                if print_progress:
                    print(f" Start seed range {index + 1}, {end - start + 1} seeds")
                for seed in range(start, end):
                    (location,
                     size_same_result) = seed_map.map(
                            seed=seed,
                            seed_maps=seed_maps,
                            size_same_result=end - start + 1)
                    if lowest_location is None:
                        lowest_location = location
                    else:
                        lowest_location = min(lowest_location, location)
                    if size_same_result:
                        seed += size_same_result
    else:
        seed_locations = [seed_map.map(seed=seed, seed_maps=seed_maps)
                          for seed in seeds]

        lowest_location = min(location for location, _ in seed_locations)

    print('*' * 20, f"Step {step}{' Alternative' if alternative else ''}", lowest_location)


if __name__ == '__main__':
    solve_05(step=1)
    solve_05(step=1, alternative=True)
    # solve_05(step=2, seeds_as_range=True)
    solve_05(step=2, seeds_as_range=True, alternative=True)

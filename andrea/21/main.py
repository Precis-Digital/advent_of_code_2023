import dataclasses
import functools

from numpy import sign

print_progress = [True, True]


class GardenSlot:
    reached_num_step: int = 0
    reached: bool = False

    def __init__(self,
                 *,
                 coord: tuple[int, int],
                 slot: str,
                 garden: 'Garden',
                 infinite_n: bool = False,
                 infinite_s: bool = False,
                 infinite_e: bool = False,
                 infinite_w: bool = False):
        self.slot = slot
        self.coord = coord
        self.plot = slot != '#'
        self.start = slot == 'S'
        self.garden = garden
        self.infinite_nsew = (infinite_n or infinite_s) ^ (infinite_e or infinite_w),
        self.infinite_ne_se_sw_nw = ((infinite_n and infinite_e)
                                     or (infinite_s and infinite_e)
                                     or (infinite_s and infinite_w)
                                     or (infinite_n and infinite_w))

    def __repr__(self) -> str:
        return ('S' if self.start
                else ('O' if self.reached
                      else ('.' if self.reached_num_step
                            else ('_' if self.plot
                                  else '#'))))

    @functools.cached_property
    def x(self) -> int:
        return self.coord[0]

    @functools.cached_property
    def y(self) -> int:
        return self.coord[1]

    @functools.cached_property
    def around_coords(self) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]:
        return ((self.x + 1, self.y),
                (self.x, self.y + 1),
                (self.x - 1, self.y),
                (self.x, self.y - 1))

    @functools.cached_property
    def possible_steps(self) -> tuple['GardenSlot', ...]:
        return tuple(
                self.garden[coord]
                for coord in self.around_coords
                if self.garden[coord]
                and self.garden[coord].plot)

    @functools.cached_property
    def possible_steps_infinite(self) -> list['GardenSlot']:
        possible: list['GardenSlot'] = []
        for coord in self.around_coords:
            garden_slot = self.garden.get_infinite(coord)
            if garden_slot.plot:
                possible.append(garden_slot)
        return possible

    def do_steps(self,
                 *,
                 num_step: int,
                 num_steps: int,
                 infinite: bool = False):
        if 0 < self.reached_num_step <= num_step:
            return
        self.reached = True
        self.reached_num_step = num_step
        if num_step < num_steps:
            possible_steps = (
                self.possible_steps_infinite if infinite
                else self.possible_steps)
            for next_step in possible_steps:
                next_step.do_steps(num_step=num_step + 1,
                                   num_steps=num_steps,
                                   infinite=infinite)
        else:
            self.reached = True


class Garden:
    start: GardenSlot

    def __init__(self,
                 *,
                 garden_map: dict[tuple[int, int], str]):
        self.map: dict[tuple[int, int], GardenSlot] = {}
        self.edge_size = 0
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0
        for (x, y), slot in garden_map.items():
            self.edge_size = max(x + 1, y + 1, self.edge_size)
            self.max_x = max(x, self.max_x)
            self.max_y = max(x, self.max_y)
            coord = (x, y)
            self.map[coord] = GardenSlot(coord=coord,
                                         slot=slot,
                                         garden=self)
            if slot == 'S':
                self.start = self.map[coord]

        self.edge_middle = int((self.edge_size - 1) / 2)

        self.range_x = range(self.min_x, self.max_x + 1)
        self.range_y = range(self.min_y, self.max_y + 1)

        assert self.start is not None

    def __getitem__(self, coord: tuple[int, int]) -> GardenSlot:
        return self.map[coord] if coord in self.map else None

    def get_infinite(self, coord: tuple[int, int]) -> GardenSlot:
        if coord in self.map:
            return self.map[coord]
        else:
            x, y = coord
            if y < self.min_y:
                infinite_n = True
                infinite_s = False
            elif y > self.max_y:
                infinite_s = True
                infinite_n = False
            else:
                infinite_n = infinite_s = False
            if x < self.min_x:
                infinite_w = True
                infinite_e = False
            elif x > self.max_x:
                infinite_e = True
                infinite_w = False
            else:
                infinite_e = infinite_w = False

            if y not in self.range_y:
                if infinite_n:
                    self.range_y = range(y, self.range_y.stop)
                else:
                    self.range_y = range(self.range_y.start, y + 1)
                for x in self.range_x:
                    self.map[(x, y)] = GardenSlot(
                            coord=(x, y),
                            slot=self.map[(
                                x % self.edge_size,
                                y % self.edge_size)].slot,
                            garden=self,
                            infinite_n=infinite_n,
                            infinite_s=infinite_s,
                            infinite_e=x > self.min_x,
                            infinite_w=x < self.min_x)
            if x not in self.range_x:
                if infinite_e:
                    self.range_x = range(self.range_x.start, x + 1)
                else:
                    self.range_x = range(x, self.range_x.stop)
                for y in self.range_y:
                    self.map[(x, y)] = GardenSlot(
                            coord=(x, y),
                            slot=self.map[(
                                x % self.edge_size,
                                y % self.edge_size)].slot,
                            garden=self,
                            infinite_n=y < self.min_y,
                            infinite_s=y > self.max_y,
                            infinite_e=infinite_e,
                            infinite_w=infinite_w)

            return self.map[coord]

    def __repr__(self):
        return '\n'.join(''.join(str(self.map[(x, y)])
                                 for x in self.range_x)
                         for y in self.range_y)

    @property
    def to_str_infinite(self):
        return '\n'.join(''.join(' '
                                 if (self.min_x <= x <= self.max_x
                                     and self.min_y <= y <= self.max_y)
                                 else str(self.map[(x, y)])
                                 for x in self.range_x)
                         for y in self.range_y)

    def do_steps(self,
                 *,
                 num_steps: int,
                 start: tuple[int, int] | None = None,
                 infinite: bool = False):
        if start is None:
            start_slot = self.start
        else:
            start_slot = self.map[start]
            start_slot.reached = True
            start_slot.reached_num_step = 0
        possible_steps = (
            start_slot.possible_steps_infinite if infinite
            else start_slot.possible_steps)
        for next_step in possible_steps:
            next_step.do_steps(num_step=1,
                               num_steps=num_steps,
                               infinite=infinite)

    @property
    def num_reached(self) -> tuple[int, int]:
        return (len([slot
                    for slot in self.map.values()
                    if slot.reached
                     and slot.reached_num_step % 2 == 0]),
                len([slot
                    for slot in self.map.values()
                    if slot.reached
                     and slot.reached_num_step % 2 == 1]))

    @property
    def num_reached_infinite(self) -> tuple[int, int]:
        return (len([slot
                     for slot in self.map.values()
                     if slot.reached and slot.infinite_nsew]),
                len([slot
                     for slot in self.map.values()
                     if slot.reached and slot.infinite_ne_se_sw_nw]))


def solve(*,
          step: int):
    print('*' * 20, f"Step {step}")

    garden_map: dict[tuple[int, int], str] = {}
    with (open('input.txt', 'r') as input_file):
        for y, line in enumerate(input_file.read().splitlines()):
            for x, slot in enumerate(line):
                garden_map[(x, y)] = slot

    if step == 1:
        garden = Garden(garden_map=garden_map)

        garden.do_steps(num_steps=64)
        (result, _) = garden.num_reached
        if print_progress[step - 1]:
            print()
            print()
            print(garden)
            print()
            print()
    else:
        num_steps = 26501365

        garden_whole = Garden(garden_map=garden_map)

        num_steps_whole_from_side = garden_whole.edge_size - 1 + garden_whole.edge_middle
        num_whole_gardens_one_direction = int((num_steps - garden_whole.edge_middle * 2)
                                              / garden_whole.edge_size)
        # num_steps_left = (num_steps - (garden.edge_middle + 1)) % garden.edge_size + 1
        num_steps_left = (num_steps
                          - num_whole_gardens_one_direction * garden_whole.edge_size
                          - garden_whole.edge_middle)
        num_steps_left_from_middle = num_steps_left + garden_whole.edge_middle

        num_straight_whole_gardens = (num_whole_gardens_one_direction * 2) + 1
        num_whole_gardens = (sum(range(1, num_straight_whole_gardens, 2)) * 2
                             + num_straight_whole_gardens)

        if print_progress[step - 1]:
            print(f"edge_size:{garden_whole.edge_size},"
                  f" edge_middle:{garden_whole.edge_middle},"
                  f" num_steps:{num_steps},"
                  f" num_steps_whole_from_side:{num_steps_whole_from_side},"
                  f" num_steps_left:{num_steps_left},"
                  f" num_steps_left_from_middle:{num_steps_left_from_middle}")
            print(f"num_whole_gardens_one_direction:{num_whole_gardens_one_direction},"
                  f" num_straight_whole_gardens:{num_straight_whole_gardens},"
                  f" num_whole_gardens:{num_whole_gardens}")

        garden_whole.do_steps(num_steps=num_steps_whole_from_side,
                              start=(0, garden_whole.edge_middle))
        num_reached_even, num_reached_odd = garden_whole.num_reached
        if garden_whole.edge_middle % 2 == num_steps % 2:
            num_even_gardens = (sum(range(1, num_straight_whole_gardens, 2)) * 2
                                 + num_straight_whole_gardens)
            num_even_gardens = (sum(range(1, num_straight_whole_gardens, 2)) * 2
                                 + num_straight_whole_gardens)
        else:
            num_even_gardens = (sum(range(1, num_straight_whole_gardens, 2)) * 2
                                 + num_straight_whole_gardens)
            num_even_gardens = (sum(range(1, num_straight_whole_gardens, 2)) * 2
                                 + num_straight_whole_gardens)

        if print_progress[step - 1]:
            print("Garden whole")
            print()
            print(garden_whole)
            print()
            print()

        if print_progress[step - 1]:
            print(f"  num_reached_whole_garden: {num_reached_whole_garden}")

        garden_left = Garden(garden_map=garden_map)
        garden_left.do_steps(num_steps=num_steps_left_from_middle,
                             reach_steps=reach_all_steps_left_from_middle,
                             infinite=True)

        if print_progress[step - 1]:
            print()
            print("Garden left steps")
            print()
            print(garden_left.to_str_infinite)
            print()
            print()

        (num_reached_nsew,
         num_reached_ne_se_sw_nw) = garden_left.num_reached_infinite

        result = (num_reached_whole_garden * num_whole_gardens
                  + num_reached_nsew
                  + num_reached_ne_se_sw_nw * num_whole_gardens_one_direction * 4)

    print('*' * 20, f"Step {step}", result)


if __name__ == '__main__':
    solve(step=1)
    solve(step=2)

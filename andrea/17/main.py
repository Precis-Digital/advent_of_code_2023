import functools
import heapq

print_progress = [False, False]

directions = ((0, 2), (1, 3), (2, 0), (3, 1))
offsets = ((1, 0), (0, 1), (-1, 0), (0, -1))
east = 0
south = 1
west = 2
north = 3


@functools.cache
def move(block: tuple[int, int],
         direction: int) -> tuple[int, int]:
    x, y = offsets[direction]
    return block[0] + x, block[1] + y


class Step:
    def __init__(self,
                 block: tuple[int, int],
                 direction: int,
                 num_straight: int,
                 lost_heat: int
                 ):
        self.block = block
        self.direction = direction
        self.num_straight = num_straight
        self.lost_heat = lost_heat

    def __hash__(self) -> int:
        return hash((self.block, self.direction, self.num_straight))

    def __eq__(self, other) -> bool:
        return (self.block == other.block
                and self.direction == other.direction
                and self.num_straight == other.num_straight)

    def __lt__(self, other: 'Step') -> bool:
        return self.lost_heat < other.lost_heat


def solve(*,
          step: int):
    print('*' * 20, f"Step {step}")

    city: dict[tuple[int, int], int] = {}

    with (open('input.txt', 'r') as input_file):
        for y, line in enumerate(input_file.read().splitlines()):
            y_max = y
            x_max = len(line) - 1
            city.update({(x, y): int(c) for x, c in enumerate(line)})

        destination = (x_max, y_max)

    def navigate():
        num_straight_must_turn = 3 if step == 1 else 10
        num_straight_can_turn = 0 if step == 1 else 4

        steps: list[Step] = [Step(block=(0, 0), direction=east, num_straight=0, lost_heat=0)]
        stepped: set[tuple[tuple[int, int], int, int]] = set()

        num_steps = 0
        while steps:
            if print_progress[step - 1]:
                num_steps += 1
                if (num_steps % 10000) == 0:
                    print(f"{str(num_steps).rjust(8)} steps, {str(len(steps)).rjust(8)}, {str(len(stepped)).rjust(8)}")

            current_step = heapq.heappop(steps)
            (block,
             direction,
             num_straight,
             lost_heat) = (current_step.block,
                           current_step.direction,
                           current_step.num_straight,
                           current_step.lost_heat)

            if block == destination:
                return lost_heat

            for direction_to, direction_from in directions:
                if direction_from == direction:
                    continue
                if direction_to == direction:
                    if num_straight == num_straight_must_turn:
                        continue
                    num_straight_to = num_straight + 1
                elif num_straight and num_straight < num_straight_can_turn:
                    continue
                else:
                    num_straight_to = 1

                x_to, y_to = block_to = move(block, direction_to)
                if (0 <= x_to <= x_max
                        and 0 <= y_to <= y_max):
                    if (block_to, direction_to, num_straight_to) in stepped:
                        continue
                else:
                    continue

                stepped.add((block_to, direction_to, num_straight_to))

                lost_heat_to = lost_heat + city[block_to]

                heapq.heappush(steps,
                               Step(block=block_to,
                                    direction=direction_to,
                                    num_straight=num_straight_to,
                                    lost_heat=lost_heat_to))

    result = navigate()

    print('*' * 20, f"Step {step}", result)


if __name__ == '__main__':
    solve(step=1)
    solve(step=2)

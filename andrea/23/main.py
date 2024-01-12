import functools
import itertools

print_progress = [False, False]


class Brick:
    def __init__(
            self,
            *,
            id: int,
            coord_1: tuple[int, int],
            coord_2: tuple[int, int],
            height: int,
            z: int):
        self.id = id
        self.coord_1 = coord_1
        self.coord_2 = coord_2
        self.height = height
        self.z = z
        self.holding: set['Brick'] = set()
        self.held_by: set['Brick'] = set()

    def __repr__(self) -> str:
        return (f"{str(self.id).rjust(4)} ({self.coord_1})-({self.coord_2}) {self.z}-{self.z_top}"
                f" {tuple(b.id for b in self.held_by)} <"
                f" {tuple(b.id for b in self.holding)}")

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value
        self.z_top = self.z + self.height

    @classmethod
    def add_from_input_line(
            cls,
            *,
            input_line_index: int,
            input_line: str,
            bricks: dict[int, set['Brick']]):
        coord_1, coord_2 = input_line.split('~')

        (x_1, y_1, z_1) = coord_1.split(',')
        (x_2, y_2, z_2) = coord_2.split(',')

        brick = cls(id=input_line_index + 1,
                    coord_1=(int(x_1), int(y_1)),
                    coord_2=(int(x_2), int(y_2)),
                    z=min(int(z_1), int(z_2)),
                    height=abs(int(z_1) - int(z_2)) + 1)

        if brick.z in bricks:
            bricks[brick.z].add(brick)
        else:
            bricks[brick.z] = {brick}

    @functools.cached_property
    def area(self) -> set[tuple[int, int]]:
        area: set[tuple[int, int]] = set()
        for x in range(min(self.coord_1[0], self.coord_2[0]),
                       max(self.coord_1[0], self.coord_2[0]) + 1):
            for y in range(min(self.coord_1[1], self.coord_2[1]),
                           max(self.coord_1[1], self.coord_2[1]) + 1):
                area.add((x, y))
        return area

    @property
    def free(self) -> bool:
        return all(len(held_brick.held_by) != 1
                   for held_brick in self.holding)

    def would_fall(self,
                   *,
                   disintegrated: set['Brick']):
        return self.held_by.issubset(disintegrated)

    def chain_disintegrate(
            self,
            *,
            disintegrated: set['Brick'] = None):
        if disintegrated is None:
            disintegrated = {self}
        would_fall = set(
                brick
                for brick in self.holding
                if brick.would_fall(disintegrated=disintegrated))
        disintegrated.update(would_fall)
        for brick in would_fall:
            brick.chain_disintegrate(disintegrated=disintegrated)
        return disintegrated

    def holds(self,
              *,
              brick: 'Brick'):
        self.holding.add(brick)
        brick.held_by.add(self)

    def fall_to(
            self,
            *,
            z: int,
            bricks: dict[int, set['Brick']],
            floor_area_z_top: dict[tuple[int, int], int],
            floor_area_bricks: dict[tuple[int, int], list['Brick']]):
        if self.z > z:
            bricks[self.z].remove(self)
            self.z = z
            if z in bricks:
                bricks[z].add(self)
            else:
                bricks[z] = {self}

        for coord in self.area:
            floor_area_z_top[coord] = self.z_top
            if coord in floor_area_bricks:
                top_brick = floor_area_bricks[coord][-1]
                if top_brick.z_top == self.z:
                    top_brick.holds(brick=self)
                floor_area_bricks[coord].append(self)
            else:
                floor_area_bricks[coord] = [self]


def solve(*,
          step: int):
    print('*' * 20, f"Step {step}")

    bricks: dict[int, set[Brick]] = {}
    with (open('input.txt', 'r') as input_file):
        for index_line, line in enumerate(input_file.read().splitlines()):
#         for index_line, line in enumerate(f"""1,0,1~1,2,1
# 0,0,2~2,0,2
# 0,2,3~2,2,3
# 0,0,4~0,2,4
# 2,0,5~2,2,5
# 0,1,6~2,1,6
# 1,1,8~1,1,9""".splitlines()):
            Brick.add_from_input_line(input_line_index=index_line,
                                      input_line=line,
                                      bricks=bricks)

    floor_bricks: set[Brick] = bricks[1]
    floor_area_z_top: dict[tuple[int, int], int] = {}
    floor_area_bricks: dict[tuple[int, int], list[Brick]] = {}
    for brick in floor_bricks:
        for coord in brick.area:
            floor_area_z_top[coord] = brick.z_top
            floor_area_bricks[coord] = [brick]

    falling_bricks: list[Brick] = sorted(
            [
                brick
                for z, z_bricks in bricks.items()
                if z > 1
                for brick in z_bricks],
            key=lambda b: b.z)

    # z_areas: dict[int, set[tuple[int, int]]] = {
    #     z: set(*brick.area
    #            for brick in z_bricks)
    #     for z, z_bricks in bricks.items()
    # }

    # z_s = sorted(bricks.keys())
    while falling_bricks:
        brick = falling_bricks.pop(0)
        z_below = max(floor_area_z_top.get(coord, 1)
                      for coord in brick.area)
        brick.fall_to(
                z=z_below,
                bricks=bricks,
                floor_area_z_top=floor_area_z_top,
                floor_area_bricks=floor_area_bricks)

    if step == 1:
        free_bricks = [brick
                   for z, z_bricks in bricks.items()
                   for brick in z_bricks
                   if brick.free]

        result = len(free_bricks)
    else:
        sum_num_other_bricks = 0
        for z, z_bricks in bricks.items():
            for brick in z_bricks:
                sum_num_other_bricks += len(brick.chain_disintegrate()) - 1

        result = sum_num_other_bricks

    print('*' * 20, f"Step {step}", result)


if __name__ == '__main__':
    solve(step=1)
    solve(step=2)

import functools

print_progress = [False, False]

directions = {1: (1, 0),
              2: (0, 1),
              3: (- 1, 0),
              4: (0, - 1)}

tile_to_direction = {
    '.': 0,
    '>': 1,
    '<': 3,
    'v': 2,
    '#': -1
}

direction_to_tile = {
    0: '.',
    1: '>',
    3: '<',
    2: 'v',
    -1: '#'
}


class TrailsMap:
    def __init__(self,
                 *,
                 array_map: list[list[int]]):
        self.array_map = array_map
        self.max_y = len(array_map) - 1
        self.max_x = len(array_map[0]) - 1
        self.start = ([x
                       for x in range(self.max_x + 1)
                       if self.array_map[0][x] == 0][0], 0)
        self.end = ([x
                     for x in range(self.max_x + 1)
                     if self.array_map[self.max_y][x] == 0][self.max_y], 0)

    @functools.cache
    def __getitem__(self, item: tuple[int, int]) -> int:
        x, y = item
        if (0 <= y <= self.max_y
                and 0 <= x < self.max_x):
            return self.array_map[y][x]
        else:
            return -1

    def print_path(self,
                   *,
                   path: 'Path'):
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                if (x, y) in path.tiles:
                    print(path.tiles.index((x, y)) % 10, end='')
                else:
                    print(direction_to_tile[self.array_map[y][x]], end='')
            print()

    def sorted_path_tiles(self,
                          *,
                          tile: tuple[int, int] = None) -> list[tuple[int, int]]:
        if tile is None:
            tile = self.start
        sorted_path_tiles = [tile]
        x, y = tile
        for to_tile in [(x + 1, y),
                        (x, y + 1),
                        (x - 1, y),
                        (x, y - 1)]:




class Path:
    def __init__(self,
                 *,
                 trails_map: TrailsMap,
                 start_or_next: tuple[int, int],
                 from_path: 'Path' = None):
        self.trails_map = trails_map
        if from_path:
            self.tiles = [*from_path.tiles, start_or_next]
        else:
            self.tiles = [start_or_next]
        self.end_y = self.trails_map.max_y

    @property
    def length(self) -> int:
        return len(set(self.tiles))

    def navigate(self,
                 *,
                 ignore_slopes: bool) -> list['Path']:
        other_paths: list['Path'] = []
        while True:
            x, y = self.tiles[-1]
            if y == self.end_y:
                return other_paths + [self]
            tile_direction = self.trails_map[x, y]
            if tile_direction > 0 and not ignore_slopes:
                x += directions[tile_direction][0]
                y += directions[tile_direction][1]
                if ((x, y) not in self.tiles
                        and self.trails_map[(x, y)] >= 0):
                    self.tiles.append((x, y))
                else:
                    return other_paths
            else:
                to_tiles = [
                    to_tile
                    for to_tile in [(x + 1, y),
                                    (x, y + 1),
                                    (x - 1, y),
                                    (x, y - 1)]
                    if (to_tile not in self.tiles
                        and self.trails_map[to_tile] >= 0)]
                if len(to_tiles) == 0:
                    return other_paths

                for to_tile in to_tiles[1:]:
                    other_paths.extend(
                            Path(trails_map=self.trails_map,
                                 start_or_next=to_tile,
                                 from_path=self).navigate(
                                    ignore_slopes=ignore_slopes))

                self.tiles.append(to_tiles[0])


def solve(*,
          step: int):
    print('*' * 20, f"Step {step}")

    array_map: list[list[int]] = []
    with (open('input.txt', 'r') as input_file):
        for line in input_file.read().splitlines():
            row = []
            array_map.append(row)
            for tile in line:
                row.append(tile_to_direction[tile])

    trails_map = TrailsMap(array_map=array_map)
    paths = Path(trails_map=trails_map,
                 start_or_next=(1, 0)).navigate(ignore_slopes=step == 2)

    paths.sort(key=lambda path: path.length, reverse=True)

    trails_map.print_path(path=paths[0])

    result = paths[0].length - 1

    print('*' * 20, f"Step {step}", result)


if __name__ == '__main__':
    solve(step=1)
    solve(step=2)

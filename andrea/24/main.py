import dataclasses
import functools
import numpy as np

print_progress = [False, False]


@dataclasses.dataclass(kw_only=True)
class Path:
    point: np.ndarray
    velocity: np.ndarray

    @classmethod
    def from_input_line(cls,
                        *,
                        input_line: str):
        point, velocity = input_line.split(' @ ')
        x, y, z = point.split(', ')
        x_v, y_v, z_v = velocity.split(', ')
        return cls(point=np.array([int(x), int(y), int(z)]),
                   velocity=np.array([int(x_v), int(y_v), int(z_v)]))

    @functools.cached_property
    def point_no_z(self):
        return self.point[:2]

    @functools.cached_property
    def velocity_no_z(self):
        return self.velocity[:2]

    def intersects(self,
                   *,
                   other: 'Path',
                   no_z: bool = False,
                   area: tuple[tuple[int, ...], tuple[int, ...]]) -> bool:
        if no_z:
            v1 = self.point_no_z.T
            c1 = self.velocity_no_z.T
            v2 = other.point_no_z.T
            c2 = other.velocity_no_z.T
        else:
            v1 = self.point.T
            c1 = self.velocity.T
            v2 = other.point.T
            c2 = other.velocity.T
        x, err, rank = np.linalg.lstsq(np.array([v1, -v2]).T, c2 - c1,
                                       rcond=-1)[:3]
        if rank == 2:
            intersection = v1 * x[0] + c1
            if no_z:
                if (area[0][0] <= intersection[0] <= area[0][1]
                        and area[1][0] <= intersection[1] <= area[1][1]):
                    return True
                else:
                    return False
            else:
                if (area[0][0] <= intersection[0] <= area[0][1]
                        and area[1][0] <= intersection[1] <= area[1][1]
                        and area[2][0] <= intersection[2] <= area[2][1]):
                    return True
                else:
                    return False
        else:
            return False
        # if rank == 2:
        #     print(v1 * x[0] + c1)
        # else:
        #     print("no intersection")


def solve(*,
          step: int):
    print('*' * 20, f"Step {step}")

    paths: list[Path] = []
    with (open('input.txt', 'r') as input_file):
        for index_line, line in enumerate(input_file.read().splitlines()):
            paths.append(Path.from_input_line(input_line=line))

    observation_area = ((200000000000000, 400000000000000),
                        (200000000000000, 400000000000000))

    num_intersections = 0

    for index, path in enumerate(paths):
        for path_2 in paths[index + 1:]:
            num_intersections += path.intersects(other=path_2,
                                                 no_z=True,
                                                 area=observation_area)

    result = num_intersections

    print('*' * 20, f"Step {step}", result)


if __name__ == '__main__':
    solve(step=1)
    #   solve(step=2)

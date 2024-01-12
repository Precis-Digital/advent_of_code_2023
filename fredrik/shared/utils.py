import functools
import inspect

Coordinate = tuple[int, int]


def read_input_to_string() -> str:
    day = inspect.stack()[1].filename.split("/")[-1].split(".")[0]
    with open(f"inputs/{day}.txt", "r") as file:
        return file.read()


def adjacent_indices(index: tuple[int, int]) -> set[tuple[int, int]]:
    return {
        (index[0] - 1, index[1] - 1),
        (index[0] - 1, index[1]),
        (index[0] - 1, index[1] + 1),
        (index[0], index[1] - 1),
        (index[0], index[1] + 1),
        (index[0] + 1, index[1] - 1),
        (index[0] + 1, index[1]),
        (index[0] + 1, index[1] + 1),
    }


@functools.cache
def cardinal_adjacent_indices(index: tuple[int, int]) -> list[Coordinate]:
    return [
        (index[0] - 1, index[1]),
        (index[0], index[1] - 1),
        (index[0], index[1] + 1),
        (index[0] + 1, index[1]),
    ]

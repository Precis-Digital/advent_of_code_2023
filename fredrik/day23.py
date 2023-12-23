import dataclasses

from shared import utils

type Coordinate = tuple[int, int]
type Graph = dict[Coordinate, dict[Coordinate, int]]


@dataclasses.dataclass(frozen=True)
class State:
    position: Coordinate
    steps: int = 0


@dataclasses.dataclass(frozen=True)
class StateWithSeen(State):
    seen: tuple[Coordinate, ...] = ()


def parse_map(map_raw: str) -> dict[Coordinate, str]:
    grid = {}
    for y, line in enumerate(map_raw.splitlines()):
        for x, char in enumerate(line):
            grid[(x, y)] = char

    return grid


def get_neighbors(
    position: Coordinate, grid: dict[Coordinate, str], slippery: bool
) -> list[Coordinate]:
    char = grid[position]
    if slippery and is_slope(char=char):
        neighbors = [get_next_from_slope(position=position, slope=char)]
    else:
        neighbors = utils.cardinal_adjacent_indices(index=position)

    valid_neighbors = []
    for neighbor in neighbors:
        if neighbor in grid and grid[neighbor] != "#":
            valid_neighbors.append(neighbor)

    return valid_neighbors


def trail_to_graph(
    trail: dict[Coordinate, str],
    start: Coordinate,
    goal: Coordinate,
    slippery: bool = True,
) -> Graph:
    choice_nodes = [start, goal]
    for position in trail:
        valid_neighbors = get_neighbors(
            position=position, grid=trail, slippery=slippery
        )

        if len(valid_neighbors) > 2:
            choice_nodes.append(position)

    graph = {node: {} for node in choice_nodes}

    for node in choice_nodes:
        queue = [State(position=node)]
        seen = {node}

        while queue:
            current = queue.pop()
            if current.position != node and current.position in choice_nodes:
                graph[node][current.position] = current.steps
                continue

            for candidate in get_neighbors(
                position=current.position, grid=trail, slippery=slippery
            ):
                if candidate not in seen:
                    queue.append(State(steps=current.steps + 1, position=candidate))
                    seen.add(candidate)

    return graph


def is_slope(char: str) -> bool:
    return char in {">", "<", "^", "v"}


def get_next_from_slope(position: Coordinate, slope: str) -> Coordinate:
    if slope == ">":
        return position[0] + 1, position[1]

    if slope == "<":
        return position[0] - 1, position[1]

    if slope == "^":
        return position[0], position[1] - 1

    if slope == "v":
        return position[0], position[1] + 1

    raise ValueError(f"Invalid slope: {slope}")


def find_longest_path(graph: Graph, start: Coordinate, goal: Coordinate) -> int:
    longest_path = 0

    queue = [StateWithSeen(position=start)]
    while queue:
        current = queue.pop()
        if current.position == goal:
            longest_path = max(longest_path, current.steps)
            continue

        for candidate, distance in graph[current.position].items():
            if candidate in current.seen:
                continue

            queue.append(
                StateWithSeen(
                    position=candidate,
                    steps=current.steps + distance,
                    seen=current.seen + (current.position,),
                )
            )

    return longest_path


def main() -> None:
    map_raw = utils.read_input_to_string()
    trail = parse_map(map_raw=map_raw)

    y_max = max(y for _, y in trail)
    x_max = max(x for x, _ in trail)

    start, goal = (1, 0), (x_max - 1, y_max)

    graph_slippery = trail_to_graph(trail=trail, start=start, goal=goal)
    graph = trail_to_graph(trail=trail, start=start, goal=goal, slippery=False)

    print(f"Part 1: {find_longest_path(graph=graph_slippery, start=start, goal=goal)}")
    print(f"Part 2: {find_longest_path(graph=graph, start=start, goal=goal)}")


if __name__ == "__main__":
    main()

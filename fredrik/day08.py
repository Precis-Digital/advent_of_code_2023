import itertools
import math
from typing import cast

from shared import utils

Network = dict[str, tuple[str, str]]

DIRECTION_MAP = {"L": 0, "R": 1}


def parse_route(route_raw: str) -> list[int]:
    return [DIRECTION_MAP[direction] for direction in route_raw]


def parse_network(network_raw: str) -> Network:
    network = {}
    for line in network_raw.splitlines():
        node, destinations = line.split(" = ")
        destinations = destinations.strip("()").split(", ")
        network[node] = tuple(destinations)

    return cast(Network, network)


def get_steps(network: Network, route: list[int], start: str, end: str) -> int:
    position = start
    count = 0
    for step in itertools.cycle(route):
        position = network[position][step]
        count += 1
        if position.endswith(end):
            break

    return count


def part1(network: dict[str, tuple[str, str]], route: list[int]) -> int:
    return get_steps(network=network, route=route, start="AAA", end="ZZZ")


def part2(network: dict[str, tuple[str, str]], route: list[int]) -> int:
    positions = {position for position in network if position.endswith("A")}
    counts = [
        get_steps(network=network, route=route, start=position, end="Z")
        for position in positions
    ]
    return math.lcm(*counts)


def main() -> None:
    route_raw, network_raw = utils.read_input_to_string().split("\n\n")
    route = parse_route(route_raw=route_raw)
    network = parse_network(network_raw=network_raw)

    count_part1 = part1(network=network, route=route)
    count_part2 = part2(network=network, route=route)

    print(f"Part 1: {count_part1}")
    print(f"Part 2: {count_part2}")


if __name__ == "__main__":
    main()

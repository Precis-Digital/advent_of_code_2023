from __future__ import annotations

import enum
import functools
import heapq
from typing import Self

from shared import utils

Coordinate = tuple[int, int]


class Direction(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()
    STILL = enum.auto()

    @functools.cached_property
    def opposite(self) -> Self:
        if self is Direction.UP:
            return Direction.DOWN
        if self is Direction.DOWN:
            return Direction.UP
        if self is Direction.LEFT:
            return Direction.RIGHT
        if self is Direction.RIGHT:
            return Direction.LEFT


def parse_heatmap(heat_map_raw: str) -> dict[Coordinate, int]:
    heat_map = {}
    for y, line in enumerate(heat_map_raw.splitlines()):
        for x, heat in enumerate(line.strip()):
            heat_map[(x, y)] = int(heat)

    return heat_map


def get_goal(heat_map: dict[Coordinate, int]) -> Coordinate:
    return list(heat_map.keys())[-1]


class State:
    __slots__ = ("heat_loss", "position", "direction", "direction_history", "ultra")

    def __init__(
        self,
        heat_loss: int = 0,
        position: Coordinate = (0, 0),
        direction: Direction = Direction.STILL,
        direction_history: int = 0,
        ultra: bool = False,
    ) -> None:
        self.heat_loss = heat_loss
        self.position = position
        self.direction = direction
        self.direction_history = direction_history
        self.ultra = ultra

    @property
    def must_turn(self) -> bool:
        if self.ultra:
            return self.direction_history == 10

        return self.direction_history == 3

    @property
    def can_stop_or_turn(self) -> bool:
        if self.direction is Direction.STILL or not self.ultra:
            return True

        return self.direction_history >= 4

    def __hash__(self) -> int:
        return hash((self.position, self.direction, self.direction_history))

    def __eq__(self, other: State) -> bool:
        return (
            self.position == other.position
            and self.direction == other.direction
            and self.direction_history == other.direction_history
        )

    def __lt__(self, other: State) -> bool:
        return self.heat_loss < other.heat_loss


@functools.cache
def get_direction(start: Coordinate, end: Coordinate) -> Direction:
    dx, dy = end[0] - start[0], end[1] - start[1]
    if dx == 0:
        return Direction.DOWN if dy > 0 else Direction.UP
    return Direction.RIGHT if dx > 0 else Direction.LEFT


def minimize_heatloss(heat_map: dict[Coordinate, int], ultra: bool = False) -> int:
    goal = get_goal(heat_map=heat_map)
    valid_positions = set(heat_map.keys())

    priority_queue = [State(ultra=ultra)]
    seen = set()

    while priority_queue:
        state = heapq.heappop(priority_queue)
        can_stop_or_turn, must_turn = state.can_stop_or_turn, state.must_turn

        if state.position == goal and can_stop_or_turn:
            return state.heat_loss

        if state in seen:
            continue

        seen.add(state)

        for candidate in utils.cardinal_adjacent_indices(index=state.position):
            if candidate not in valid_positions:
                continue

            direction = get_direction(start=state.position, end=candidate)
            if must_turn and direction == state.direction:
                continue

            if direction == state.direction.opposite:
                continue

            if not can_stop_or_turn and direction != state.direction:
                continue

            direction_history = (
                state.direction_history + 1 if direction == state.direction else 1
            )

            heapq.heappush(
                priority_queue,
                State(
                    heat_loss=state.heat_loss + heat_map[candidate],
                    position=candidate,
                    direction=direction,
                    direction_history=direction_history,
                    ultra=ultra,
                ),
            )


def main() -> None:
    heat_map_raw = utils.read_input_to_string()
    heat_map = parse_heatmap(heat_map_raw)

    print(f"Part 1: {minimize_heatloss(heat_map=heat_map)}")
    print(f"Part 2: {minimize_heatloss(heat_map=heat_map, ultra=True)}")


if __name__ == "__main__":
    main()

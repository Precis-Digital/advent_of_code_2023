from __future__ import annotations

import collections
import dataclasses
import enum
import functools
import math
from typing import Self

from shared import utils

type Module = FlipFlop | Conjunction | Broadcaster | Button


BUTTON = "button"
BROADCASTER = "broadcaster"
GOAL = "rx"


class Intensity(enum.Enum):
    LOW = enum.auto()
    HIGH = enum.auto()


@dataclasses.dataclass
class Pulse:
    intensity: Intensity
    sender: str
    destination: str


class State(enum.Enum):
    ON = enum.auto()
    OFF = enum.auto()

    @property
    def flip(self) -> Self:
        if self is State.OFF:
            return State.ON

        return State.OFF


@dataclasses.dataclass
class Button:
    name: str = BUTTON
    connections: list[str] = dataclasses.field(default_factory=list)

    def __post_init__(self) -> None:
        self.connections.append(BROADCASTER)

    def pulse(self, **_) -> list[Pulse]:
        pulses = []
        for connection in self.connections:
            pulses.append(
                Pulse(intensity=Intensity.LOW, sender=self.name, destination=connection)
            )
        return pulses


@dataclasses.dataclass
class Broadcaster:
    connections: list[str]
    name: str = BROADCASTER

    def pulse(self, received: Pulse) -> list[Pulse]:
        pulses = []
        for connection in self.connections:
            pulses.append(
                Pulse(
                    intensity=received.intensity,
                    sender=self.name,
                    destination=connection,
                )
            )
        return pulses


@dataclasses.dataclass
class FlipFlop:
    name: str
    connections: list[str]
    state: State = State.OFF

    def pulse(self, received: Pulse) -> list[Pulse]:
        if received.intensity is Intensity.HIGH:
            return []

        self.state = self.state.flip
        intensity = Intensity.HIGH if self.state is State.ON else Intensity.LOW

        pulses = []
        for connection in self.connections:
            pulses.append(
                Pulse(intensity=intensity, sender=self.name, destination=connection)
            )
        return pulses


@dataclasses.dataclass
class Conjunction:
    name: str
    connections: list[str]
    state: dict[str, Intensity] = dataclasses.field(default_factory=dict)

    def pulse(self, received: Pulse) -> list[Pulse]:
        self.state[received.sender] = received.intensity

        intensity = (
            Intensity.HIGH if Intensity.LOW in self.state.values() else Intensity.LOW
        )

        pulses = []
        for connection in self.connections:
            pulses.append(
                Pulse(intensity=intensity, sender=self.name, destination=connection)
            )

        return pulses


@dataclasses.dataclass
class ModuleConfiguration:
    nodes: dict[str, Module] = dataclasses.field(default_factory=dict)
    high_pulse_count: int = 0
    low_pulse_count: int = 0
    button_count: int = 0
    low_pulse_periods: dict[str, int] = dataclasses.field(default_factory=dict)

    @functools.cached_property
    def conjunction_before_goal(self) -> Conjunction:
        for node in self.nodes.values():
            if GOAL in node.connections:
                return node

    @property
    def found_all_goal_periods(self) -> bool:
        all_keys = self.conjunction_before_goal.state.keys()
        found_keys = self.low_pulse_periods.keys()
        return all_keys == found_keys

    def update_goal_periods(self) -> None:
        for key, value in self.conjunction_before_goal.state.items():
            if key in self.low_pulse_periods:
                continue

            if value is Intensity.HIGH:
                self.low_pulse_periods[key] = self.button_count

    @classmethod
    def from_raw(cls, modules_raw: str) -> Self:
        nodes, conjunctions = {}, []
        for module in modules_raw.splitlines():
            name, destinations = module.replace(" ", "").split("->")
            destinations = destinations.split(",")

            if name == BROADCASTER:
                nodes[name] = Broadcaster(connections=destinations)
                continue

            prefix, name = name[0], name[1:]
            if prefix == "%":
                nodes[name] = FlipFlop(name=name, connections=destinations)
            elif prefix == "&":
                conjunction = Conjunction(name=name, connections=destinations)
                nodes[name] = conjunction
                conjunctions.append(conjunction)
            else:
                raise ValueError(f"Unknown module type: {prefix}")

        for name, module in nodes.items():
            for conjunction in conjunctions:
                if conjunction.name in module.connections:
                    conjunction.state[name] = Intensity.LOW

        nodes[BUTTON] = Button()
        return cls(nodes=nodes)

    def increment_count(self, pulse: Pulse) -> None:
        if pulse.intensity is Intensity.HIGH:
            self.high_pulse_count += 1
        else:
            self.low_pulse_count += 1

    def push_button(self, find_goal: bool = False) -> None:
        self.button_count += 1

        queue = collections.deque(*[self.nodes[BUTTON].pulse()])
        while queue:
            pulse = queue.popleft()

            if find_goal:
                self.update_goal_periods()

            self.increment_count(pulse)
            if sender := self.nodes.get(pulse.destination):
                new_pulses = sender.pulse(received=pulse)
                queue.extend(new_pulses)


def part1(modules_raw: str) -> int:
    module_config = ModuleConfiguration.from_raw(modules_raw=modules_raw)

    for _ in range(1000):
        module_config.push_button()

    return module_config.high_pulse_count * module_config.low_pulse_count


def part2(modules_raw: str) -> int:
    module_config = ModuleConfiguration.from_raw(modules_raw=modules_raw)
    while not module_config.found_all_goal_periods:
        module_config.push_button(find_goal=True)

    return math.lcm(*module_config.low_pulse_periods.values())


def main() -> None:
    modules_raw = utils.read_input_to_string()

    print(f"Part 1: {part1(modules_raw=modules_raw)}")
    print(f"Part 2: {part2(modules_raw=modules_raw)}")


if __name__ == "__main__":
    main()

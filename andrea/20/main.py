import dataclasses
import re
from math import lcm

print_progress = [False, False]


@dataclasses.dataclass
class Pulse:
    source: 'Module'
    dest: 'Module'
    high_low: bool


@dataclasses.dataclass
class Module:
    type: str
    name: str
    destinations_names: list[str]
    high_low: bool = False

    _re_match = re.compile(r'^([%&]?)(\w+) -> (\w+(?:, \w+)*)$')

    def __post_init__(self):
        self.broadcaster = self.name == 'broadcaster'
        assert ((self.broadcaster and self.type == '')
                or (not self.broadcaster and self.type in {'%', '&', 'O'}))
        self.flip_flop = self.type == '%'
        self.conjunction = self.type == '&'
        self.goal = self.type == 'O'
        self.sources: dict['Module', bool] = {}
        self.destinations: list['Module'] = []

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: 'Module') -> bool:
        return self.name == other.name

    def __repr__(self):
        return f"{self.name} {int(self.high_low)}"

    @classmethod
    def from_input_line(cls,
                        *,
                        input_line: str):
        type_str, name, destinations = cls._re_match.fullmatch(input_line).groups()
        return cls(type=type_str,
                   name=name,
                   destinations_names=destinations.split(', '))

    def add_input(self,
                  *,
                  module: 'Module'):
        self.sources[module] = False

    @classmethod
    def complete(cls,
                 *,
                 modules: dict[str, 'Module']) -> tuple['Module', 'Module']:
        goal: 'Module' or None = None
        to_goal: 'Module' or None = None
        for module in modules.values():
            for destination_name in module.destinations_names:
                if destination_name in modules:
                    destination = modules[destination_name]
                else:
                    assert goal is None
                    assert to_goal is None
                    destination = goal = cls(
                            type='O',
                            name=destination_name,
                            destinations_names=[])
                    to_goal = module
                module.destinations.append(destination)
                destination.add_input(module=module)

        assert goal is not None
        assert to_goal is not None

        modules[goal.name] = goal

        return to_goal, goal

    @staticmethod
    def update_iterations_to_goal(
            *,
            source: 'Module',
            iteration: int | None = None,
            iterations_to_goal: dict['Module', int] | None = None):
        if iteration is not None and iterations_to_goal is not None:
            if (source in iterations_to_goal
                    and iterations_to_goal[source] == 0):
                iterations_to_goal[source] = iteration

    def pulse(self,
              *,
              high_low: bool,
              next_pulses: list[Pulse] | None = None,
              iteration: int | None = None,
              iterations_to_goal: dict['Module', int] | None = None,
              source: 'Module' = None) -> tuple[int, int]:
        num_high, num_low = int(high_low), int(not high_low)

        if self.goal:
            self.high_low = high_low
        elif self.broadcaster:
            next_pulses = []
            for destination in self.destinations:
                (num_high_loop,
                 num_low_loop) = destination.pulse(
                        high_low=high_low,
                        source=self,
                        next_pulses=next_pulses,
                        iteration=iteration,
                        iterations_to_goal=iterations_to_goal)
                num_high += num_high_loop
                num_low += num_low_loop

            while next_pulses:
                next_pulse = next_pulses.pop(0)
                (num_high_loop,
                 num_low_loop) = next_pulse.dest.pulse(
                        high_low=next_pulse.high_low,
                        source=next_pulse.source,
                        next_pulses=next_pulses,
                        iteration=iteration,
                        iterations_to_goal=iterations_to_goal)
                num_high += num_high_loop
                num_low += num_low_loop

        elif self.flip_flop:
            if high_low:
                self.update_iterations_to_goal(
                        source=source,
                        iteration=iteration,
                        iterations_to_goal=iterations_to_goal)
            if not high_low:
                self.high_low = not self.high_low
                for destination in self.destinations:
                    next_pulses.append(Pulse(
                            source=self,
                            dest=destination,
                            high_low=self.high_low))
                    # (num_high_loop,
                    #  num_low_loop) = destination.pulse(
                    #         high_low=self.high_low,
                    #         source=self,
                    #         next_pulses=next_pulses,
                    #         iteration=iteration,
                    #         iterations_to_goal=iterations_to_goal)
                    # num_high += num_high_loop
                    # num_low += num_low_loop

        elif self.conjunction:
            self.sources[source] = high_low
            if high_low:
                self.update_iterations_to_goal(
                        source=source,
                        iteration=iteration,
                        iterations_to_goal=iterations_to_goal)
            if all(self.sources.values()):
                for destination in self.destinations:
                    next_pulses.append(Pulse(
                            source=self,
                            dest=destination,
                            high_low=False))
                    # (num_high_loop,
                    #  num_low_loop) = destination.pulse(
                    #         high_low=False,
                    #         source=self,
                    #         next_pulses=next_pulses,
                    #         iteration=iteration,
                    #         iterations_to_goal=iterations_to_goal)
                    # num_high += num_high_loop
                    # num_low += num_low_loop
            else:
                for destination in self.destinations:
                    next_pulses.append(Pulse(
                            source=self,
                            dest=destination,
                            high_low=True))
                    # (num_high_loop,
                    #  num_low_loop) = destination.pulse(
                    #         high_low=True,
                    #         source=self,
                    #         next_pulses=next_pulses,
                    #         iteration=iteration,
                    #         iterations_to_goal=iterations_to_goal)
                    # num_high += num_high_loop
                    # num_low += num_low_loop
        else:
            raise ValueError(f"Invalid module type: {self.type}")

        return num_high, num_low


def solve(*,
          step: int):
    print('*' * 20, f"Step {step}")

    modules: dict[str, 'Module'] = {}
    broadcaster: Module or None = None
    with (open('input.txt', 'r') as input_file):
        for line in input_file.read().splitlines():
            module = Module.from_input_line(input_line=line)
            modules[module.name] = module
            if module.broadcaster:
                assert broadcaster is None
                broadcaster = module

    assert broadcaster is not None

    to_goal, goal = Module.complete(modules=modules)

    if step == 1:
        num_high, num_low = 0, 0
        for _ in range(1, 1001):
            num_high_loop, num_low_loop = broadcaster.pulse(high_low=False)
            num_high += num_high_loop
            num_low += num_low_loop

        result = num_high * num_low
    else:
        num_pushes = 0
        iterations_to_goal: dict[Module, int] = {
            module: 0
            for module in to_goal.sources.keys()}
        while any(iterations == 0
                  for iterations in iterations_to_goal.values()):
            num_pushes += 1
            broadcaster.pulse(high_low=False,
                              iteration=num_pushes,
                              iterations_to_goal=iterations_to_goal)

        result = lcm(*iterations_to_goal.values())

    print('*' * 20, f"Step {step}", result)


if __name__ == '__main__':
    solve(step=1)
    solve(step=2)

import functools

print_progress = [False, False]


class Wire:
    left: 'Component'
    right: 'Component'
    wires: set['Wire']

    def __init__(self,
                 *,
                 left: 'Component',
                 right: 'Component'):
        if left < right:
            self.left = left
            self.right = right
        else:
            self.left = right
            self.right = left

        left.wires.append(self)
        right.wires.append(self)

    @classmethod
    def make_name(cls,
                  *,
                  left: str | 'Component',
                  right: str | 'Component') -> str:
        return f"{left}-{right}"

    @functools.cached_property
    def name(self):
        return self.make_name(left=self.left,
                              right=self.right)

    @classmethod
    def from_input(cls,
                   *,
                   names: tuple[str, str],
                   wires: dict[str, 'Wire'],
                   components: dict[str, 'Component']):
        left_name, right_name = sorted(names)
        if not Wire.make_name(left=left_name,
                              right=right_name) in wires:
            if left_name in components:
                left = components[left_name] = Component(name=left_name)
            else:
                left = components[left_name]
            if right_name in components:
                right = components[right_name] = Component(name=right_name)
            else:
                right = components[right_name]
            wire = cls(left=left, right=right)
            wires[wire.name] = wire

    #    def __hash__(self) -> int:
    #        return hash((self.left, self.right))

    @functools.cached_property
    def split_components(self) -> tuple[set['Component'], set['Component']]:
        left_components: set['Component'] = set()
        right_components: set['Component'] = set()
        passed_wires: set['Wire'] = set()

        return left_components, right_components

    def navigate(self,
                 *,
                 from_component: 'Component',
                 components: set['Component'],
                 wires: set['Wire']):
        if self in wires:
            return
        if from_component == self.left:
            self.right.navigate(from_wire=self,
                                components=components)
        else:
            self.left.navigate(from_wire=self,
                               components=components)


class Component:
    wires: list[Wire]

    def __init__(self,
                 *,
                 name: str):
        self.name = name

    @functools.cached_property
    def __repr__(self):
        return self.name

    @functools.cached_property
    def __hash__(self):
        return hash(self.name)

    @functools.cache
    def __lt__(self, other):
        return self.name < other.name

    def navigate(self,
                 *,
                 from_wire: Wire = None,
                 components: set['Component'],
                 wires: set[Wire]):
        if self in components:
            return
        components.add(self)
        for wire in self.wires:
            if from_wire is None or wire != from_wire:
                wire.navigate(from_component=self,
                              components=components,
                              wires=wires)


def solve(*,
          step: int):
    print('*' * 20, f"Step {step}")

    wires: dict[str, Wire] = {}
    components: dict[str, Component] = {}
    with (open('input.txt', 'r') as input_file):
        for index_line, line in enumerate(input_file.read().splitlines()):
            start, ends = line.split(': ')
            for end in ends.split(' '):
                Wire.from_input(names=(start, end),
                                components=components,
                                wires=wires)

    result = 0

    print('*' * 20, f"Step {step}", result)


if __name__ == '__main__':
    solve(step=1)
    solve(step=2)

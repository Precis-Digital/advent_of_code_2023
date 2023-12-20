import dataclasses
import re

print_progress = [False, False]


@dataclasses.dataclass
class RuleRange:
    x: range
    m: range
    a: range
    s: range

    def __getitem__(self, item) -> range:
        return getattr(self, item)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    @classmethod
    def replace_range(cls,
                      *,
                      other: 'RuleRange',
                      key: str,
                      new_range: range):
        new_ranges = cls(x=other.x,
                         m=other.m,
                         a=other.a,
                         s=other.s)
        new_ranges[key] = new_range
        return new_ranges

    def no_intersection(self,
                        *,
                        other_range: 'RuleRange'):
        return ((min(self.x.stop, other_range.x.stop)
                 - max(self.x.start, other_range.x.start)) <= 0
                or (min(self.m.stop, other_range.m.stop)
                    - max(self.m.start, other_range.m.start)) <= 0
                or (min(self.a.stop, other_range.a.stop)
                    - max(self.a.start, other_range.a.start)) <= 0
                or (min(self.s.stop, other_range.s.stop)
                    - max(self.s.start, other_range.s.start)) <= 0)


@dataclasses.dataclass
class WorkflowRule:
    parameter: str
    clause: str
    value: int
    then_workflow: str

    _re_rule_part = re.compile(r'(\w+)([<>])(\d+):(\w+)$')

    def __post_init__(self):
        self._then_accept = self.then_workflow == 'A'
        self._then_reject = self.then_workflow == 'R'

    @classmethod
    def from_input_rule(cls,
                        *,
                        input_rule: str) -> 'WorkflowRule':
        (parameter,
         clause,
         value,
         then_workflow) = cls._re_rule_part.fullmatch(input_rule).groups()
        return cls(parameter=parameter,
                   clause=clause,
                   value=int(value),
                   then_workflow=then_workflow)

    def __repr__(self):
        return f"{self.parameter}{self.clause}{self.value} -> {self.then_workflow}"

    def rating_match_rule(self,
                          *,
                          step: int,
                          rating: 'Rating') -> bool:
        if print_progress[step - 1] > 1:
            print(f"  {self.parameter}{self.clause}{self.value}", end='')
        match self.clause:
            case '>':
                if rating[self.parameter] > self.value:
                    if print_progress[step - 1] > 1:
                        print(f" -> {self.then_workflow}")
                    return True
            case '<':
                if rating[self.parameter] < self.value:
                    if print_progress[step - 1] > 1:
                        print(f" -> {self.then_workflow}")
                    return True
        if print_progress[step - 1] > 1:
            print()
        return False

    def get_accept_ranges(
            self,
            *,
            step: int,
            workflows: dict[str, 'Workflow'],
            accept_ranges: list[RuleRange],
            alternate_ranges: list[RuleRange],
            ranking_ranges: list['RuleRange']):

        for ranking_range in ranking_ranges:
            parameter_range = ranking_range[self.parameter]

            if print_progress[step - 1] > 1:
                print(f"  {self.parameter}{self.clause}{str(self.value).ljust(5)} {ranking_range}")

            match self.clause:
                case '>':
                    passing_range = range(
                            max(parameter_range.start, self.value + 1),
                            parameter_range.stop)
                    alternate_range = range(
                            parameter_range.start,
                            min(parameter_range.stop, self.value + 1))
                case '<':
                    passing_range = range(
                            parameter_range.start,
                            min(parameter_range.stop, self.value))
                    alternate_range = range(
                            max(parameter_range.start, self.value),
                            parameter_range.stop)
                case _:
                    raise ValueError(f"Invalid clause: {self.clause}")

            if alternate_range.start < alternate_range.stop:
                alternate_ranges.append(
                        RuleRange.replace_range(
                                other=ranking_range,
                                key=self.parameter,
                                new_range=alternate_range))
                if print_progress[step - 1] > 1:
                    print(f"    split  {alternate_ranges[-1]}")

            if passing_range.start < passing_range.stop:
                new_ranking_range = RuleRange.replace_range(
                        other=ranking_range,
                        key=self.parameter,
                        new_range=passing_range)
                if self._then_accept:
                    accept_ranges.append(new_ranking_range)
                    if print_progress[step - 1] > 1:
                        print(f"    Accept {new_ranking_range}")
                elif not self._then_reject:
                    if print_progress[step - 1] > 1:
                        print(f"    {self.then_workflow.rjust(6)} {new_ranking_range}")
                    workflows[self.then_workflow].get_accept_ranges(
                            step=step,
                            workflows=workflows,
                            accept_ranges=accept_ranges,
                            ranking_ranges=[new_ranking_range])


@dataclasses.dataclass
class Workflow:
    name: str
    rules: list[WorkflowRule]
    else_workflow: str

    _re_input = re.compile(r'^(\w+)\{([^}]+)}$')

    def __post_init__(self):
        self._else_accept = self.else_workflow == 'A'
        self._else_reject = self.else_workflow == 'R'

    @classmethod
    def from_input_rules(cls,
                         *,
                         input_rules: list[str]) -> list['WorkflowRule']:
        return [WorkflowRule.from_input_rule(input_rule=input_rule)
                for input_rule in input_rules]

    @classmethod
    def from_input_line(cls,
                        *,
                        input_line: str):
        name, input_rules = cls._re_input.fullmatch(input_line).groups()
        input_rules = input_rules.split(',')
        return cls(name=name,
                   rules=cls.from_input_rules(input_rules=input_rules[:-1]),
                   else_workflow=input_rules[-1])

    def rating_to_workflow(self,
                           *,
                           step: int,
                           rating: 'Rating') -> str:
        for rule in self.rules:
            if rule.rating_match_rule(step=step,
                                      rating=rating):
                return rule.then_workflow
        return self.else_workflow

    def get_accept_ranges(
            self,
            *,
            step: int,
            workflows: dict[str, 'Workflow'],
            accept_ranges: list[RuleRange],
            ranking_ranges: list[RuleRange]):

        for rule in self.rules:
            if print_progress[step - 1] > 1:
                print(f" {self.name.ljust(5)} {rule}")
            rule_alternate_ranges: list[RuleRange] = []
            rule.get_accept_ranges(
                    step=step,
                    workflows=workflows,
                    accept_ranges=accept_ranges,
                    alternate_ranges=rule_alternate_ranges,
                    ranking_ranges=ranking_ranges)
            ranking_ranges = rule_alternate_ranges

        if self._else_accept:
            accept_ranges.extend(ranking_ranges)
        elif not self._else_reject:
            workflows[self.else_workflow].get_accept_ranges(
                    step=step,
                    workflows=workflows,
                    accept_ranges=accept_ranges,
                    ranking_ranges=ranking_ranges)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Rating:
    x: int
    m: int
    a: int
    s: int

    _re_input = re.compile(r'^\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}$')

    @classmethod
    def from_input_line(cls,
                        *,
                        input_line: str) -> 'Rating':
        x, m, a, s = cls._re_input.fullmatch(input_line).groups()
        return cls(x=int(x),
                   m=int(m),
                   a=int(a),
                   s=int(s))

    def __getitem__(self, item: str) -> int:
        return getattr(self, item)

    def accept_value(self,
                     *,
                     step: int,
                     workflows: dict[str, Workflow]) -> int:
        if print_progress[step - 1] > 1:
            print(f"{{x={self.x},m={self.m},a={self.a},s={self.s}}}:")
        result = workflows['in'].rating_to_workflow(step=step,
                                                    rating=self)
        while result not in {'A', 'R'}:
            result = workflows[result].rating_to_workflow(step=step,
                                                          rating=self)

        assert result in {'A', 'R'}

        if print_progress[step - 1]:
            print(f" {(self.x + self.m + self.a + self.s) if result == 'A' else 0}")

        return (self.x + self.m + self.a + self.s) if result == 'A' else 0


def solve(*,
          step: int):
    print('*' * 20, f"Step {step}")

    workflows: dict[str, Workflow] = {}
    ratings: list[Rating] = []
    with (open('input.txt', 'r') as input_file):
        lines = input_file.read().splitlines()
        split_line = lines.index('')

        for line in lines[:split_line]:
            workflow = Workflow.from_input_line(input_line=line)
            assert workflow.name not in workflows
            workflows[workflow.name] = workflow

        if step == 1:
            for line in lines[split_line + 1:]:
                rating = Rating.from_input_line(input_line=line)
                ratings.append(rating)

    if step == 1:
        accept_values = [rating.accept_value(step=step,
                                             workflows=workflows)
                         for rating in ratings]

        result = sum(accept_values)
    else:
        start_range = RuleRange(x=range(1, 4001),
                                m=range(1, 4001),
                                a=range(1, 4001),
                                s=range(1, 4001))
        accept_ranges: list[RuleRange] = []
        workflows['in'].get_accept_ranges(
                step=step,
                workflows=workflows,
                accept_ranges=accept_ranges,
                ranking_ranges=[start_range])

        if print_progress[step - 1] > 1:
            print('\n'.join(f"{accept_range.x} {accept_range.m} {accept_range.a} {accept_range.s}"
                            for accept_range in accept_ranges))

        assert all(all(first_range.no_intersection(other_range=second_range)
                       for second_range in (accept_ranges[:index_first]
                                            + accept_ranges[index_first + 1:]))
                   for index_first, first_range in enumerate(accept_ranges))

        result = 0
        for accept_range in accept_ranges:
            result += ((accept_range.x.stop - accept_range.x.start)
                       * (accept_range.m.stop - accept_range.m.start)
                       * (accept_range.a.stop - accept_range.a.start)
                       * (accept_range.s.stop - accept_range.s.start))

    print('*' * 20, f"Step {step}", result)


if __name__ == '__main__':
    solve(step=1)
    solve(step=2)

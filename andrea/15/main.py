import functools
import re

print_progress = [False, False]

re_lens = re.compile(r'(\w+)([-=])(\d+)?')


@functools.cache
def hash_string(*,
                string: str) -> int:
    hash_result = 0
    for c in string:
        hash_result = ((hash_result + ord(c)) * 17) % 256
    return hash_result


@functools.cache
def process_sequence(*,
                     sequence: str) -> (str, int, str, int):
    groups = re_lens.match(sequence).groups()
    return (groups[0],
            hash_string(string=groups[0]),
            groups[1],
            int(groups[2]) if groups[2] else 0)


def solve(*,
          step: int):
    print('*' * 20, f"Step {step}")

    result = 0
    if step == 1:
        with (open('input.txt', 'r') as input_file):
            for index_line, line in enumerate(input_file.read().splitlines()):
                for sequence in line.split(','):
                    result += hash_string(string=sequence)
    else:
        lenses_focal: dict[str, int] = {}
        boxes: list[list[str]] = [list() for _ in range(256)]
        with (open('input.txt', 'r') as input_file):
            for index_line, line in enumerate(input_file.read().splitlines()):
                for sequence in line.split(','):
                    label, label_hash, operator, focal = process_sequence(sequence=sequence)
                    box = boxes[label_hash]
                    if label in box:
                        if operator == '-':
                            box.remove(label)
                        else:
                            lenses_focal[label] = focal
                    else:
                        if operator == '=':
                            box.append(label)
                            lenses_focal[label] = focal
        for index_box, box in enumerate(boxes):
            for index_slot, label in enumerate(box):
                result += (index_box + 1) * (index_slot + 1) * lenses_focal[label]

    print('*' * 20, f"Step {step}", result)


if __name__ == '__main__':
    solve(step=1)
    solve(step=2)

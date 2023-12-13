import functools
import re

print_progress = [False, False]

re_sequences = re.compile(r'(\d+)')


@functools.cache
def iterate_combinations(*,
                         step: int,
                         springs: str,
                         lengths: tuple[int, ...]):
    if not springs:
        if print_progress[step - 1] == 2:
            print('{springs} {lengths}\n'
                  'Fail end input' if lengths else 'Success')

        return 0 if lengths else 1

    if not lengths:
        if print_progress[step - 1] == 2:
            print(f'{springs} {lengths}\n'
                  f'Fail # in the leftover springs' if '#' in springs else 'Success')
        return 0 if '#' in springs else 1

    if len(springs) < sum(lengths) + (len(lengths) - 1):
        if print_progress[step - 1] == 2:
            print(f'{springs} {lengths}\n'
                  f'Fail not enough space for all sequences'
                  f' {len(springs)} < {sum(lengths) + (len(lengths) - 1)}')
        return 0

    length = lengths[0]
    if '.' in springs[:length]:
        index = springs.index('.')
        if '#' in springs[:index]:
            if print_progress[step - 1] == 2:
                print(f'{springs} {lengths}\n'
                      f'. inside length of next sequence, fail because # before')
            return 0
        if print_progress[step - 1] == 2:
            print(f'{springs} {lengths}\n'
                  f'. inside length of next sequence, restart after')
        return iterate_combinations(
                step=step,
                springs=springs[springs.index('.') + 1:],
                lengths=lengths)

    if len(springs) == length:
        if print_progress[step - 1] == 2:
            print(f'{springs} {lengths}\n'
                  f'leftover exact length of last sequence')
        return 1

    match springs[0]:
        case '#':
            if springs[length] == '#':
                if print_progress[step - 1] == 2:
                    print(f'{springs} {lengths}\n'
                          f'#{"-" * (length - 1)} followed by #, so fail')
                return 0

            if print_progress[step - 1] == 2:
                print(f'{springs} {lengths}\n'
                      f'#{"-" * (length - 1)} not followed by #'
                      f' so restart after {"#" * length}.')
            return iterate_combinations(
                    step=step,
                    springs=springs[length + 1:],
                    lengths=lengths[1:])
        case '?':
            match springs[length]:
                case '#':
                    if print_progress[step - 1] == 2:
                        print(f'{springs} {lengths}\n'
                              f'?{"-" * (length - 1)} followed by #'
                              f' so try only with .#{"-" * (length - 1)}#')
                    return iterate_combinations(
                            step=step,
                            springs=springs[1:],
                            lengths=lengths)
                case '.':
                    if '#' in springs[:length]:
                        if print_progress[step - 1] == 2:
                            print(f'{springs} {lengths}\n'
                                  f'?{"-" * (length - 1)} with # inside followed by .,'
                                  f' try only with {"#" * length}.')
                        return iterate_combinations(
                                step=step,
                                springs=springs[length + 1:],
                                lengths=lengths[1:])
                    else:
                        if print_progress[step - 1] == 2:
                            print(f'{springs} {lengths}\n'
                                  f'?{"-" * (length - 1)} followed by .,'
                                  f' try {"." * length}. ...')
                        combinations = iterate_combinations(
                                step=step,
                                springs=springs[length + 1:],
                                lengths=lengths)

                        if print_progress[step - 1] == 2:
                            print(f'{springs} {lengths}\n'
                                  f'?{"-" * (length - 1)} followed by .,'
                                  f'     {" " * length}  ... and {"#" * length}.')
                        combinations += iterate_combinations(
                                step=step,
                                springs=springs[length + 1:],
                                lengths=lengths[1:])
                        return combinations

                case '?':
                    if print_progress[step - 1] == 2:
                        print(f'{springs} {lengths}\n'
                              f'?{"-" * (length - 1)}?, try .{"-" * length}? ...')
                    combinations = iterate_combinations(
                            step=step,
                            springs=springs[1:],
                            lengths=lengths)

                    if print_progress[step - 1] == 2:
                        print(f'{springs} {lengths}\n'
                              f'?{"-" * (length - 1)}?,       ... and {"#" * length}.')
                    combinations += iterate_combinations(
                            step=step,
                            springs=springs[length + 1:],
                            lengths=lengths[1:])
                    return combinations


def solve(*,
          step: int):
    print('*' * 20, f"Step {step}")

    result = 0

    with (open('input.txt', 'r') as input_file):
        for index, line in enumerate(input_file.read().splitlines()):
            springs, sequences_lengths = line.split(' ')

            sequences_lengths = tuple(int(length) for length in re_sequences.findall(sequences_lengths))

            if step == 2:
                springs = '?'.join([springs] * 5)
                sequences_lengths = sequences_lengths * 5

            combinations = iterate_combinations(
                    step=step,
                    springs=springs,
                    lengths=sequences_lengths)

            if print_progress[step - 1] == 1:
                print(str(index + 1).rjust(4), springs[:int((len(springs) - 4) / 5)].rjust(40), combinations)

            assert combinations > 0

            result += combinations

    print('*' * 20, f"Step {step}", result)


if __name__ == '__main__':
    solve(step=1)
    solve(step=2)

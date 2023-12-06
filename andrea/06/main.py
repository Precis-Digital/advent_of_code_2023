import re

re_end_line = re.compile(r'\r?\n?$')
re_time_distance = re.compile(r'^(Time|Distance):')
re_numbers = re.compile(r'\b(\d+)')
re_clean_spaces = re.compile(r'\s+')

print_progress = False


def solve_06(*,
             step: int):
    print('*' * 20, f"Step {step}")

    times = None
    distances = None

    with (open('input.txt', 'r') as input_file):
        for game_line in input_file:
            time_distance = re_time_distance.match(game_line)
            if step == 2:
                game_line = re_clean_spaces.sub('', game_line)
            if time_distance.group(1) == 'Time':
                times = [int(number)
                         for number in re_numbers.findall(game_line)]
            else:
                distances = [int(number)
                             for number in re_numbers.findall(game_line)]

    if times is None or distances is None:
        raise ValueError('Missing Time or Distance')

    result = 1

    for race_time, record_distance in zip(times, distances):
        half_time = int(race_time / 2)
        num_tries = 0
        for step_time in range(half_time):
            prev_num_tries = num_tries
            if step_time:
                hold_time = half_time - step_time
                if hold_time * (race_time - hold_time) > record_distance:
                    num_tries += 1
                    if print_progress:
                        print(f"  {str(num_tries).rjust(4)}"
                              f" {race_time} {record_distance}"
                              f" - {hold_time} {hold_time * (race_time - hold_time)}")
                hold_time = half_time + step_time
                if hold_time * (race_time - hold_time) > record_distance:
                    num_tries += 1
                    if print_progress:
                        print(f"  {str(num_tries).rjust(4)}"
                              f" {race_time} {record_distance}"
                              f" - {hold_time} {hold_time * (race_time - hold_time)}")
            else:
                if half_time * (race_time - half_time) > record_distance:
                    num_tries += 1
                    if print_progress:
                        print(f"  {str(num_tries).rjust(4)}"
                              f" {race_time} {record_distance}"
                              f" - {half_time} {half_time * (race_time - half_time)}")

            if prev_num_tries == num_tries:
                break

        result *= num_tries

    print('*' * 20, f"Step {step}", result)


if __name__ == '__main__':
    solve_06(step=1)
    solve_06(step=2)

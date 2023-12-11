import math
import re

print_progress = [False, False]

re_end_line = re.compile(r'\r?\n?$')
re_readings = re.compile(r'(-?\d+)')


class Sensor:
    def __init__(self,
                 *,
                 readings: str):
        self.readings = [int(reading.group(1)) for reading in re_readings.finditer(readings)]

    def find_next_reading(self,
                          *,
                          step: int):
        readings_sequences = [self.readings]

        while True:
            prev_readings = readings_sequences[-1]
            readings = [reading - prev_readings[index]
                        for index, reading in enumerate(prev_readings[1:])]
            if math.lcm(*readings) == math.gcd(*readings):
                if step == 1:
                    readings.append(readings[-1])
                else:
                    readings.insert(0, readings[0])
                if print_progress[step - 1]:
                    if step == 1:
                        print(f"  {readings[:-1]} -> {readings[-1]}")
                    else:
                        print(f"  {readings[0]} <- {readings[1:]}")
                while readings_sequences:
                    if step == 1:
                        difference = readings[-1]
                    else:
                        difference = readings[0]
                    readings = readings_sequences.pop()
                    if step == 1:
                        readings.append(readings[-1] + difference)
                    else:
                        readings.insert(0, readings[0] - difference)
                    if print_progress[step - 1]:
                        if step == 1:
                            print(f"  {readings[:-1]} -> {readings[-1]}")
                        else:
                            print(f"  {readings[0]} <- {readings[1:]}")
                if step == 1:
                    return readings[-1]
                else:
                    return readings[0]
            else:
                readings_sequences.append(readings)


def solve(*,
          step: int):
    print('*' * 20, f"Step {step}")

    result = 0
    with (open('input.txt', 'r') as input_file):
        for game_line in input_file:
            result += Sensor(readings=game_line).find_next_reading(step=step)

    print('*' * 20, f"Step {step}", result)


if __name__ == '__main__':
    solve(step=1)
    solve(step=2)

import functools
from numpy import shape, array, flip, arange, ndarray

from utils.utils import performance

print_progress = [False, False]

directions_fall_array = {
    'N': array(('.', 'O')),
    'W': array(('.', 'O')),
    'S': array(('O', '.')),
    'E': array(('O', '.'))
}


@functools.cache
def tilt_line(*,
              step: int,
              line: str,
              direction: str) -> tuple[str, bool]:
    if print_progress[step - 1] >= 2:
        print(f" in {line}")

    if direction in ('N', 'W'):
        if '.O' in line:
            new_column = '#'.join(('O' * part.count('O')
                                   + '.' * part.count('.')) if part else ''
                                  for part in line.split('#'))
            return tilt_line(
                    step=step,
                    line=new_column,
                    direction=direction)[0], True
        else:
            if print_progress[step - 1] >= 2:
                print(f"out {line}")
            return line, False
    else:
        if 'O.' in line:
            new_column = '#'.join(('.' * part.count('.')
                                   + 'O' * part.count('O')) if part else ''
                                  for part in line.split('#'))
            return tilt_line(
                    step=step,
                    line=new_column,
                    direction=direction)[0], True
        else:
            if print_progress[step - 1] >= 2:
                print(f"out {line}")
            return line, False


def search_sequence_numpy(*,
                          arr: ndarray,
                          seq: ndarray) -> bool:
    """ Find sequence in an array using NumPy only.

    Parameters
    ----------
    arr    : input 1D array
    seq    : input 1D array

    Output
    ------
    Output : Boolean
    """

    # Store sizes of input array and sequence
    Na, Nseq = arr.size, seq.size

    # Range of sequence
    r_seq = arange(Nseq)

    # Create a 2D array of sliding indices across the entire length of input array.
    # Match up with the input sequence & get the matching starting indices.
    M = (arr[arange(Na - Nseq + 1)[:, None] + r_seq] == seq).all(1)

    # Get the range of those indices as final output
    return M.any() > 0


def tilt_platform(*,
                  step: int,
                  platform: ndarray,
                  iter_axis_rows: int,
                  iter_axis_columns: int,
                  direction: str):
    as_rows = direction in ('N', 'S')

    global_moved = False

    if as_rows:
        for row_index in range(iter_axis_rows):
            if search_sequence_numpy(arr=platform[:, row_index],
                                     seq=directions_fall_array[direction]):
                column, moved = tilt_line(
                        step=step,
                        line=''.join(platform[:, row_index]),
                        direction=direction)
                platform[:, row_index] = tuple(column)
                global_moved |= moved
    else:
        for column_index in range(iter_axis_columns):
            if search_sequence_numpy(arr=platform[column_index],
                                     seq=directions_fall_array[direction]):
                column, moved = tilt_line(
                        step=step,
                        line=''.join(platform[column_index]),
                        direction=direction)
                platform[column_index] = tuple(column)
                global_moved |= moved

    return global_moved


def platform_hash(*,
                  platform: ndarray,
                  direction: str) -> str:
    return (direction
            + '\n'
            + '\n'.join(''.join(line) for line in platform))


def tilt_platform_or_use_hash(
        *,
        step: int,
        platform: ndarray,
        iter_axis_rows: int,
        iter_axis_columns: int,
        direction: str,
        from_hashes: list[str],
        to_hashes: list[str],
        sequences_done: int,
        limit: int) -> int:
    sequences_left_to_do = limit - sequences_done

    from_hash = platform_hash(platform=platform,
                              direction=direction)
    if from_hash in from_hashes and direction == 'N':
        found_index = from_hashes.index(from_hash)
        if print_progress[step - 1]:
            print(f"Cache Hit {sequences_done}")
            print(from_hash)
        if sequences_left_to_do:
            sequences_available = len(from_hashes) - found_index
            if sequences_available <= sequences_left_to_do:
                step_to = (found_index
                           + (sequences_left_to_do
                              % sequences_available))
            else:
                step_to = (found_index
                           + sequences_left_to_do)
            sequences_done += sequences_left_to_do
        else:
            step_to = found_index

        if sequences_done < limit:
            to_hash: str = to_hashes[step_to]
        else:
            to_hash: str = from_hashes[step_to]

        for index, line in enumerate(to_hash.split('\n')[1:]):
            platform[index] = list(line)

        return sequences_done

    from_hashes.append(from_hash)

    tilt_platform(step=step,
                  platform=platform,
                  iter_axis_rows=iter_axis_rows,
                  iter_axis_columns=iter_axis_columns,
                  direction=direction)

    to_hash = platform_hash(platform=platform,
                            direction=direction)
    to_hashes.append(to_hash)

    return sequences_done


def solve(*,
          step: int):
    print('*' * 20, f"Step {step}")

    rocks: list[list[str]] = []
    with (open('input.txt', 'r') as input_file):

        for index_line, line in enumerate(input_file.read().splitlines()):
            rocks.append(list(line))

    platform = array(rocks)

    iter_axis_rows, iter_axis_columns = shape(platform)

    hashes_n: list[str] = []
    hashes_n_to: list[str] = []
    hashes_s: list[str] = []
    hashes_s_to: list[str] = []
    hashes_w: list[str] = []
    hashes_w_to: list[str] = []
    hashes_e: list[str] = []
    hashes_e_to: list[str] = []

    def do_x_tilt_sequences(*,
                            sequences_done: int,
                            sequences_do: int) -> int:
        if print_progress[step - 1]:
            print(f"Done {sequences_done} tilt sequences,"
                  f" do {sequences_do} more. {tilt_line.cache_info()}")

        for sequence_do in range(sequences_do):
            sequences_done = tilt_platform_or_use_hash(
                    step=step,
                    platform=platform,
                    iter_axis_rows=iter_axis_rows,
                    iter_axis_columns=iter_axis_columns,
                    direction='N',
                    from_hashes=hashes_n,
                    to_hashes=hashes_n_to,
                    sequences_done=sequences_done,
                    limit=limit)

            if sequences_done == limit:
                break

            sequences_done = tilt_platform_or_use_hash(
                    step=step,
                    platform=platform,
                    iter_axis_rows=iter_axis_rows,
                    iter_axis_columns=iter_axis_columns,
                    direction='W',
                    from_hashes=hashes_w,
                    to_hashes=hashes_w_to,
                    sequences_done=sequences_done,
                    limit=limit)

            sequences_done = tilt_platform_or_use_hash(
                    step=step,
                    platform=platform,
                    iter_axis_rows=iter_axis_rows,
                    iter_axis_columns=iter_axis_columns,
                    direction='S',
                    from_hashes=hashes_s,
                    to_hashes=hashes_s_to,
                    sequences_done=sequences_done,
                    limit=limit)

            sequences_done = tilt_platform_or_use_hash(
                    step=step,
                    platform=platform,
                    iter_axis_rows=iter_axis_rows,
                    iter_axis_columns=iter_axis_columns,
                    direction='E',
                    from_hashes=hashes_e,
                    to_hashes=hashes_e_to,
                    sequences_done=sequences_done,
                    limit=limit)

            sequences_done += 1

        return sequences_done

    if step == 1:
        tilt_platform(step=step,
                      platform=platform,
                      iter_axis_rows=iter_axis_rows,
                      iter_axis_columns=iter_axis_columns,
                      direction='N')
    else:
        index_tilt = 0
        limit = 1000000000
        while index_tilt < limit:
            index_tilt = do_x_tilt_sequences(sequences_done=index_tilt,
                                             sequences_do=10000)
            assert index_tilt > 0
            assert (index_tilt % 10000) == 0
        assert index_tilt == limit

    if print_progress[step - 1]:
        print()
        print('\n'.join(''.join(row) for row in platform))

    result = sum(sum(1 if rock == 'O' else 0
                     for rock in line) * (index + 1)
                 for index, line in enumerate(flip(platform)))

    print('*' * 20, f"Step {step}", result)


if __name__ == '__main__':
    solve(step=1)
    solve(step=2)

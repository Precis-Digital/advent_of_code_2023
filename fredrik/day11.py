import itertools

from shared import utils


def main() -> None:
    image_lines = utils.read_input_to_string().splitlines()
    galaxies = []
    for y, row in enumerate(image_lines):
        for x, char in enumerate(row):
            if char == "#":
                galaxies.append((x, y))

    width = len(image_lines[0])
    height = len(image_lines)

    galaxy_columns = {galaxy[0] for galaxy in galaxies}
    galaxy_rows = {galaxy[1] for galaxy in galaxies}

    galaxy_free_columns = {col for col in range(width)} - galaxy_columns
    galaxy_free_rows = {row for row in range(height)} - galaxy_rows

    total_distance = expansions = 0
    for galaxy1, galaxy2 in itertools.combinations(galaxies, r=2):
        for col in galaxy_free_columns:
            if galaxy1[0] > col > galaxy2[0] or galaxy2[0] > col > galaxy1[0]:
                expansions += 1

        for row in galaxy_free_rows:
            if galaxy1[1] > row > galaxy2[1] or galaxy2[1] > row > galaxy1[1]:
                expansions += 1

        total_distance += abs(galaxy1[0] - galaxy2[0]) + abs(galaxy1[1] - galaxy2[1])

    print(f"Part 1: {total_distance + expansions}")
    print(f"Part 2: {total_distance + expansions*(1_000_000-1)}")


if __name__ == "__main__":
    main()

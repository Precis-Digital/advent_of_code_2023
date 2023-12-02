def open_file(file_name):
    with open(file_name, "r") as f:
        return f.read().splitlines()


def extract_values_from_row(row):
    game_num = row.split(":")[0].replace("Game ", "")

    max_green = 0
    max_blue = 0
    max_red = 0

    for drawings in row.split(":")[1].split(";"):
        for drawing in drawings.split(","):
            count, color = drawing.strip().split(" ")
            if color == "red":
                max_red = int(count) if int(count) > max_red else max_red
            elif color == "blue":
                max_blue = int(count) if int(count) > max_blue else max_blue
            elif color == "green":
                max_green = int(count) if int(count) > max_green else max_green

    return {
        "game_num": game_num,
        "max_green": max_green,
        "max_blue": max_blue,
        "max_red": max_red,
    }


def task_one(sample=False):
    if sample:
        lines = open_file("Sample.txt")
    else:
        lines = open_file("Input.txt")

    RED_COUNT = 12
    GREEN_COUNT = 13
    BLUE_COUNT = 14

    summed_game_nums = 0
    for line in lines:
        parsed_row = extract_values_from_row(line)
        if (
            parsed_row["max_red"] <= RED_COUNT
            and parsed_row["max_green"] <= GREEN_COUNT
            and parsed_row["max_blue"] <= BLUE_COUNT
        ):
            summed_game_nums += int(parsed_row["game_num"])

    print(f"Task One Solution: {summed_game_nums} ({sample=})")


def task_two(sample=False):
    if sample:
        lines = open_file("Sample.txt")
    else:
        lines = open_file("Input.txt")

    summed_min_powers = 0
    for line in lines:
        parsed_row = extract_values_from_row(line)

        summed_min_powers += (
            parsed_row["max_red"] * parsed_row["max_green"] * parsed_row["max_blue"]
        )

    print(f"Task Two Solution: {summed_min_powers} ({sample=})")


task_one(sample=True)
task_one()

task_two(sample=True)
task_two()

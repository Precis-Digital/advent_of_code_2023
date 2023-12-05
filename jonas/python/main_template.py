import time


def open_file(file_name):
    with open(file_name, "r") as f:
        return f.read().splitlines()


def task_one(sample=False):
    start = time.time()
    if sample:
        lines = open_file("Sample.txt")
    else:
        lines = open_file("Input.txt")

    answer = len(lines)

    print(
        f"Task Two - {round((time.time() - start) * 1000, 2)}ms - Solution: {answer}"
        + (" (sample)" if sample else "")
    )


def task_two(sample=False):
    start = time.time()
    if sample:
        lines = open_file("Sample.txt")
    else:
        lines = open_file("Input.txt")

    answer = len(lines)

    print(
        f"Task Two - {round((time.time() - start) * 1000, 2)}ms - Solution: {answer}"
        + (" (sample)" if sample else "")
    )


task_one(sample=True)
task_one()

task_two(sample=True)
task_two()

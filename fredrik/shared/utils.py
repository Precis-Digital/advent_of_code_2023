import inspect


def read_input_to_string() -> str:
    day = inspect.stack()[1].filename.split("/")[-1].split(".")[0]
    with open(f"inputs/{day}.txt", "r") as file:
        return file.read()

from time import perf_counter


def performance(func):
    def wrapper_function(*args, **kwargs):
        tic = perf_counter()
        result = func(*args,  **kwargs)
        toc = perf_counter()
        print(f"Executed in {toc - tic:0.4f} seconds")
        return result
    return wrapper_function

import time


def time_me(func):
    def callable(*args):
        start = time.time()
        out = func(*args)
        end = time.time()
        print(end - start)
        return out

    return callable

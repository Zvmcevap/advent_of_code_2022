from utils.stop_watch import time_me


def get_input():
    with open("day_6.txt") as f:
        return f.readline().strip()


@time_me
def problem_solver(how_many_uniques: int):
    dsb = get_input()
    for i in range(len(dsb) - (how_many_uniques - 1)):
        uniques = set(dsb[i: i + how_many_uniques])
        if len(uniques) == how_many_uniques:
            return i + how_many_uniques


if __name__ == "__main__":
    print(problem_solver(4))
    print(problem_solver(14))

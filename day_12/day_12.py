from utils.stop_watch import time_me
from pathfinder import Pathfinder


@time_me
def where_where_they_going_without_ever_knowing_the_way():
    pathfinder = Pathfinder()

    victory_part_one = len(pathfinder.a_star())
    pathfinder.print_map()

    victory_part_two = len(pathfinder.djikstra())
    pathfinder.print_map()

    return victory_part_one, victory_part_two


if __name__ == "__main__":
    solution_one, solution_two = where_where_they_going_without_ever_knowing_the_way()
    print(f"SOLUTION PART ONE = {solution_one}")
    print(f"SOLUTION PART TWO = {solution_two}")

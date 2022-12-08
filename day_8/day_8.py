from utils.stop_watch import time_me
import numpy as np


def get_forrest():
    with open("day_8.txt") as f:
        return [[int(tree) for tree in line.strip()] for line in f.readlines()]


@time_me
def see_the_forest_for_the_trees():
    forest = np.array(get_forrest())
    visible_trees = 2 * len(forest) + 2 * (len(forest[0]) - 2)
    maximum_scenic_score = 0
    for row in range(1, len(forest) - 1):
        for column in range(1, len(forest[0]) - 1):
            tree = forest[row, column]

            # List of trees to the left, right, top and bottom
            left = forest[row, :column]
            right = forest[row, column + 1:]
            top = forest[:row, column]
            bot = forest[row + 1:, column]

            # Part One - Check all directions if all trees are smaller
            if np.all(left < tree) or np.all(right < tree) or np.all(top < tree) or np.all(bot < tree):
                visible_trees += 1

            # Part Two - Search all directions i steps from tree
            search_left, search_right, search_top, search_bot = True, True, True, True
            vis_left, vis_right, vis_top, vis_bot = 0, 0, 0, 0
            i = 0
            while search_left or search_right or search_top or search_bot:
                # Check if edge
                if len(left) - i <= 0:
                    search_left = False
                if i >= len(right):
                    search_right = False
                if len(top) - i <= 0:
                    search_top = False
                if i >= len(bot):
                    search_bot = False
                # Increase if not edge or was bigger step before
                vis_left += 1 if search_left else 0
                vis_right += 1 if search_right else 0
                vis_top += 1 if search_top else 0
                vis_bot += 1 if search_bot else 0
                # Check if tree bigger or equal to tree
                if search_left and tree <= left[len(left) - i - 1]:
                    search_left = False
                if search_right and tree <= right[i]:
                    search_right = False
                if search_top and tree <= top[len(top) - i - 1]:
                    search_top = False
                if search_bot and tree <= bot[i]:
                    search_bot = False
                i += 1

            scenic_score = vis_left * vis_right * vis_top * vis_bot
            if scenic_score > maximum_scenic_score:
                maximum_scenic_score = scenic_score

    return visible_trees, maximum_scenic_score


if __name__ == "__main__":
    solution_part_one, solution_part_two = see_the_forest_for_the_trees()
    print(f"Solution for part one is {solution_part_one}.")
    print(f"Solution for part two is {solution_part_two}.")

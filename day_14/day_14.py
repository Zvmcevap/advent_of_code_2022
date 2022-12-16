from typing import Optional
from PIL import Image

from utils.stop_watch import time_me
import matplotlib.pyplot as plt
import numpy as np


# With plotting it takes 3258.933945417404 seconds without plotting 1.1972358226776123


def get_cave_coordinates():
    with open("day_14.txt") as f:
        structure = []
        for line in f.readlines():
            struct_lines = (line.strip().split(" -> "))
            sl = []
            for coords in struct_lines:
                coords = [int(coords.split(",")[0]), int(coords.split(",")[1])]
                sl.append(coords)
            structure.append(sl)
        exes = []
        eyes = []
        x_und_y = []
        for struct in structure:
            for i in range(len(struct) - 1):
                x = struct[i][0]
                y = struct[i][1]
                xy = [x, y]
                if i < 1:
                    exes.append(x)
                    eyes.append(y)
                    x_und_y.append(xy)
                while x != struct[i + 1][0] or y != struct[i + 1][1]:
                    x += 1 if x < struct[i + 1][0] else -1 if x > struct[i + 1][0] else 0
                    y += 1 if y < struct[i + 1][1] else -1 if y > struct[i + 1][1] else 0
                    xy = [x, y]
                    exes.append(x)
                    eyes.append(y)
                    x_und_y.append(xy)

        return exes, eyes, x_und_y


class Sandcastle:
    def __init__(self):
        self.cave = np.array([])
        self.cave_part_two = np.array([])
        self.sand = []
        self.sand_part_two = []

    def create_cave_system(self, xy, exes, eyes):
        cave = []
        for m in range(max(eyes) + 1):
            column = []
            for n in range(min(exes), max(exes) + 1):
                if [n, m] in xy:
                    column.append(1)
                elif m == 0 and n == 500:
                    self.sand = [0, 500 - min(exes)]
                    column.append(3)
                else:
                    column.append(0)
            cave.append(column)
        self.cave = np.array(cave)

    def create_cave_system_part_two(self):
        self.cave_part_two = np.copy(self.cave)

        bottom_width = 1 + 2 * (len(self.cave_part_two) + 2)
        left_missing = int(bottom_width / 2) + 1 - self.sand[1]
        right_missing = int(bottom_width / 2) + 1 - (len(self.cave_part_two[0]) - self.sand[1])
        self.sand_part_two = [0, self.sand[1] + left_missing]

        left_array = np.zeros((len(self.cave_part_two), left_missing), dtype="int32")
        right_array = np.zeros((len(self.cave_part_two), right_missing), dtype="int32")
        self.cave_part_two = np.concatenate((left_array, self.cave_part_two, right_array), axis=1)

        bottom_air = np.zeros(bottom_width + 1, dtype="int32")
        bottom_floor = np.ones(bottom_width + 1, dtype="int32")
        self.cave_part_two = np.append(self.cave_part_two, [bottom_air, bottom_floor], axis=0)

    def find_bottom(self, row: int, column: int, cave):
        drops = []
        for i in range(row + 1, len(cave[:, column])):
            drops.append((i, column))
            if 3 > cave[i, column] > 0:
                return drops

    def check_left(self, row, column, cave) -> Optional[bool]:
        if column == 0:
            return None
        if cave[row, column - 1] > 0:
            return False
        return True

    def check_right(self, row, column, cave) -> Optional[bool]:
        if column + 1 == len(cave[0]):
            return None
        if cave[row, column + 1] > 0:
            return False
        return True

    def build_sandcastle(self, part_one=True, start_row=None, start_column=None, p=0):
        cave = self.cave if part_one else self.cave_part_two
        if not start_row or not start_column:
            start_row = self.sand[0]
            start_column = self.sand[1] if part_one else self.sand_part_two[1]

        drops = self.find_bottom(row=start_row, column=start_column, cave=cave)
        while len(drops) > 0:
            row = drops[-1][0]
            column = drops[-1][1]

            if cave[row, column] < 1:
                p = self.build_sandcastle(part_one=part_one, start_row=row, start_column=column, p=p)
                if not p:
                    return False
            left = self.check_left(row=row, column=column, cave=cave)
            right = self.check_right(row=row, column=column, cave=cave)
            if left:
                # sand_places.append((row, column))
                drops.append((row + 1, column - 1))
            elif right:
                # sand_places.append((row, column))
                drops.append((row + 1, column + 1))
            else:
                if left is None or right is None:
                    print("Falling out of bounds")
                    return False
                if cave[row - 1, column] == 3:
                    print("Blocked top")
                    cave[row - 1, column] = 2
                    p += 1
                    self.plot_cave(p, part_one)
                    return False
                cave[row - 1, column] = 2
                drops.pop()
                p += 1
                # self.plot_cave(p, part_one)
        return p

    def print_cave(self):
        print(self.cave)

    def plot_cave(self, i: int, part_one: bool):
        # plot !
        plt.rcParams["figure.figsize"] = [10.50, 6.0]
        plt.rcParams["figure.autolayout"] = True
        if part_one:
            plt.imshow(self.cave)
            folder_name = "plot_part_one"
        else:
            folder_name = "plot_part_two"
            plt.imshow(self.cave_part_two)
        plt.savefig(f"./{folder_name}/{i}.png")
        plt.close()


@time_me
def must_be_the_reason_than_Im_king_of():
    exes, eyes, xy = get_cave_coordinates()

    my_sandcastle = Sandcastle()
    my_sandcastle.create_cave_system(xy=xy, exes=exes, eyes=eyes)
    my_sandcastle.build_sandcastle(part_one=True)
    my_sandcastle.create_cave_system_part_two()
    my_sandcastle.build_sandcastle(part_one=False)
    units_of_sand = np.count_nonzero(my_sandcastle.cave == 2)
    units_of_sand_part_two = np.count_nonzero(my_sandcastle.cave_part_two == 2)

    return units_of_sand, units_of_sand_part_two


def make_gif():
    frames = []
    for i in range(0, 22915, 38):
        if i > 0:
            frames.append(Image.open(f"plot_part_two/{i}.png"))
    frame_one = Image.open("plot_part_two/1.png")
    frame_one.save("finished_part_two.gif", format="GIF", append_images=frames, save_all=True, durration=1, loop=0)


if __name__ == "__main__":
    solution_one, solution_two = must_be_the_reason_than_Im_king_of()
    print(f"Solution one = {solution_one}, Solution two = {solution_two}")
    # make_gif()

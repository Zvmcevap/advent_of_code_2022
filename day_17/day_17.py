import math

from matplotlib import pyplot as plt
from utils.stop_watch import time_me
import numpy as np


def get_jet(filename):
    with open(filename) as f:
        jet_list = []
        for letter in f.readline():
            jet = -1 if letter == "<" else 1
            jet_list.append(jet)
        return jet_list


class Cave:
    def __init__(self):
        self.cave = np.ones((1, 7))

    def add_roof(self, amount):
        if amount > 0:
            self.cave = np.concatenate((np.zeros((amount, 7)), self.cave), axis=0)

    def plot_cave(self, picname):
        # plot !
        plt.imshow(self.cave)
        plt.rcParams["figure.figsize"] = [10.50, 6.0]
        plt.rcParams["figure.autolayout"] = True
        plt.savefig(f"./plots/{picname}.png")
        plt.close()


class Minus:
    def __init__(self):
        self.y = 0
        self.x = 2  # Left most square
        self.add_roof = 1

    def check_x_axis(self, cave, amount: int):
        if amount > 0:
            if self.x + 4 < len(cave[0]) and cave[self.y, self.x + 4] == 0:
                self.x += amount
                return True
        if amount < 0:
            if self.x > 0 and cave[self.y, self.x - 1] == 0:
                self.x += amount
                return True
        return False

    def check_down(self, cave):
        ones_bellow = np.count_nonzero(cave[self.y + 1, self.x: self.x + 4])
        if ones_bellow == 0:
            self.y += 1
            return None
        else:
            cave[self.y, self.x: self.x + 4] = 1
            return self.y


class Stick:
    def __init__(self):
        self.y = 0
        self.x = 2
        self.add_roof = 4

    def recenter(self, y):
        self.y = y

    def check_x_axis(self, cave, amount: int):
        if amount < 0 < self.x:
            if np.count_nonzero(cave[self.y:self.y + 4, self.x + amount]) == 0:
                self.x += amount
                return True
        if amount > 0 and self.x + 1 < len(cave[0]):
            if np.count_nonzero(cave[self.y:self.y + 4, self.x + amount]) == 0:
                self.x += amount
                return True
        return False

    def check_down(self, cave):
        if cave[self.y + 4, self.x] == 0:
            self.y += 1
            return None
        else:
            cave[self.y: self.y + 4, self.x] = 1
            return self.y


class Elle:
    def __init__(self):
        self.x = 4
        self.y = 2
        self.add_roof = 3

    def check_x_axis(self, cave, amount: int):
        if amount < 0 < self.x - 2 and cave[self.y, self.x - 3] == 0:
            if np.count_nonzero(cave[self.y - 2: self.y - 1, self.x + amount]) == 0:
                # self.undraw(cave=cave)
                self.x += amount
                # self.draw(cave=cave)
                return True
        if amount > 0 and self.x + 1 < len(cave[0]):
            if np.count_nonzero(cave[self.y - 2:self.y + 1, self.x + 1]) == 0:
                # self.undraw(cave=cave)
                self.x += amount
                # self.draw(cave=cave)
                return True
        return False

    def check_down(self, cave):
        if np.count_nonzero(cave[self.y + 1, self.x - 2: self.x + 1]) == 0:
            # self.undraw(cave=cave)
            self.y += 1
            # self.draw(cave=cave)
            return None
        else:
            cave[self.y, self.x - 2:self.x] = 1
            cave[self.y - 2: self.y + 1, self.x] = 1
            return self.y - 2

    def draw(self, cave):
        cave[self.y, self.x - 2:self.x] = 1
        cave[self.y - 2: self.y + 1, self.x] = 1

    def undraw(self, cave):
        cave[self.y, self.x - 2:self.x] = 0
        cave[self.y - 2: self.y + 1, self.x] = 0


class Square:
    def __init__(self):
        self.x = 2
        self.y = 0
        self.add_roof = 2

    def recenter(self, y):
        self.y = y

    def check_x_axis(self, cave, amount: int):
        if amount < 0 < self.x:
            if np.count_nonzero(cave[self.y: self.y + 2, self.x + amount]) == 0:
                self.x += amount
                return True
        if amount > 0 and self.x + 2 < len(cave[0]):
            if np.count_nonzero(cave[self.y:self.y + 2, self.x + 1 + amount]) == 0:
                self.x += amount
                return True
        return False

    def check_down(self, cave):
        if np.count_nonzero(cave[self.y + 2, self.x: self.x + 2]) == 0:
            self.y += 1
            return None
        else:
            cave[self.y: self.y + 2, self.x:self.x + 2] = 1
            return self.y


class Plus:
    def __init__(self):
        self.x = 3
        self.y = 1
        self.add_roof = 3

    def check_x_axis(self, cave, amount: int):
        if amount < 0 < self.x - 1 and cave[self.y, self.x - 2] == 0:
            if cave[self.y + 1, self.x - 1] == cave[self.y - 1, self.x - 1] == 0:
                # self.undraw(cave=cave)
                self.x += amount
                # self.draw(cave=cave)
                return True
        if amount > 0 and self.x + 2 < len(cave[0]) and cave[self.y, self.x + 2] == 0:
            if cave[self.y + 1, self.x + 1] == cave[self.y - 1, self.x + 1] == 0:
                # self.undraw(cave=cave)
                self.x += amount
                # self.draw(cave=cave)
                return True
        return False

    def recenter(self, y):
        self.y = y + 1

    def check_down(self, cave):
        # self.undraw(cave=cave)
        if cave[self.y + 2, self.x] == cave[self.y + 1, self.x + 1] == cave[self.y + 1, self.x - 1] == 0:
            self.y += 1
            # self.draw(cave=cave)
            return None
        else:
            cave[self.y - 1: self.y + 2, self.x] = 1
            cave[self.y, self.x - 1:self.x + 2] = 1
            return self.y - 1

    def draw(self, cave):
        cave[self.y - 1: self.y + 2, self.x] = 1
        cave[self.y, self.x - 1:self.x + 2] = 1

    def undraw(self, cave):
        cave[self.y - 1: self.y + 2, self.x] = 0
        cave[self.y, self.x - 1:self.x + 2] = 0


class ShapeAnalizer:
    def __init__(self, shape_name):
        # Data incoming from doing tetris
        self.shape_numbers = []
        self.command_numbers = []
        self.tower_increase = []
        # Data analyzed for patterns
        self.first_repeated_command = 0
        self.repetition_length = 0
        self.sum_of_repeat = 0
        self.sum_before_repeats = 0
        # These are just for fun (aka, thought I needed them)
        self.name = shape_name
        self.first_repeated_shape = 0
        self.repetition_length_shapes = 0

    def super_duper_analyzer_3000(self):
        cmds_per_index = []
        self.command_numbers = np.array(self.command_numbers)
        self.shape_numbers = np.array(self.shape_numbers)
        self.tower_increase = np.array(self.tower_increase)

        if len(self.tower_increase) != len(self.shape_numbers) != len(self.command_numbers):
            raise Exception("Different Amounts of Datas, ABORT!")
        added = []
        for command in self.command_numbers:
            if command not in added:
                added.append(command)
                repeats = np.where(self.command_numbers == command)
                if len(repeats[0]) > 3:
                    cmds_per_index.append([repeats[0][0], repeats[0][1], repeats[0][2], repeats[0][3]])

        if len(cmds_per_index) == 0:
            raise Exception("NOT ENOUGH REPEATS, WANT, NO.., NEED 4 TOWERS OF DATA")

        cmds_per_index = np.array(cmds_per_index)
        for command in cmds_per_index:
            # Increases per what-you-call-it
            first_sum = sum(self.tower_increase[command[0]:command[1]])
            second_sum = sum(self.tower_increase[command[1]:command[2]])
            third_sum = sum(self.tower_increase[command[2]:command[3]])

            # Difference in shape separation
            first_shape_diff = self.shape_numbers[command[1]] - self.shape_numbers[command[0]]
            second_shape_diff = self.shape_numbers[command[2]] - self.shape_numbers[command[1]]
            third_shape_diff = self.shape_numbers[command[3]] - self.shape_numbers[command[2]]

            # Analysis complete, save data in class variables
            if first_sum == second_sum == third_sum and first_shape_diff == second_shape_diff == third_shape_diff:
                self.first_repeated_command = command[0]
                self.sum_of_repeat = first_sum
                self.repetition_length_shapes = first_shape_diff
                self.repetition_length = command[1] - command[0]
                self.first_repeated_shape = self.shape_numbers[command[0]]
                self.sum_before_repeats = sum(self.tower_increase[:command[0]])
                break

    def __str__(self):
        return f"Shape: {self.name} " \
               f"\nFirst repeated shape: {self.first_repeated_shape}; repeat length: {self.repetition_length}" \
               f"\nsum before repeat: {self.sum_before_repeats}; sum of repeat {self.sum_of_repeat}" \
               f"\n-----"


def do_tetris(how_many_times, second_part=False, test=False):
    test = test
    filename = "test.txt" if test else "day_17.txt"
    jet = get_jet(filename)
    cave = Cave()

    i = 0
    part_two_search = {0: ShapeAnalizer("Minus"),
                       1: ShapeAnalizer("Plus"),
                       2: ShapeAnalizer("Elle"),
                       3: ShapeAnalizer("Stick"),
                       4: ShapeAnalizer("Square")
                       }  # part two
    for t in range(0, how_many_times):
        # print(f"current = {t} - percent = {t/2022}")
        tetra_mod = t % 5
        if tetra_mod == 0:
            tetromina = Minus()
        elif tetra_mod == 1:
            tetromina = Plus()
        elif tetra_mod == 2:
            tetromina = Elle()
        elif tetra_mod == 3:
            tetromina = Stick()
        else:
            tetromina = Square()

        roof_addition = tetromina.add_roof + 3
        previous_roof = len(cave.cave) - 1
        cave.add_roof(amount=roof_addition)

        if second_part:
            part_two_search[tetra_mod].shape_numbers.append(t)  # part two
            part_two_search[tetra_mod].command_numbers.append(i)  # also part two

        while True:
            tetromina.check_x_axis(amount=jet[i], cave=cave.cave)
            i = (i + 1) % len(jet)
            stopped_at_y = tetromina.check_down(cave=cave.cave)
            if stopped_at_y:
                # cave.plot_cave(t)
                cropp_y = stopped_at_y if stopped_at_y < roof_addition else roof_addition
                cave.cave = cave.cave[cropp_y:, :]
                part_two_search[tetra_mod].tower_increase.append(len(cave.cave) - 1 - previous_roof)  # part two
                break

    return len(cave.cave) - 1 if not second_part else part_two_search


def herkul_poirot():
    test = False
    big_ass_number = 1000000000000
    big_ass_solution = 1514285714288  # Testing basic solution

    # Do a bunch of times to find patterns for the super-duper analyzer
    shapes = do_tetris(5 * 2000, second_part=True, test=test)

    # Do the analysis // very scientific
    for id_number in shapes:
        shapes[id_number].super_duper_analyzer_3000()

    # 5 shapes 5 numbers
    fifth = big_ass_number // 5

    repeats_summation = 0
    constant_summation = 0
    remainder_summation = 0

    for id_number in shapes:
        shape = shapes[id_number]
        frc = shape.first_repeated_command
        divisor = (fifth - frc) // shape.repetition_length
        remainder = (fifth - frc) % shape.repetition_length

        constant_summation += shape.sum_before_repeats
        repeats_summation += shape.sum_of_repeat * divisor
        remainder_summation += sum(shape.tower_increase[frc: frc + remainder])

    solution = repeats_summation + constant_summation + remainder_summation
    # Test the solution
    if test:
        print(f"Test case works: {solution == big_ass_solution}")
    return solution


if __name__ == "__main__":
    solution_one = do_tetris(how_many_times=2022)
    print(f"Part uno = {solution_one}")

    solution_two = herkul_poirot()
    print(f"Part due = {solution_two}")

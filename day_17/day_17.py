from matplotlib import pyplot as plt
from typing import List
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
        self.cave = np.concatenate(
            (np.concatenate((np.ones((4, 1)), np.zeros((4, 7)), np.ones((4, 1))), axis=1), np.ones((1, 9))), axis=0)

    def plot_cave(self, picname):
        # plot !
        plt.imshow(self.cave)
        plt.rcParams["figure.figsize"] = [10.50, 6.0]
        plt.rcParams["figure.autolayout"] = True
        plt.savefig(f"./plots/{picname}.png")
        plt.close()


class Minus:
    def __init__(self, left: List[int]):
        self.squares = [[left[0], left[0] + i] for i in range(1, 5)]
        self.left = self.squares[0]
        self.right = self.squares[-1]

    def check_x_axis(self, cave, amount: int):
        amount = amount
        left = True if amount > 0 else False
        index = 0 if left else -1
        if cave[self.squares[0][0], self.squares[index][1] + amount] == 1:
            return False
        cave[self.squares[0][0], self.squares[0][1]: self.squares[-1][1]] = 0
        print(self.squares)
        self.move_x_axis(amount)
        cave[self.squares[0][0], self.squares[0][1]: self.squares[-1][1]] = 1
        print(self.squares)
        return True

    def move_x_axis(self, amount):
        for square in self.squares:
            square[1] += amount


    def check_down(self, cave):
        non_zeroes = np.count_nonzero(cave[self.squares[0][0] + 1, self.squares[0][1]: self.squares[0][-1]])
        print(non_zeroes)
        if non_zeroes == 0:
            return False
        cave[self.squares[0][0], self.squares[0][1]: self.squares[-1][1]] = 0
        for square in self.squares:
            square[0] += 1
        cave[self.squares[0][0], self.squares[0][1]: self.squares[-1][1]] = 1




def part_one():
    test = False
    filename = "test.txt" if test else "day_17.txt"
    jet = get_jet(filename)
    cave = Cave()
    cave.plot_cave(str(0))

    minus = Minus([0, 2])
    for i in range(1, 5):
        if minus.check_x_axis(amount=jet[i], cave=cave.cave):
            print(f"Successful move {jet[i]}")
        else:
            print(f"Failed move {jet[i]}")
        if minus.check_down(cave=cave.cave):
            print("Successful move down")
        else:
            print("Unsuccessful move down")
        cave.plot_cave(i)


if __name__ == "__main__":
    part_one()

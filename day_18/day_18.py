import numpy as np
import matplotlib.pyplot as plt

from utils.stop_watch import time_me
import re
from operator import attrgetter


def get_drops(filename):
    with open(filename) as f:
        drops = []
        for line in f.readlines():
            drop = [int(i) for i in line.strip().split(",")]
            drops.append(drop)
        return drops


class Droplet:
    def __init__(self, coords):
        self.x = coords[0] + 1
        self.y = coords[1] + 1
        self.z = coords[2] + 1

        self.sides = 6

    def barf_out_zeros(self, matrix):
        #print(matrix[self.x - 1:self.x + 2, self.y - 1: self.y + 2, self.z - 1:self.z + 2])
        non_zero_x = np.count_nonzero(matrix[self.x - 1:self.x + 2, self.y, self.z])
        non_zero_y = np.count_nonzero(matrix[self.x, self.y - 1: self.y + 2, self.z])
        non_zero_z = np.count_nonzero(matrix[self.x, self.y, self.z - 1:self.z + 2])
        #print(non_zero_x, non_zero_y, non_zero_z)
        return non_zero_x + non_zero_y + non_zero_z

    def __str__(self):
        return f"[{self.x}, {self.y}, {self.z}]"


@time_me
def part_one():
    test = False
    filename = "test.txt" if test else "day_18.txt"
    data = get_drops(filename)

    droplets = []
    for d in data:
        drop = Droplet(coords=d)
        droplets.append(drop)

    droplets.sort(key=attrgetter("x"))
    maximum_x = max([drop.x for drop in droplets])
    maximum_y = max([drop.y for drop in droplets])
    maximum_z = max([drop.z for drop in droplets])

    print("Matrix, size")
    print(maximum_x, maximum_y, maximum_z)
    droplet_matrix = np.ones((maximum_x + 2, maximum_y + 2, maximum_z + 2))

    for drop in droplets:
        droplet_matrix[drop.x, drop.y, drop.z] = 0

    sides = 0
    i = 1
    for drop in droplets:
        print(f"i = {i}")
        sides += drop.barf_out_zeros(matrix=droplet_matrix)
        i += 1

    for i, m in enumerate(droplet_matrix):
        plt.imshow(m)
        plt.savefig(f"./cave/{i}.png")
        plt.close()
    return sides


if __name__ == "__main__":
    solution_part_one = part_one()
    print(f"Solution part one = {part_one()}")

from typing import List
from copy import deepcopy
from utils.stop_watch import time_me
import json


class Packet:
    def __init__(self, container):
        self.container = container

    def __lt__(self, other):
        return self.check_order(deepcopy(self.container), deepcopy(other.container))

    def check_order(self, left: List, right: List):
        for i in range(max(len(left), len(right))):
            if i == len(left):
                return True
            if i == len(right):
                return False

            if type(left[i]) == int and type(right[i]) == int:
                if left[i] != right[i]:
                    return left[i] < right[i]
            else:
                if type(left[i]) == list and type(right[i]) == int:
                    right[i] = [right[i]]
                elif type(left[i]) == int and type(right[i]) == list:
                    left[i] = [left[i]]
                if self.check_order(left[i], right[i]) is not None:
                    return self.check_order(left[i], right[i])


class Sorter:
    def __init__(self):
        self.original_packets: List[Packet] = get_packets()
        self.first_divider = Packet([[2]])
        self.second_divider = Packet([[6]])
        self.packets = self.original_packets.copy()
        self.packets.append(self.first_divider)
        self.packets.append(self.second_divider)
        self.check_order = self.second_divider.check_order

    def get_solution_one(self):
        properly_sorted_indexes = 0
        for i in range(0, len(self.original_packets) - 1, 2):
            if self.check_order(self.original_packets[i].container, self.original_packets[i + 1].container):
                properly_sorted_indexes += (int(i / 2 + 1))
        return properly_sorted_indexes

    def get_solution_two(self):
        self.packets.sort()
        return (self.packets.index(self.first_divider) + 1) * (self.packets.index(self.second_divider) + 1)


def get_packets():
    with open("day_13.txt") as f:
        packets = []
        for line in f.readlines():
            if line.strip() != "":
                packet = Packet(container=json.loads(line))
                packets.append(packet)
        return packets


@time_me
def very_solution():
    sorter = Sorter()
    return sorter.get_solution_one(), sorter.get_solution_two()


if __name__ == "__main__":
    solution_one, solution_two = very_solution()
    print(f"Solution part one = {solution_one}; Solution part two = {solution_two}")

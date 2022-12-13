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

    def get_solution_part_one(self):
        properly_sorted_indexes = []
        for i in range(0, len(self.original_packets) - 1, 2):
            left = self.original_packets[i].container
            right = self.original_packets[i + 1].container
            if self.check_order(left, right):
                properly_sorted_indexes.append(int(i / 2 + 1))
        return sum(properly_sorted_indexes)

    # Sorting algorithms retrieved from Uvod v Algoritme, FIŠ University to test them out
    @time_me
    def selection_sort(self):
        sbe = self.packets.copy()
        i = 0
        while i < len(sbe) - 1:
            index_min = i
            j = i + 1
            while j < len(sbe):
                if not self.check_order(deepcopy(sbe[index_min].container), deepcopy(sbe[j].container)):
                    index_min = j
                j = j + 1
            sbe[i], sbe[index_min] = sbe[index_min], sbe[i]
            i += 1
        fd_index = 0
        sd_index = 0
        for i, pack in enumerate(sbe):
            if pack == self.first_divider:
                fd_index = i + 1
            if pack == self.second_divider:
                sd_index = i + 1
        print("---------------------------------")
        print("selection")
        return fd_index * sd_index

    @time_me
    def insertion_sort(self):
        sbi = self.packets.copy()
        i = 1
        while i < len(sbi):
            testy_packet = sbi[i]
            j = i - 1
            while j >= 0 and self.check_order(deepcopy(testy_packet.container), deepcopy(sbi[j].container)):
                sbi[j + 1] = sbi[j]
                j -= 1
            sbi[j + 1] = testy_packet
            i += 1

        fd_index = 0
        sd_index = 0
        for i, pack in enumerate(sbi):
            if pack == self.first_divider:
                fd_index = i + 1
            if pack == self.second_divider:
                sd_index = i + 1
        print("---------------------------------")
        print("insertion")
        return fd_index * sd_index

    @time_me
    def bubble_sort(self):
        dbb = self.packets.copy()
        trade = True
        number_of_unsorted = len(dbb)

        while trade:
            trade = False
            i = 0
            while i < number_of_unsorted - 1:
                if not self.check_order(deepcopy(dbb[i].container), deepcopy(dbb[i + 1].container)):
                    dbb[i], dbb[i + 1] = dbb[i + 1], dbb[i]
                    trade = True
                i += 1
            number_of_unsorted -= 1

        fd_index = 0
        sd_index = 0
        for i, pack in enumerate(dbb):
            if pack == self.first_divider:
                fd_index = i + 1
            if pack == self.second_divider:
                sd_index = i + 1
        print("---------------------------------")
        print("bubble")
        return fd_index * sd_index

    # Merge needs 2
    @time_me
    def merge_sort(self):
        sorted_by_merge = self.packets.copy()
        self.merge_sort_algo(sorted_by_merge)

        fd_index = 0
        sd_index = 0
        for i, pack in enumerate(sorted_by_merge):
            if pack == self.first_divider:
                fd_index = i + 1
            if pack == self.second_divider:
                sd_index = i + 1
        print("---------------------------------")
        print("merge")
        return fd_index * sd_index

    def merge_sort_algo(self, packets: List[Packet]):
        if len(packets) > 1:
            middle_index = len(packets) // 2
            left = packets[:middle_index]
            right = packets[middle_index:]

            self.merge_sort_algo(left)
            self.merge_sort_algo(right)

            i = j = k = 0

            while i < len(left) and j < len(right):
                if self.check_order(deepcopy(left[i].container), deepcopy(right[j].container)):
                    packets[k] = left[i]
                    i += 1
                else:
                    packets[k] = right[j]
                    j += 1
                k += 1
            while i < len(left):
                packets[k] = left[i]
                i += 1
                k += 1

            while j < len(right):
                packets[k] = right[j]
                j += 1
                k += 1

    # Quick sort needs three function
    @time_me
    def quick_sort(self):
        sorted_by_quick_sort = self.packets

        self.conquer(sorted_by_quick_sort, 0, len(sorted_by_quick_sort) - 1)

        fd_index = 0
        sd_index = 0
        for i, pack in enumerate(sorted_by_quick_sort):
            if pack == self.first_divider:
                fd_index = i + 1
            if pack == self.second_divider:
                sd_index = i + 1
        print("---------------------------------")
        print("quick")
        return fd_index * sd_index

    def divide(self, packets: List[Packet], left: int, right: int) -> int:
        pivot = packets[right]
        i = left - 1

        for j in range(left, right):
            if self.check_order(deepcopy(packets[j].container), deepcopy(pivot.container)):
                i = i + 1
                packets[i], packets[j] = packets[j], packets[i]

        if self.check_order(deepcopy(packets[right].container), deepcopy(packets[i + 1].container)):
            packets[right], packets[i + 1] = packets[i + 1], packets[right]

        return i + 1

    def conquer(self, packets: List[Packet], left: int, right: int):
        if left < right:
            pivot = self.divide(packets, left, right)

            self.conquer(packets, left, pivot - 1)
            self.conquer(packets, pivot + 1, right)

    @time_me
    def python_sort(self):
        sorted_by_python = self.packets.copy()
        sorted_by_python.sort()

        fd_index = 0
        sd_index = 0
        for i, pack in enumerate(sorted_by_python):
            if pack == self.first_divider:
                fd_index = i + 1
            if pack == self.second_divider:
                sd_index = i + 1
        print("---------------------------------")
        print("python")
        return fd_index * sd_index


def get_packets():
    with open("day_13.txt") as f:
        packets = []
        for line in f.readlines():
            if line.strip() != "":
                packet = Packet(
                    container=json.loads(line)
                )
                packets.append(packet)
        return packets


def very_solution():
    sorter = Sorter()
    part_uno = sorter.get_solution_part_one()

    merge = sorter.merge_sort()
    quick = sorter.quick_sort()
    bubble = sorter.bubble_sort()
    insertion = sorter.insertion_sort()
    selection = sorter.selection_sort()
    python = sorter.python_sort()

    print("---------------------------------")
    print("Solutions Part Two")
    print(f"quick = {quick}, merge = {merge}, bubble = {bubble}, insertion = {insertion}, selection = {selection}, python_sort = {python}")
    print("---------------------------------")

    return part_uno


if __name__ == "__main__":
    solution_one = very_solution()
    print(f"Solution part one = {solution_one}")

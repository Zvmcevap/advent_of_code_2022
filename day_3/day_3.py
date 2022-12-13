from utils.stop_watch import time_me
import re
import string

letters = list(string.ascii_letters)
rucksacks = []
print(letters)

with open("day_3.txt") as f:
    for line in f.readlines():
        rucksacks.append(line.strip())


@time_me
def part_one():
    value = 0
    for ruck in rucksacks:
        r_1 = ruck[:int(len(ruck) / 2)]
        r_2 = ruck[int(len(ruck) / 2):]

        match = set(r_1) & set(r_2)
        if len(match) > 0:
            for letter in match:
                value += letters.index(letter) + 1

    print(f"Solution part one = {value}")


@time_me
def part_two():
    value = 0
    for i in range(0, len(rucksacks) - 2, 3):
        match = set(rucksacks[i]) & set(rucksacks[i+1]) & set(rucksacks[i+2])
        value += letters.index(match.pop()) + 1

    print(f"Solution part two = {value}")



if __name__ == "__main__":
    part_one()
    part_two()

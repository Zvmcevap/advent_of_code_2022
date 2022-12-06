from utils.stop_watch import time_me

from collections import deque
import re


@time_me
def create_data_from_input():
    commands = []
    commands_started = False
    stacks = []

    for i in range(9):
        sklad = deque()
        stacks.append(sklad)

    with open("day_5.txt") as f:
        for line in f.readlines():
            if set("[") & set(line.strip()):
                for i, char in enumerate(line.strip()):
                    if not (char == "[" or char == " " or char == "]"):
                        stack_position = int(((i - 1) / 4))
                        stacks[stack_position].append(char)

            if commands_started:
                search_pattern = re.search("move ([0-9]+) from ([0-9]+) to ([0-9]+)", line)
                command = {}
                command["move"] = int(search_pattern.group(1))
                command["from"] = int(search_pattern.group(2))
                command["to"] = int(search_pattern.group(3))
                commands.append(command)

            if not line.strip():
                commands_started = True

    for sklad in stacks:
        sklad.reverse()
    return stacks, commands


@time_me
def part_one():
    stacks, commands = create_data_from_input()
    for command in commands:
        for i in range(command["move"]):
            stacks[command["to"] - 1].append(stacks[command["from"] - 1].pop())

    solution = ""
    for sklad in stacks:
        solution += sklad.pop()
    print(f"Solution = {solution}")


@time_me
def part_two():
    stacks, commands = create_data_from_input()
    tovorna_mesta = []
    for sklad in stacks:
        tovorna_mesta.append(list(sklad))

    for command in commands:
        how_many = command["move"]
        tovorna_mesta[command["to"] - 1] += tovorna_mesta[command["from"] - 1][-how_many:]
        tovorna_mesta[command["from"] - 1] = tovorna_mesta[command["from"] - 1][:-how_many]

    solution = ""
    for mesto in tovorna_mesta:
        solution += mesto[-1]
    print(solution)



if __name__ == "__main__":
    part_one()
    part_two()

from utils.stop_watch import time_me
from typing import List, Dict


def get_input_list():
    with open("day_11.txt") as f:
        return [line.strip().split(":") for line in f.readlines()]


class Item:
    def __init__(self, worry_value: int):
        self.worry_value: int = worry_value

    def __repr__(self):
        return f"{self.worry_value}"


class Monkey:
    def __init__(self, items, operation, test_value):
        self.items: List[Item] = items
        self.operation: List[str] = operation
        self.test_value: int = test_value
        self.throw_to: Dict[bool, Monkey] = {}
        self.checked_item_counter = 0

    def calculate_worry(self, item):
        self.checked_item_counter += 1
        if self.operation[0] == "+":
            if self.operation[1] == "old":
                item.worry_value += item.worry_value
            else:
                item.worry_value += int(self.operation[1])
        elif self.operation[0] == "*":
            if self.operation[1] == "old":
                item.worry_value *= item.worry_value
            else:
                item.worry_value *= int(self.operation[1])
        item.worry_value = item.worry_value % (2 * 3 * 5 * 7 * 11 * 13 * 17 * 19)  # :D

    def test(self, item: Item, relief: bool):
        if relief:
            item.worry_value = int(item.worry_value / 3)
        return item.worry_value % self.test_value == 0

    def throw(self, item, relief: bool):
        self.throw_to[self.test(item=item, relief=relief)].items.append(item)

    def play_round(self, relief: bool):
        for item in self.items:
            self.calculate_worry(item=item)
            self.throw(item=item, relief=relief)
        self.items.clear()

    def __lt__(self, other):
        return self.checked_item_counter < other.checked_item_counter

    def __str__(self):
        return f"Monkey, checked: {self.checked_item_counter}, items: {self.items}"


def make_monkey_list():
    input_list = get_input_list()
    monkeys = []
    items = []
    operations = []
    for line in input_list:
        if line[0] == "Starting items":
            items = [Item(worry_value=int(value)) for value in line[1].split(", ")]
        if line[0] == "Operation":
            operations = [line[1].split()[-2], line[1].split()[-1]]
        if line[0] == "Test":
            test_value = int(line[1].split()[-1])
            new_monkey = Monkey(items=items, operation=operations, test_value=test_value)
            monkeys.append(new_monkey)

    monkey_number = 0
    for line in input_list:
        if line[0] == "If true":
            monkeys[monkey_number].throw_to[True] = monkeys[int(line[1].split()[-1])]
        if line[0] == "If false":
            monkeys[monkey_number].throw_to[False] = monkeys[int(line[1].split()[-1])]
            monkey_number += 1
    return monkeys


@time_me
def get_monkey_business(relief: bool, rounds: int):
    monkeys = make_monkey_list()
    for i in range(rounds):
        for monkey in monkeys:
            monkey.play_round(relief=relief)
    monkeys.sort(reverse=True)
    return monkeys[0].checked_item_counter * monkeys[1].checked_item_counter


if __name__ == "__main__":
    solution_one = get_monkey_business(True, 20)
    print(f"Solution part one = {solution_one}")
    solution_two = get_monkey_business(False, 10000)
    print(f"Solution part two = {solution_two}")

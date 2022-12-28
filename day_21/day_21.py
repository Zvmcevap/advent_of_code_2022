from typing import Optional, List

from utils.stop_watch import time_me


def assemble_monkeys():
    with open("day_21.txt") as f:
        monkey_yell = []
        monkey_do = []
        root = None
        humn = None
        for line in f.readlines():
            data = line.strip().split()
            if len(data) == 2:
                monkey = Monkey(name=data[0][:-1], number=int(data[1]))
                monkey_yell.append(monkey)
                if monkey.name == "humn":
                    humn = monkey
            else:
                monkey = Monkey(name=data[0][:-1], operation=data[2], monkey_names=[data[1], data[3]])
                if monkey.name == "root":
                    root = monkey
                if monkey.name == "humn":
                    humn = monkey
                monkey_do.append(monkey)
        for monkey in monkey_do:
            for yeller in monkey_yell:
                if monkey.waiting_names[0] == yeller.name:
                    monkey.waiting_on.insert(0, yeller)
                    yeller.influences.append(monkey)
                if monkey.waiting_names[1] == yeller.name:
                    monkey.waiting_on.insert(1, yeller)
                    yeller.influences.append(monkey)
                if len(monkey.waiting_on) == 2:
                    monkey.do()
                    break
            if len(monkey.waiting_on) < 2:
                for doer in monkey_do:
                    if monkey.waiting_names[0] == doer.name:
                        monkey.waiting_on.insert(0, doer)
                        doer.influences.append(monkey)
                    if monkey.waiting_names[1] == doer.name:
                        monkey.waiting_on.insert(1, doer)
                        doer.influences.append(monkey)
                    if len(monkey.waiting_on) == 2:
                        break
    return monkey_do, root, humn


class Monkey:
    def __init__(self, name: str, number: int = None, operation: str = None, monkey_names: List[str] = None):
        self.name: str = name
        self.number: Optional[int] = number
        self.operation: Optional[str] = operation
        self.waiting_names: Optional[List[str]] = monkey_names
        self.waiting_on: List[Monkey] = []
        self.influences: List[Monkey] = []

    def do(self):
        if self.waiting_on[0].number is None or self.waiting_on[1].number is None:
            print(self.waiting_on)
            raise Exception(self.waiting_on[0], self.waiting_on[1])
        if self.operation == "+":
            self.number = self.waiting_on[0].number + self.waiting_on[1].number
        if self.operation == "-":
            self.number = self.waiting_on[0].number - self.waiting_on[1].number
        if self.operation == "*":
            self.number = self.waiting_on[0].number * self.waiting_on[1].number
        if self.operation == "/":
            self.number = self.waiting_on[0].number / self.waiting_on[1].number
        if self.name == "root":
            return self.waiting_on[0].number == self.waiting_on[1].number

    def do_reverse(self, main_influence, number_needed: int):
        if self.name == "root":
            return self.waiting_on[0].number if self.waiting_on[0] != main_influence else self.waiting_on[1].number
        if self.name == "humn":
            self.number = number_needed

        if self.operation == "+":
            if self.waiting_on[0] == main_influence:
                return number_needed - self.waiting_on[1].number
            return number_needed - self.waiting_on[0].number

        if self.operation == "-":
            if self.waiting_on[0] == main_influence:
                return number_needed + self.waiting_on[1].number
            return self.waiting_on[0].number - number_needed

        if self.operation == "*":
            if self.waiting_on[0] == main_influence:
                return number_needed / self.waiting_on[1].number
            return number_needed / self.waiting_on[0].number

        if self.operation == "/":
            if self.waiting_on[0] == main_influence:
                return number_needed * self.waiting_on[1].number
            return self.waiting_on[0].number / number_needed

    def __str__(self):
        fancy_string = f"{self.name}: {self.number} | "
        if len(self.waiting_on) == 2:
            fancy_string += f"{self.waiting_on[0].name}: {self.waiting_on[0].number} {self.operation} {self.waiting_on[1].name}: {self.waiting_on[1].number}"
        return fancy_string

    def __repr__(self):
        return f"{self.name} number: {self.number} operations: {self.operation}"


def make_monkeys_make_maths(waiter: Monkey):
    for monkey in waiter.waiting_on:
        if monkey.number is None:
            make_monkeys_make_maths(waiter=monkey)
    waiter.do()


def chain_influences(influencer: Monkey, chain: List[Monkey]):
    chain.append(influencer)
    for monkey in influencer.influences:
        if monkey.name == "root":
            chain.append(monkey)
            return chain
        new_chain = chain.copy()
        new_chain = chain_influences(influencer=monkey, chain=new_chain)
        if new_chain is not None:
            return new_chain


@time_me
def monkey_business():
    monkey_do, root, me = assemble_monkeys()
    make_monkeys_make_maths(waiter=root)

    chain_of_influences = chain_influences(influencer=me, chain=[])

    chain_of_influences.reverse()

    number_needed = None
    for i in range(len(chain_of_influences)):
        if i == len(chain_of_influences) - 1:
            chain_of_influences[i].do_reverse(main_influence=None, number_needed=number_needed)
            break
        number_needed = chain_of_influences[i].do_reverse(main_influence=chain_of_influences[i + 1],
                                                          number_needed=number_needed)


    # Test the little monkey maths
    for monkey in monkey_do:
        monkey.number = None
    make_monkeys_make_maths(waiter=root)
    print(root)
    print(root.do())
    return root.number, me.number


if __name__ == "__main__":
    one, two = monkey_business()
    print(f"One is {one}")
    print(f"Two is {two}")

from typing import List, Union

from utils.stop_watch import time_me


class EmptyGround:
    def __init__(self, row, column):
        self.row = row
        self.col = column
        self.elves_wanting: List[Elf] = []

    def move_elves(self, grove):
        if len(self.elves_wanting) > 1:
            for elf in self.elves_wanting:
                elf.can_move = False
            self.elves_wanting.clear()
            return False
        if len(self.elves_wanting) == 1:
            elf_to_move = self.elves_wanting[0]
            grove[self.row][self.col] = elf_to_move
            grove[elf_to_move.row][elf_to_move.col] = self
            self.row, self.col, elf_to_move.row, elf_to_move.col = elf_to_move.row, elf_to_move.col, self.row, self.col
            elf_to_move.can_move = False
            self.elves_wanting.clear()
            return True
        return False

    def __repr__(self):
        return f"Ground: {self.row, self.col}"

    def __str__(self):
        return "."


class Elf:
    def __init__(self, row, column):
        self.can_move = False
        self.row = row
        self.col = column
        self.search_pattern = ["N", "S", "W", "E"]

    def check_north(self, grove: List[EmptyGround]):
        for space in range(-1, 2, 1):
            if isinstance(grove[self.row - 1][self.col + space], Elf):
                return False
        grove[self.row - 1][self.col].elves_wanting.append(self)
        return True

    def check_south(self, grove: List[EmptyGround]):
        for space in range(-1, 2, 1):
            if isinstance(grove[self.row + 1][self.col + space], Elf):
                return False
        grove[self.row + 1][self.col].elves_wanting.append(self)
        return True

    def check_west(self, grove: List[EmptyGround]):
        for space in range(-1, 2, 1):
            if isinstance(grove[self.row + space][self.col - 1], Elf):
                return False
        grove[self.row][self.col - 1].elves_wanting.append(self)
        return True

    def check_east(self, grove: List[EmptyGround]):
        for space in range(-1, 2, 1):
            if isinstance(grove[self.row + space][self.col + 1], Elf):
                return False
        grove[self.row][self.col + 1].elves_wanting.append(self)
        return True

    def staying_put(self, grove):
        for space in range(-1, 2, 1):
            if isinstance(grove[self.row + space][self.col - 1], Elf):
                return False
            if isinstance(grove[self.row + space][self.col + 1], Elf):
                return False
            if isinstance(grove[self.row + 1][self.col + space], Elf):
                return False
            if isinstance(grove[self.row - 1][self.col + space], Elf):
                return False
        return True

    def search_for_a_spot(self, seek_at, grove):
        if self.staying_put(grove=grove):
            return True
        for search in range(4):
            if self.search_pattern[(seek_at + search) % 4] == "N" and self.check_north(grove=grove):
                self.can_move = True
                return
            if self.search_pattern[(seek_at + search) % 4] == "S" and self.check_south(grove=grove):
                self.can_move = True
                return
            if self.search_pattern[(seek_at + search) % 4] == "W" and self.check_west(grove=grove):
                self.can_move = True
                return
            if self.search_pattern[(seek_at + search) % 4] == "E" and self.check_east(grove=grove):
                self.can_move = True
                return

    def __repr__(self):
        return f"Elf: {self.row, self.col}"

    def __str__(self):
        return "#"


def load_grove(filename):
    groove = []
    elfs = []
    empty_grounds = []
    with open(filename) as f:
        for row, line in enumerate(f.readlines()):
            groovy_line = []
            for column, char in enumerate(line.strip()):
                if char == ".":
                    empty_space = EmptyGround(row=row, column=column)
                    groovy_line.append(empty_space)
                    empty_grounds.append(empty_space)
                elif char == "#":
                    elf = Elf(row=row, column=column)
                    groovy_line.append(elf)
                    elfs.append(elf)
            groove.append(groovy_line)
    return groove, elfs, empty_grounds


def extend_grove(grove, empty_grounds, elfs):
    extend_left = min([elf.col for elf in elfs]) == 0
    extend_right = max([elf.col for elf in elfs]) == len(grove[0]) - 1
    extend_top = min([elf.row for elf in elfs]) == 0
    extend_bot = max([elf.row for elf in elfs]) == len(grove) - 1

    if extend_left or extend_right:
        for grove_line in grove:
            if extend_left:
                new_ground_left = EmptyGround(row=None, column=0)
                grove_line.insert(0, new_ground_left)
                empty_grounds.append(new_ground_left)
            if extend_right:
                new_ground_right = EmptyGround(row=None, column=len(grove_line))
                grove_line.append(new_ground_right)
                empty_grounds.append(new_ground_right)
    if extend_top:
        new_grow_line_top = []
        for i in range(len(grove[0])):
            new_grove_top = EmptyGround(row=0, column=i)
            new_grow_line_top.append(new_grove_top)
            empty_grounds.append(new_grove_top)
        grove.insert(0, new_grow_line_top)
    if extend_bot:
        new_grow_line_bot = []
        for i in range(len(grove[0])):
            new_grove_bot = EmptyGround(row=0, column=i)
            new_grow_line_bot.append(new_grove_bot)
            empty_grounds.append(new_grove_bot)
        grove.append(new_grow_line_bot)
    for row in range(len(grove)):
        for column, item in enumerate(grove[row]):
            item.row = row
            item.col = column


def get_free_real_estate(grove, elfs):
    elf_left = min([elf.col for elf in elfs])
    elf_right = max([elf.col for elf in elfs])
    elf_top = min([elf.row for elf in elfs])
    elf_bot = max([elf.row for elf in elfs])

    free_real_estate = 0
    for gl in grove[elf_top: elf_bot + 1]:
        for item in gl[elf_left: elf_right + 1]:
            if isinstance(item, EmptyGround):
                free_real_estate += 1
    return free_real_estate


@time_me
def gardening():
    test = False
    filename = "test.txt" if test else "day_23.txt"
    grove, elfs, empty_grounds = load_grove(filename)

    solution_one = None
    solution_two = 0
    elfs_have_moved = True

    while elfs_have_moved:
        elfs_have_moved = False
        decision_ticker = solution_two % 4
        extend_grove(grove=grove, empty_grounds=empty_grounds, elfs=elfs)
        for elf in elfs:
            elf.search_for_a_spot(seek_at=decision_ticker, grove=grove)
        for e_ground in empty_grounds:
            if e_ground.move_elves(grove=grove):
                elfs_have_moved = True
        solution_two += 1
        if solution_two == 10:
            solution_one = get_free_real_estate(grove=grove, elfs=elfs)

    return solution_one, solution_two


if __name__ == "__main__":
    one, two = gardening()
    print(f"Solution one {one}")
    print(f"Solution two {two}")

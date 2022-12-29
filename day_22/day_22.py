import numpy as np

from utils.stop_watch import time_me


def get_maze(filename):
    with open(filename) as f:
        map = []
        navigation = []
        end_of_map = False
        max_m = 0
        for line in f.readlines():
            if len(line) == 1:
                end_of_map = True
            if not end_of_map:
                draw = []
                for char in line:
                    if char == " ":
                        draw.append(0)
                    if char == ".":
                        draw.append(1)
                    if char == "#":
                        draw.append(2)
                max_m = len(draw) if len(draw) > max_m else max_m
                map.append(draw)
            else:
                digits = ""
                for char in line.strip():
                    if char.isdigit():
                        digits += char
                    else:
                        navigation.append(int(digits))
                        digits = ""
                        navigation.append(char)
                if digits != "":
                    navigation.append(int(digits))
    for m in map:
        while len(m) < max_m:
            m.append(0)
    return navigation, np.array(map)


class WalkyTurny:
    def __init__(self, tablet, navigation):
        self.tablet = tablet
        self.navigation = navigation
        self.directions = ("R", "D", "L", "U")  # Right, Down, Left, Up
        self.current_direction = 0
        self.row = 0
        self.col = np.nonzero(self.tablet[0])[0][0]

    def change_direction(self, direction):
        if direction != "R" and direction != "L":
            print(direction)
            raise Exception("WTF IS THE DIRECTION")
        self.current_direction += 1 if direction == "R" else -1
        if self.current_direction == 4:
            self.current_direction = 0
        if self.current_direction == -1:
            self.current_direction = 3

    def wrap_around(self):
        new_index = None
        temp = None
        if self.directions[self.current_direction] == "R":
            temp = self.col
            while temp > 0 and self.tablet[self.row, temp - 1] != 0:
                temp -= 1
                if self.tablet[self.row, temp] == 1:
                    new_index = temp
        if self.directions[self.current_direction] == "L":
            temp = self.col
            while temp + 1 < len(self.tablet[self.row]) and self.tablet[self.row, temp + 1] != 0:
                temp += 1
                if self.tablet[self.row, temp] == 1:
                    new_index = temp
        if self.directions[self.current_direction] == "U":
            temp = self.row
            while temp + 1 < len(self.tablet) and self.tablet[temp + 1, self.col] != 0:
                temp += 1
            if self.tablet[temp, self.col] == 1:
                new_index = temp
        if self.directions[self.current_direction] == "D":
            temp = self.row
            while temp > 0 and self.tablet[temp - 1, self.col] != 0:
                temp -= 1
            if self.tablet[temp, self.col] == 1:
                new_index = temp
        return new_index

    def warp_going_right(self):
        if self.row < 50:
            new_column = 99
            new_row = 149 - self.row
            potential_direction = "L"
        elif self.row < 100:
            new_column = self.row + 50
            new_row = 49
            potential_direction = "U"
        elif self.row < 150:
            new_column = 149
            new_row = 149 - self.row
            potential_direction = "L"
        elif self.row < 200:
            new_column = self.row - 100
            new_row = 149
            potential_direction = "U"
        else:
            raise Exception("Failed Warp Right")
        if self.tablet[new_row, new_column] == 1:
            self.current_direction = self.directions.index(potential_direction)
            return new_row, new_column
        return None, None

    def warp_going_left(self):
        if self.row < 50:
            new_column = 0
            new_row = 149 - self.row
            potential_direction = "R"
        elif self.row < 100:
            new_column = self.row - 50
            new_row = 100
            potential_direction = "D"
        elif self.row < 150:
            new_column = 50
            new_row = 149 - self.row
            potential_direction = "R"
        elif self.row < 200:
            new_column = self.row - 100
            new_row = 0
            potential_direction = "D"
        else:
            raise Exception("Failed Warp Right")
        if self.tablet[new_row, new_column] == 1:
            self.current_direction = self.directions.index(potential_direction)
            return new_row, new_column
        return None, None

    def warp_going_up(self):
        if self.col < 50:
            new_column = 50
            new_row = self.col + 50
            potential_direction = "R"
        elif self.col < 100:
            new_column = 0
            new_row = self.col + 100
            potential_direction = "R"
        elif self.col < 150:
            new_column = self.col - 100
            new_row = 199
            potential_direction = "U"
        else:
            raise Exception("Failed Warp Right")
        if self.tablet[new_row, new_column] == 1:
            self.current_direction = self.directions.index(potential_direction)
            return new_row, new_column
        return None, None

    def warp_going_down(self):
        if self.col < 50:
            new_column = self.col + 100
            new_row = 0
            potential_direction = "D"
        elif self.col < 100:
            new_column = 49
            new_row = self.col + 100
            potential_direction = "L"
        elif self.col < 150:
            new_column = 99
            new_row = self.col - 50
            potential_direction = "L"
        else:
            raise Exception("Failed Warp Right")
        if self.tablet[new_row, new_column] == 1:
            self.current_direction = self.directions.index(potential_direction)
            return new_row, new_column
        return None, None

    def check_direction_and_walk(self, amount, cube):
        if self.row < 0 or self.col < 0:
            raise Exception("OUCH")
        elif self.row >= len(self.tablet) or self.col >= len(self.tablet[0]):
            raise Exception("UFF")
        elif self.directions[self.current_direction] == "R":
            self.walk_right(amount=amount, cube=cube)
        elif self.directions[self.current_direction] == "L":
            self.walk_left(amount=amount, cube=cube)
        elif self.directions[self.current_direction] == "U":
            self.walk_up(amount=amount, cube=cube)
        elif self.directions[self.current_direction] == "D":
            self.walk_down(amount=amount, cube=cube)

    def walk_right(self, amount, cube):
        for i in range(amount):
            new_index = self.col + 1
            if new_index == len(self.tablet[self.row]) or self.tablet[self.row, new_index] == 0:
                if not cube:
                    new_index = self.wrap_around()
                    if new_index is None:
                        return
                if cube:
                    new_row, new_column = self.warp_going_right()
                    if new_row is None or new_column is None:
                        return
                    self.col = new_column
                    self.row = new_row
                    self.check_direction_and_walk(amount=amount - i - 1, cube=cube)
                    return
            elif self.tablet[self.row, new_index] == 2:
                return
            self.col = new_index

    def walk_left(self, amount, cube):
        for i in range(amount):
            new_index = self.col - 1
            if new_index < 0 or self.tablet[self.row, new_index] == 0:
                if not cube:
                    new_index = self.wrap_around()
                    if new_index is None:
                        return
                if cube:
                    new_row, new_column = self.warp_going_left()
                    if new_row is None or new_column is None:
                        return
                    self.col = new_column
                    self.row = new_row
                    self.check_direction_and_walk(amount=amount - i - 1, cube=cube)
                    return
            elif self.tablet[self.row, new_index] == 2:
                return
            self.col = new_index

    def walk_up(self, amount, cube):
        for i in range(amount):
            new_index = self.row - 1
            if new_index < 0 or self.tablet[new_index, self.col] == 0:
                if not cube:
                    new_index = self.wrap_around()
                    if new_index is None:
                        return
                if cube:
                    new_row, new_column = self.warp_going_up()
                    if new_row is None or new_column is None:
                        return
                    self.col = new_column
                    self.row = new_row
                    self.check_direction_and_walk(amount=amount - i - 1, cube=cube)
                    return
            elif self.tablet[new_index, self.col] == 2:
                return
            self.row = new_index

    def walk_down(self, amount, cube):
        for i in range(amount):
            new_index = self.row + 1
            if new_index == len(self.tablet) or self.tablet[new_index, self.col] == 0:
                if not cube:
                    new_index = self.wrap_around()
                    if new_index is None:
                        return
                if cube:
                    new_row, new_column = self.warp_going_down()
                    if new_row is None or new_column is None:
                        return
                    self.col = new_column
                    self.row = new_row
                    self.check_direction_and_walk(amount=amount - 1 - i, cube=cube)
                    return
            elif self.tablet[new_index, self.col] == 2:
                return
            self.row = new_index

    def walk_the_walk(self, cube):
        i = 0
        for command in self.navigation:
            if type(command) == str:
                self.change_direction(direction=command)
            elif type(command) == int:
                self.check_direction_and_walk(amount=command, cube=cube)
                i += 1


@time_me
def part_one(cube=False):
    test = False
    filename = "test.txt" if test else "day_22.txt"
    navigation, tablet = get_maze(filename=filename)
    walkabout = WalkyTurny(navigation=navigation, tablet=tablet)
    walkabout.walk_the_walk(cube=cube)

    index_of_direction = walkabout.directions.index(walkabout.directions[walkabout.current_direction])
    column = walkabout.col + 1
    row = walkabout.row + 1
    solution = 1000 * row + 4 * column + index_of_direction
    return solution


if __name__ == "__main__":
    solution_one = part_one()
    print(f"Solution one = {solution_one}")

    solution_two = part_one(True)
    print(f"Solution two = {solution_two}")

from typing import List, Optional

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

from utils.stop_watch import time_me


class Wind:
    def __init__(self, row: int, column: int):
        self.row = row
        self.col = column
        self.start_row = row
        self.start_col = column

    def move(self, maze):
        pass


class Upwind(Wind):
    def move(self, maze: List[List[int]]):
        if self.row == 1:
            self.row = len(maze) - 2
        else:
            self.row -= 1
        maze[self.row][self.col] = 2

    def __str__(self):
        return "^"


class Downwind(Wind):
    def move(self, maze: List[List[int]]):
        if self.row == len(maze) - 2:
            self.row = 1
        else:
            self.row += 1
        maze[self.row][self.col] = 2

    def __str__(self):
        return "v"


class Leftwind(Wind):
    def move(self, maze: List[List[int]]):
        if self.col == 1:
            self.col = len(maze[0]) - 2
        else:
            self.col -= 1
        maze[self.row][self.col] = 2

    def __str__(self):
        return "<"


class Rightwind(Wind):
    def move(self, maze: List[List[int]]):
        if self.col == len(maze[0]) - 2:
            self.col = 1
        else:
            self.col += 1
        maze[self.row][self.col] = 2

    def __str__(self):
        return ">"


def get_maze_dimensions_and_winds(filename):
    winds_of_change = []
    with open(filename) as f:
        row = 0
        for line in f.readlines():
            map_width = len(line.strip())
            for column, character in enumerate(line.strip()):
                if character == "<":
                    wind = Leftwind(row=row, column=column)
                elif character == ">":
                    wind = Rightwind(row=row, column=column)
                elif character == "^":
                    wind = Upwind(row=row, column=column)
                elif character == "v":
                    wind = Downwind(row=row, column=column)
                else:
                    continue
                winds_of_change.append(wind)
            row += 1
    map_length = row
    return winds_of_change, map_length, map_width


class Decider:
    def __init__(self, row: int, column: int, depth: int):
        self.row: int = row
        self.col: int = column
        self.depth: int = depth
        self.visited = False

        self.children: List[Decider] = []
        self.fully_explored = False

        # Plot purposes
        self.parent: Optional[Decider] = None

    def __str__(self):
        return f"Decision row: {self.row}; col: {self.col}; depth: {self.depth}"

    def __repr__(self):
        return f"Decision row: {self.row}; col: {self.col}; depth: {self.depth}"


class Walker:
    def __init__(self, winds: List[Wind], maze_length: int, maze_width: int):
        self.winds: List[Wind] = winds
        self.maze_h: int = maze_length
        self.maze_w: int = maze_width
        self.maze = None
        # Start Position
        self.start_row = 0
        self.start_col = 1
        # Exit Target
        self.exit_row = self.maze_h - 1
        self.exit_col = self.maze_w - 2

        # Decisions
        self.first_decision = Decider(row=self.start_row, column=self.start_col, depth=0)
        self.fastest_exit = None
        self.fastest_last_decision = None

    def reset_maze(self):
        # Make a walled matrix
        maze = np.zeros((self.maze_h, self.maze_w))
        maze[0] = maze[-1] = np.ones(self.maze_w)
        maze[:, 0] = maze[:, -1] = np.ones(self.maze_h)

        # Place the entrance and exit
        maze[self.start_row, self.start_col] = 0
        maze[self.exit_row, self.exit_col] = 0

        # Set it
        self.maze = maze

    def blow(self):
        self.reset_maze()
        for wind in self.winds:
            wind.move(maze=self.maze)

    def check_for_options(self, decision: Decider):
        decision.visited = True
        # Check Down
        if decision.row < len(self.maze) - 1 and self.maze[decision.row + 1, decision.col] == 0:
            decision.children.append(Decider(row=decision.row + 1, column=decision.col, depth=decision.depth + 1))
        # Check Right
        if self.maze[decision.row, decision.col + 1] == 0:
            decision.children.append(Decider(row=decision.row, column=decision.col + 1, depth=decision.depth + 1))
        # Check Left
        if self.maze[decision.row, decision.col - 1] == 0:
            decision.children.append(Decider(row=decision.row, column=decision.col - 1, depth=decision.depth + 1))
        # Check Up
        if decision.row > 0 and self.maze[decision.row - 1, decision.col] == 0:
            decision.children.append(Decider(row=decision.row - 1, column=decision.col, depth=decision.depth + 1))
        # Check Stay Put
        if self.maze[decision.row, decision.col] == 0:
            decision.children.append(Decider(row=decision.row, column=decision.col, depth=decision.depth + 1))

    def space_time_dijsktra(self, first_deci, going_back=False, solutions=None, been_before = False):
        if solutions is None:
            solutions = []
        open_list: List[Decider] = [first_deci]
        exit_node = (self.start_row, self.start_col) if going_back else (self.exit_row, self.exit_col)
        while len(open_list) > 0:
            if not been_before or first_deci not in open_list:
                self.blow()
            copy_of_open_list = open_list.copy()
            for deci in copy_of_open_list:
                if deci.row == exit_node[0] and deci.col == exit_node[1]:
                    solutions.append(deci)
                    if len(solutions) == 3:
                        return solutions
                    going_back = not going_back
                    return self.space_time_dijsktra(first_deci=deci,
                                                    going_back=going_back,
                                                    solutions=solutions,
                                                    been_before=True)
                open_list.remove(deci)
                self.check_for_options(decision=deci)
                for child in deci.children:
                    child.parent = deci
                    if not any(x.row == child.row and x.col == child.col for x in open_list):
                        open_list.append(child)

    def plot_maze(self, i):
        plt.imshow(self.maze)
        plt.savefig(f"./plots_part_two/{i}.png")
        plt.close()


@time_me
def part_one():
    test = False
    filename = "test.txt" if test else "day_24.txt"

    winds, map_length, map_width = get_maze_dimensions_and_winds(filename)
    walker = Walker(winds=winds, maze_length=map_length, maze_width=map_width)
    fastest_maybe = walker.space_time_dijsktra(first_deci=walker.first_decision, going_back=False, solutions=[])

    return fastest_maybe[0].depth, fastest_maybe[2].depth


def make_gif():
    frames = []
    for i in range(0, 252):
        if i > 0:
            frames.append(Image.open(f"plots_part_two/{i}.png"))
    frame_one = Image.open("plots_part_two/0.png")
    frame_one.save("path.gif", format="GIF", append_images=frames, save_all=True, duration=100, loop=0)


if __name__ == "__main__":
    solve_one, solve_two = part_one()
    print(f"Solution one {solve_one} Solution two {solve_two}")
    # make_gif()

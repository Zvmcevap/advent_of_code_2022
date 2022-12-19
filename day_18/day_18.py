from typing import List
import numpy as np

from utils.stop_watch import time_me


def get_drops(filename):
    with open(filename) as f:
        drops = []
        for line in f.readlines():
            drop = [int(i) for i in line.strip().split(",")]
            drops.append(drop)
        return drops


class Node:
    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        self.z = coords[2]
        self.wall_count = 0

    def __str__(self):
        return f"[{self.x}, {self.y}, {self.z}]"


class Droplet:
    def __init__(self, coords):
        self.x = coords[0] + 1
        self.y = coords[1] + 1
        self.z = coords[2] + 1

    def part_one_sides(self, matrix):
        non_zero_x = np.count_nonzero(matrix[self.x - 1:self.x + 2, self.y, self.z])
        non_zero_y = np.count_nonzero(matrix[self.x, self.y - 1: self.y + 2, self.z])
        non_zero_z = np.count_nonzero(matrix[self.x, self.y, self.z - 1:self.z + 2])
        # print(non_zero_x, non_zero_y, non_zero_z)
        return non_zero_x + non_zero_y + non_zero_z

    def part_two_sides(self, matrix):
        non_zero_x = np.count_nonzero(matrix[self.x - 1:self.x + 2, self.y, self.z] == 2)
        non_zero_y = np.count_nonzero(matrix[self.x, self.y - 1: self.y + 2, self.z] == 2)
        non_zero_z = np.count_nonzero(matrix[self.x, self.y, self.z - 1:self.z + 2] == 2)
        return non_zero_x + non_zero_y + non_zero_z

    def __str__(self):
        return f"[{self.x}, {self.y}, {self.z}]"

    def __repr__(self):
        return f"[{self.x}, {self.y}, {self.z}]"


class GoallessDijkstra:
    def __init__(self, le_map: np.ndarray):
        self.le_map: np.ndarray = le_map
        self.surface_count: int = 0
        self.open_list: List[Node] = [Node([0, 0, 0])]
        self.closed_list: List[tuple[int, int, int]] = []

        self.finished_nodes: set[Node] = set()

    def do_da_dijkstra(self):
        loop_count = 0
        while len(self.open_list) > 0:
            # Starten
            current_node = self.open_list[0]
            if current_node in self.finished_nodes:
                raise "DUPLICATE NODE!"
            # Check directions / if node append to open list / if true increase surface count / if false do nada
            for i in range(-1, 2, 2):
                self.check_x(n=current_node, amount=i)
                self.check_y(n=current_node, amount=i)
                self.check_z(n=current_node, amount=i)
            loop_count += 1
            self.le_map[current_node.x, current_node.y, current_node.z] = 2
            self.open_list.remove(current_node)
            self.finished_nodes.add(current_node)
            self.closed_list.append((current_node.x, current_node.y, current_node.z))

    def check_x(self, n: Node, amount: int):
        if (amount < 0 and n.x == 0) or (amount > 0 and n.x == np.size(self.le_map, axis=0) - 1):
            return
        new_node_value = self.le_map[n.x + amount, n.y, n.z]
        if new_node_value == 0:
            self.surface_count += 1
            n.wall_count += 1
            return True
        elif new_node_value == 1:
            new_node = Node([n.x + amount, n.y, n.z])
            if not self.check_if_node_exist(n):
                self.open_list.append(new_node)
            return True

    def check_y(self, n: Node, amount: int):
        if (amount < 0 and n.y == 0) or (amount > 0 and n.y == np.size(self.le_map, axis=1) - 1):
            return False
        new_node_value = self.le_map[n.x, n.y + amount, n.z]
        if new_node_value == 0:
            self.surface_count += 1
            n.wall_count += 1
            return True
        elif new_node_value == 1:
            new_node = Node([n.x, n.y + amount, n.z])
            if not self.check_if_node_exist(n):
                self.open_list.append(new_node)
            return False

    def check_z(self, n: Node, amount: int):
        if (amount < 0 and n.z == 0) or (amount > 0 and n.z == np.size(self.le_map, axis=2) - 1):
            return False
        new_node_value = self.le_map[n.x, n.y, n.z + amount]
        if new_node_value == 0:
            self.surface_count += 1
            n.wall_count += 1
            return True
        elif new_node_value == 1:
            new_node = Node([n.x, n.y, n.z + amount])
            if not self.check_if_node_exist(n):
                self.open_list.append(new_node)
            return False

    def check_if_node_exist(self, node: Node):
        return (node.x, node.y, node.z) in self.closed_list


@time_me
def part_both():
    test = False
    filename = "test.txt" if test else "day_18.txt"
    data = get_drops(filename)

    droplets = []
    for d in data:
        drop = Droplet(coords=d)
        droplets.append(drop)

    # Find array x, y, z size make 3D matrix
    maximum_x = max([drop.x for drop in droplets])
    maximum_y = max([drop.y for drop in droplets])
    maximum_z = max([drop.z for drop in droplets])
    droplet_matrix = np.ones((maximum_x + 2, maximum_y + 2, maximum_z + 2))
    # Change Droplet locations to 0 (numpy has count_non_zero function)
    for drop in droplets:
        droplet_matrix[drop.x, drop.y, drop.z] = 0

    # Part one
    sides = 0
    for drop in droplets:
        sides += drop.part_one_sides(matrix=droplet_matrix)

    # Part Dos
    path_finder = GoallessDijkstra(le_map=droplet_matrix)
    path_finder.do_da_dijkstra()
    nodes_wall_count = 0
    for drop in droplets:
        nodes_wall_count += drop.part_two_sides(matrix=droplet_matrix)

    return sides, nodes_wall_count


if __name__ == "__main__":
    solution_part_one, solution_part_duce = part_both()
    print(f"Solution part one = {solution_part_one}")
    print(f"Solution part duce = {solution_part_duce}")

from utils.stop_watch import time_me
from typing import List, Dict


def get_input():
    lines = []
    with open("day_7.txt") as f:
        for line in f.readlines():
            lines.append(line.strip().split())
        return lines


class Directory:
    def __init__(self, name, depth, papa):
        self.name: str = name
        self.contains_files: Dict[str, int] = {}
        self.contains_directories: List[Directory] = []
        self.size: int = 0
        self.depth: int = depth
        self.parent_dir: Directory = papa

    def get_size_of_files(self):
        self.size = 0
        for file_name in self.contains_files:
            self.size += self.contains_files[file_name]

    def get_size(self):
        self.get_size_of_files()
        for directory in self.contains_directories:
            directory.get_size()
            self.size += directory.size

    def print_directory(self):
        print(f'{"  " * self.depth} /{self.name} (dir) total size: {self.size}kb')
        for file_name in self.contains_files:
            print(f'{"  " * (self.depth + 1)} - {file_name} (file, {self.contains_files[file_name]}kb)')

        for directory in self.contains_directories:
            directory.print_directory()


def get_file_system():
    commands = get_input()
    root = Directory(name="/", depth=0, papa=None)
    current_dir = root

    for cmd in commands:
        if cmd[0] == "$":
            if cmd[1] == "cd":
                if cmd[2] == "..":
                    current_dir = current_dir.parent_dir
                else:
                    for directory in current_dir.contains_directories:
                        if cmd[2] == directory.name:
                            current_dir = directory
        elif cmd[0] == "dir":
            new_directory = Directory(name=cmd[1], depth=current_dir.depth + 1, papa=current_dir)
            current_dir.contains_directories.append(new_directory)
        else:
            current_dir.contains_files[cmd[1]] = int(cmd[0])
    root.get_size()
    return root


def get_sum_of_smaller_eq_than_x(directory: Directory, summation: int, x: int):
    if directory.size <= x:
        summation += directory.size
    for child_directory in directory.contains_directories:
        summation = get_sum_of_smaller_eq_than_x(directory=child_directory, summation=summation, x=x)
    return summation


def get_sizes_of_folders_big_enough_to_delete(directory: Directory, sizes: List, amount_to_delete: int):
    sizes.append(directory.size)
    for child_directory in directory.contains_directories:
        if child_directory.size >= amount_to_delete:
            sizes = get_sizes_of_folders_big_enough_to_delete(
                directory=child_directory,
                sizes=sizes,
                amount_to_delete=amount_to_delete
            )
    return sizes


@time_me
def print_file_system_for_funsies():
    root = get_file_system()
    root.print_directory()


@time_me
def part_one():
    root = get_file_system()
    solution = get_sum_of_smaller_eq_than_x(directory=root, summation=0, x=100000)
    print(f"Solution Part One = {solution}")


@time_me
def part_two():
    root = get_file_system()
    amount_to_delete = root.size - (70000000 - 30000000)
    print(amount_to_delete)
    sizes = get_sizes_of_folders_big_enough_to_delete(
        directory=root,
        sizes=[],
        amount_to_delete=amount_to_delete
    )
    solution = min(sizes)
    print(f"Solution Part Two = {solution}")


if __name__ == "__main__":
    print_file_system_for_funsies()
    part_one()
    part_two()

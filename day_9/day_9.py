from typing import Dict, List, Set, Tuple

from utils.stop_watch import time_me


def get_commands() -> List[Dict[str, int]]:
    with open("day_9.txt") as f:
        commands = []
        for line in f.readlines():
            split_line = line.strip().split()
            commands.append({split_line[0]: int(split_line[1])})
        return commands


class Pedestrian:
    def __init__(self, commands: List[Dict[str, int]], rope_length: int):
        self.commands = commands
        self.rope: List[Dict[str, int]] = [{"horizontal": 0, "vertical": 0} for i in range(rope_length)]
        self.tail_visits: Set[Tuple[int, int]] = {(0, 0)}

    def move_head(self, direction, chain):
        for key in direction:
            if key == "L" or key == "R":
                chain["horizontal"] += 1 if key == "R" else -1
            else:
                chain["vertical"] += 1 if key == "D" else -1

    def move_child(self, parent: Dict[str, int], child: Dict[str, int]):
        # Check vertically
        if abs(parent["vertical"] - child["vertical"]) > 1:
            child["vertical"] += int((parent["vertical"] - child["vertical"]) / 2)
            # Check diagonally
            if abs(parent["horizontal"] - child["horizontal"]) > 1:
                child["horizontal"] += int((parent["horizontal"] - child["horizontal"]) / 2)
            elif parent["horizontal"] != child["horizontal"]:
                child["horizontal"] = parent["horizontal"]
            return

        # Check horizontally
        if abs(parent["horizontal"] - child["horizontal"]) > 1:
            child["horizontal"] += int((parent["horizontal"] - child["horizontal"]) / 2)
            # Check if diagonally
            if abs(parent["vertical"] - child["vertical"]) > 1:
                child["vertical"] += int((parent["vertical"] - child["vertical"]) / 2)
            elif parent["vertical"] != child["vertical"]:
                child["vertical"] = parent["vertical"]
            return

    def take_a_walk(self):
        for command in self.commands:
            for direction in command:
                for steps in range(command[direction]):
                    for i, chain in enumerate(self.rope):
                        if i == 0:
                            self.move_head(direction=direction, chain=chain)
                        else:
                            self.move_child(parent=self.rope[i - 1], child=chain)
                    self.tail_visits.add((self.rope[-1]["horizontal"], self.rope[-1]["vertical"]))
        return self.tail_visits


@time_me
def get_tale_visits_of_snakey_rope(rope_length: int):
    pedestrian = Pedestrian(commands=get_commands(), rope_length=rope_length)
    return len(pedestrian.take_a_walk())


if __name__ == "__main__":
    print(f"Solution to part one is {get_tale_visits_of_snakey_rope(2)}")
    print(f"Solution for part two is {get_tale_visits_of_snakey_rope(10)}")

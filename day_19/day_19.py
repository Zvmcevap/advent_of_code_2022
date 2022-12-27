import math
from typing import Dict, Optional, List
import re

from utils.stop_watch import time_me


def load_blueprints(filename):
    blueprints = []
    pattern = "Blueprint ([0-9]+):.* ([0-9]+) ore.* ([0-9]+) ore.* ([0-9]+) ore and ([0-9]+) clay.* ([0-9]+) ore and ([0-9]+) obsidian."
    with open(filename) as f:
        for line in f.readlines():
            data = re.findall(string=line.strip(), pattern=pattern)[0]
            costs = {"ore": {"ore": int(data[1])},
                     "clay": {"ore": int(data[2])},
                     "obsidian": {"ore": int(data[3]), "clay": int(data[4])},
                     "goede": {"ore": int(data[5]), "obsidian": int(data[6])}
                     }
            blueprint = Blueprint(blue_num=int(data[0]), costs=costs)
            blueprints.append(blueprint)
    return blueprints


class Blueprint:
    def __init__(self, blue_num: int, costs):
        self.id: int = blue_num
        self.costs: Dict[str, Dict[str, int]] = costs

    def __str__(self):
        return f"Blueprint: {self.id}" \
               f"\nCosts: " \
               f"\nOre bot = {self.costs['ore']}" \
               f"\nClay bot = {self.costs['clay']} " \
               f"\nObsidian bot = {self.costs['obsidian']}" \
               f"\nGoede bot = {self.costs['goede']}"


class Stratagem:
    def __init__(self, blueprint: Blueprint):
        self.blueprint: Blueprint = blueprint
        self.goedes_collected: int = 0
        self.silos: Dict[str, int] = {"ore": 0, "clay": 0, "obsidian": 0, "goede": 0}
        self.garage: Dict[str, int] = {"ore": 1, "clay": 0, "obsidian": 0, "goede": 0}

    def tree_of_decisions(self, time_left: int, silos: Dict[str, int], garage: Dict[str, int]):
        # Worth it? HUZZAH!
        if silos["goede"] + time_left * garage["goede"] + time_left * (time_left - 1)/2 < self.goedes_collected:
            return
        if time_left == 0:
            if self.goedes_collected < silos["goede"]:
                self.goedes_collected = silos["goede"]
            return

        my_options = self.get_options(garage=garage, silos=silos, time_left=time_left)
        if len(my_options) == 0:
            silos["goede"] += time_left * garage["goede"]
            if self.goedes_collected < silos["goede"]:
                self.goedes_collected = silos["goede"]
            return

        for robot in my_options:
            time_spent = my_options[robot]
            time_that_will_be_left = time_left - time_spent
            new_silos = self.harvest_mineral(silos=silos, garage=garage, time_spent=time_spent)
            for mineral in self.blueprint.costs[robot]:
                new_silos[mineral] -= self.blueprint.costs[robot][mineral]
            new_garage = garage.copy()
            new_garage[robot] += 1
            self.tree_of_decisions(time_left=time_that_will_be_left, silos=new_silos, garage=new_garage)

    def harvest_mineral(self, silos, garage, time_spent):
        new_silos = {}
        for mineral in silos:
            new_silos[mineral] = silos[mineral] + time_spent * garage[mineral]
        return new_silos

    def get_options(self, garage, silos, time_left):
        # Opcije za robota so tiste katere lahko zgradim v danem času
        my_options: Dict[str, int] = {}
        for robot in garage:
            costs = self.blueprint.costs[robot]
            can_build = True
            max_time_to_harvest = 0
            for mineral in costs:
                if mineral == "ore" and garage["ore"] >= 5:
                    can_build = False
                    break
                if mineral == "clay" and garage["clay"] >= self.blueprint.costs["obsidian"]["clay"]:
                    can_build = False
                    break
                if mineral == "obsidian" and garage["obsidian"] >= self.blueprint.costs["goede"]["obsidian"]:
                    can_build = False
                    break
                if garage[mineral] == 0:
                    can_build = False
                    break
                time_to_harvest = math.ceil((costs[mineral] - silos[mineral]) / garage[mineral])
                if time_to_harvest >= time_left:
                    can_build = False
                    break
                max_time_to_harvest = time_to_harvest if time_to_harvest > max_time_to_harvest else max_time_to_harvest
            if can_build and max_time_to_harvest < 5:
                if robot == "goede" and max_time_to_harvest == 0:
                    return {"goede": 1}
                my_options[robot] = max_time_to_harvest + 1

        return my_options


@time_me
def play_starcraft():
    test = False
    filename = "test2.txt" if test else "day_19.txt"
    blueprints = load_blueprints(filename=filename)

    # Part One
    part_one_goades = []
    print("--- PART ONE ---")
    for b in blueprints:
        strategy = Stratagem(blueprint=b)
        strategy.tree_of_decisions(time_left=24, silos=strategy.silos, garage=strategy.garage)
        goedes_collected = strategy.goedes_collected
        print(b)
        print(f"Goedes Collected: {goedes_collected}")
        part_one_goades.append(b.id * goedes_collected)

    # Part two
    do_times = 2 if test else 3
    part_two_goedes = []
    print("\n--- PART TWO ---")
    for blue in range(do_times):
        strategy = Stratagem(blueprint=blueprints[blue])
        strategy.tree_of_decisions(time_left=32, silos=strategy.silos, garage=strategy.garage)
        part_two_goedes.append(strategy.goedes_collected)
        print(blueprints[blue])
        print(f"Goedes Collected: {strategy.goedes_collected}")
        print("-------------")
    solution_dos = 1
    for goede in part_two_goedes:
        solution_dos *= goede

    return sum(part_one_goades), solution_dos


if __name__ == "__main__":
    solution_one, solution_two = play_starcraft()
    print(f"Solve one = {solution_one}")
    print(f"Solve two = {solution_two}")

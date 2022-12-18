import math
from copy import deepcopy
from operator import attrgetter
from typing import List, Dict

from utils.stop_watch import time_me
from plot_maker import plot_graph
import re


def get_input(filename):
    valves = []
    with open(filename) as f:
        for line in f.readlines():
            names = re.findall(pattern='[A-Z][A-Z]', string=line.strip())
            flow = re.search(pattern='[0-9]+', string=line.strip())
            valve = Valve(name=names[0], flow=int(flow.group()), valve_names=[names[i] for i in range(1, len(names))])
            valves.append(valve)
        for valve in valves:
            valve.find_my_valves(all_valves=valves)
    return valves


class Valve:
    def __init__(self, name: str, flow: int, valve_names: List[str]):
        self.name: str = name
        self.flow: int = flow
        self.valve_names: List[str] = valve_names
        self.connections: List[Valve] = []
        # Decision making
        self.potential_flow: int = 0
        # Make tree
        self.parent = None
        self.distance = math.inf
        # Big reset
        self.remember_thy_flow: int = flow
        self.end_pressure: int = 0

    def find_my_valves(self, all_valves: List):
        for valve in all_valves:
            if valve.name in self.valve_names:
                self.connections.append(valve)

    def get_potential_flow(self, time: int) -> int:
        flow = self.flow * (time - 1)
        return flow if flow > 0 else 0

    def open_valve(self, time):
        pressure = self.flow * (time - self.distance - 1)
        self.end_pressure = pressure if pressure > 0 else 0
        self.flow = 0

    def __str__(self):
        parent_name = None
        if self.parent:
            parent_name = self.parent.name
        return f"Valve: {self.name}, flow: {self.flow}, potential: {self.potential_flow} distance: {self.distance} //parent: {parent_name}"

    def __repr__(self):
        return f"{self.name}"


class Path:
    def __init__(self):
        self.valve_names: List[str] = []
        self.score: int = 0
    def __str__(self):
        return f"{self.valve_names} score: {self.score}"


class Decision:
    def __init__(self):
        self.made_decisions: List[Decision] = []
        self.possible_paths: int = 0
        self.fully_explored = False

    def __str__(self):
        return f"Dec: {self.made_decisions} //Paths: {self.possible_paths}"

    def __repr__(self):
        return f"{self.possible_paths}"


class PathRememberer:
    def __init__(self, valves: List[Valve]):
        self.valves: List[Valve] = valves
        # Decision making
        self.decision: Decision = Decision()
        # End Game
        self.paths: List[Path] = []
        self.end_scores = []

    def should_I_open(self, time, current_valve: Valve, compare_valve: Valve):
        if current_valve.flow == 0:
            return False
        time_difference = int(abs(compare_valve.distance - current_valve.distance))
        my_valve_potential = current_valve.get_potential_flow(time=time_difference + 1)
        open_valve = 0
        move_on = 0
        open_valve += compare_valve.get_potential_flow(time=time - 1 - time_difference)
        move_on += compare_valve.get_potential_flow(time=time - time_difference)
        return open_valve + my_valve_potential > move_on

    def calculate_distances(self, current_valve: Valve, time: int):
        open_list: List[Valve] = [current_valve]
        closed_list: List[Valve] = []
        while len(open_list) > 0 and current_valve.distance < time - 1:
            current_valve = open_list[0]
            for valve in current_valve.connections:
                if valve not in open_list and valve not in closed_list:
                    valve.parent = current_valve
                    valve.distance = current_valve.distance + 1
                    open_list.append(valve)
                if valve in closed_list and valve.distance > current_valve.distance + 1:
                    valve.distance = current_valve.distance + 1
                    valve.parent = current_valve
                    open_list.append(valve)
                    closed_list.remove(valve)
            closed_list.append(current_valve)
            open_list.remove(current_valve)
        #plot_graph(closed_list, "TEST", False)
        return closed_list

    def update_potential_flow(self, valves: List[Valve], time: int):
        for v in valves:
            v.potential_flow = v.get_potential_flow(time=time)

    def find_dead_ends(self, valves: List[Valve]):
        dead_ends = valves.copy()
        for v in valves:
            if v.parent in dead_ends:
                dead_ends.remove(v.parent)
        return dead_ends

    def compare_child_to_candidate(self, child: Valve, candidate: Valve, time: int):
        # If parent is worth opening, candidate isn't worth walking to
        if self.should_I_open(time=time, current_valve=child, compare_valve=candidate):
            return child
        else:
            return candidate

    def dead_end_potential(self, de: Valve, time: int):
        valve = de
        candidate = None
        if valve.parent:
            candidate = valve.parent
        # Compare the candidate to the parent of child
        while valve.parent:
            candidate = self.compare_child_to_candidate(time=time, child=valve, candidate=candidate)
            valve = valve.parent
        return candidate

    def get_candidates(self, current_valve: Valve, time: int) -> List[Valve]:
        current_valve.distance = 0
        reachable_valves = self.calculate_distances(current_valve=current_valve, time=time)
        dead_ends = self.find_dead_ends(valves=reachable_valves)
        self.update_potential_flow(valves=reachable_valves, time=time)
        potential = []
        for de in dead_ends:
            candidate = self.dead_end_potential(de=de, time=time)
            if candidate and candidate.flow > 0 and candidate not in potential:
                potential.append(candidate)
        return potential

    def small_reset(self):
        for valve in self.valves:
            valve.parent = None
            valve.potential_flow = 0
            valve.distance = math.inf

    def big_reset(self):
        self.small_reset()
        for valve in self.valves:
            valve.flow = valve.remember_thy_flow
            valve.end_pressure = 0

    def walky_venty_valvy(self):
        path = Path()
        self.big_reset()
        valves = self.valves
        current_valve = self.valves[0]
        time = 30
        decision = self.decision
        end_presure = 0
        while time > 0 and not decision.fully_explored:
            self.small_reset()
            candidates = self.get_candidates(current_valve=current_valve, time=time)
            # Tell the decision maker how many options it has
            decision.possible_paths = len(candidates)
            # Check if current valve is better than the candidates
            open_current = False
            if current_valve.flow > 0:
                for candidate in candidates:
                    if self.should_I_open(current_valve=current_valve, compare_valve=candidate, time=time):
                        open_current = True
            # Open it if yes
            if open_current and time > 0:
                end_presure += current_valve.flow * (time - 1)
                current_valve.open_valve(time=time)
                time -= 1
                if time == 0:
                    decision.fully_explored = True
                    break
            if len(candidates) == 0:
                # End search, all is done
                decision.fully_explored = True
                break
            # Check if a decision was already made
            index = None
            future_decision = None
            if len(decision.made_decisions) < decision.possible_paths:
                future_decision = Decision()
                index = len(decision.made_decisions)
                decision.made_decisions.append(future_decision)
            # else figure out how to select something new, check if path is explored
            else:
                all_explored = True
                for i, deci in enumerate(decision.made_decisions):
                    if not deci.fully_explored:
                        index = i
                        future_decision = deci
                        all_explored = False
                        break
                if all_explored:
                    decision.fully_explored = True
                    return False
            # Save decision, somewhere
            # Prepare for next minute
            if index == future_decision is None:
                decision.fully_explored = True
                break
            path.valve_names.append(current_valve.name)
            current_valve = sorted(candidates, key=attrgetter("potential_flow"))[index]
            time -= current_valve.distance
            end_presure += current_valve.flow * (time - 1) if time > 0 else 0
            current_valve.distance = 0
            current_valve.open_valve(time=time)

            if time - 1 <= 1:
                decision.fully_explored = True
                break
            decision = future_decision
            time -= 1
        # Finished With path
        all_explored = True
        for deci in self.decision.made_decisions:
            if not deci.fully_explored:
                all_explored = False
        self.decision.fully_explored = all_explored
        path.valve_names.append(current_valve.name)
        path.score = 0
        self.end_scores.append(end_presure)
        end_presure = 0
        for valve in valves:

            path.score += valve.end_pressure
        self.paths.append(path)
        return path

    def explore_all_paths(self):
        i = 0
        max_score = 0
        while not self.decision.fully_explored:
            path = self.walky_venty_valvy()
            if path:
                print(max_score, path)
            max_score += 1

def part_one():
    test = False
    input_file = save_location = "test" if test else "day_16"
    valves = get_input(input_file + ".txt")
    path_rememberer = PathRememberer(valves=valves)
    path_rememberer.explore_all_paths()
    print("PATHS")
    path_rememberer.end_scores.sort()
    for i, p in enumerate(sorted(path_rememberer.paths, key=attrgetter("score"))):
        if i > len(path_rememberer.paths) - 30:
            print(i, p, "-", path_rememberer.end_scores[i])
    print(len(path_rememberer.paths))


if __name__ == "__main__":
    solve_part_one = part_one()
    print(f"Solution to part one is {solve_part_one}")

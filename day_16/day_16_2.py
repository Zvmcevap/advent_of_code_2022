from operator import attrgetter
from itertools import combinations, permutations
from typing import List, Dict, Tuple, Optional

from utils.stop_watch import time_me
from plot_maker import plot_graph
import re


def get_input(filename):
    valves = []
    with open(filename) as f:
        for line in f.readlines():
            names = re.findall(pattern='[A-Z][A-Z]', string=line.strip())
            flow = re.search(pattern='[0-9]+', string=line.strip())
            valve = Valve(name=names[0],
                          flow=int(flow.group()),
                          connecting_names=[names[i] for i in range(1, len(names))])
            valves.append(valve)
        for valve in valves:
            valve.find_my_connections(all_valves=valves)
    return valves


class Valve:
    def __init__(self, name, flow, connecting_names):
        self.name: str = name
        self.remember_thy_flow: int = flow
        self.connections: List[Valve] = []
        self.connecting_names: List[str] = connecting_names

        # Big reset
        self.flow: int = flow
        self.end_flow: int = 0

        # Small reset
        self.distance: int = 30
        self.potential_flow: int = 0
        self.time_flow: int = 0

    def find_my_connections(self, all_valves):
        for valve in all_valves:
            if valve.name in self.connecting_names:
                self.connections.append(valve)

    def open_valve(self, time):
        if time - 1 < 0:
            raise Exception("Valve Opening Went To Hell")
        self.end_flow = self.flow * time
        self.flow = 0

    def __str__(self):
        return f"{self.name};flow: {self.flow} potencial: {self.potential_flow} distance: {self.distance};"

    def __repr__(self):
        return f"{self.name}"


class Decision:
    def __init__(self, valve, score_up_to_now: int, parent):
        self.valve = valve
        self.score = score_up_to_now
        self.valve_distance = valve.distance
        self.parent = parent
        self.calculated_possible_paths = False
        self.made_decisions: Dict[Valve, Optional[Decision]] = {}
        self.fully_explored: bool = False

    def check_if_fully_explored(self):
        self.fully_explored = True
        for valve in self.made_decisions:
            if not self.made_decisions[valve] or self.made_decisions[valve].fully_explored:
                self.fully_explored = False

    def __str__(self):
        return f"Valve: {self.valve}, Score: {self.score} explored: {self.fully_explored}// {self.made_decisions}"

    def __repr__(self):
        return f"Valve: {self.valve.name} explored: {self.fully_explored}//"


class Manaphant:
    def __init__(self):
        self.target: Optional[Valve] = None
        self.time_to_open: int = 0
        self.score_added = 0
        self.paused = False
        # self.valve_distances_from_target: Dict[Valve, int] = {}

    def select_new_target(self, valve: Valve, time_left: int):
        self.target = valve
        self.time_to_open = valve.distance + 1
        if time_left - self.time_to_open < 1:
            raise Exception("Inappropriate distance to target")
        self.score_added = self.target.flow * (time_left - self.time_to_open)
        self.target.open_valve(time=time_left - self.time_to_open)
        return self.score_added

    def play_round(self):
        self.time_to_open -= 1
        if self.time_to_open > 0:
            return False
        elif self.time_to_open == 0 and self.target:
            return True

    def __str__(self):
        return f"Target: {self.target}, time remaining: {self.time_to_open}"


class PathFinder:
    def __init__(self, valves: List[Valve]):
        self.valves: List[Valve] = valves
        # Decision-making
        self.decision: Decision = Decision(score_up_to_now=0, valve=self.get_first_valve(), parent=None)
        # End Game
        self.part_one_end_scores = []
        self.part_two_end_scores = []

    def get_first_valve(self):
        for valve in self.valves:
            if valve.name == "AA":
                valve.distance = 0
                return valve

    def big_reset(self):
        self.small_reset(self.decision)
        for valve in self.valves:
            valve.flow = valve.remember_thy_flow
            valve.end_flow = 0

    def small_reset(self, decision: Decision):
        for valve in self.valves:
            valve.parent = None
            valve.distance = 30
            valve.potential_flow = 0
        self.recursion_reset(decision=decision)

    def recursion_reset(self, decision: Decision):
        decision.valve.flow = 0
        if decision.parent:
            self.recursion_reset(decision=decision.parent)

    def calculate_distances(self, current_valve: Valve, time_left: int):
        open_list: List[Valve] = [current_valve]
        closed_list: List[Valve] = []

        while len(open_list) > 0:
            # Select current Valve, remove it from the open list, add to closed list
            current_valve = open_list[0]
            # If it does not lead to next valve it's a dead end
            open_list.remove(current_valve)
            closed_list.append(current_valve)

            # No need to check connections if distance > time left - (time to open + 1):
            if current_valve.distance + 1 > time_left - 2:
                continue

            # Get it's connections, set distances, potential_flow and parent:
            for valve in current_valve.connections:
                if valve not in closed_list and valve not in open_list:
                    valve.distance = current_valve.distance + 1
                    valve.potential_flow = valve.flow * (time_left - 1 - valve.distance)
                    valve.time_flow = valve.flow * (time_left - 1)
                    open_list.append(valve)
                if valve in closed_list and valve.distance > current_valve.distance + 1:
                    valve.distance = current_valve.distance + 1
                    valve.potential_flow = valve.flow * (time_left - 1 - valve.distance)
                    closed_list.remove(valve)
                    open_list.append(valve)
                if valve in open_list and valve.distance > current_valve.distance + 1:
                    valve.distance = current_valve.distance + 1
                    valve.potential_flow = valve.flow * (time_left - 1 - valve.distance)
                    open_list.append(valve)
        # plot_graph(valves=closed_list, filename=30-time_left, full_graph=False)
        return closed_list

    def remove_zero_flow_valves(self, valves: List[Valve]):
        valves_copy = valves.copy()
        for valve in valves_copy:
            if valve.flow == 0:
                valves.remove(valve)

    def get_nonzero_potential(self, valves: List[Valve]):
        valves_copy = valves.copy()
        for valve in valves:
            if valve.potential_flow == 0:
                valves_copy.remove(valve)
        return valves_copy

    def get_candidates_two_point_oh(self, valves: List[Valve]):
        if len(valves) <= 7:
            return valves
        return valves[0: 8]

    def print_decision(self, decision: Decision):
        print(decision)
        if decision.parent:
            self.print_decision(decision=decision.parent)

    def check_parents_for_paths_explored(self, decision: Decision):
        if not decision.fully_explored:
            return
        all_explored = True
        for valve in decision.made_decisions:
            if decision.made_decisions[valve] is None:
                return
            if not decision.made_decisions[valve].fully_explored:
                all_explored = False
        decision.fully_explored = all_explored
        if all_explored and decision.parent:
            self.check_parents_for_paths_explored(decision.parent)

    def walky_venty_valvy(self):
        self.big_reset()
        current_valve = self.get_first_valve()
        time = 30
        decision = self.decision
        while time > 1 and not decision.fully_explored:
            if not decision.calculated_possible_paths:
                decision.calculated_possible_paths = True
                # Check if I should open current
                if current_valve.flow > 0:  # Placeholder, just check if flow is less than 0
                    # Reduce time and open current
                    current_valve.open_valve(time=time - 1)
                    decision.score += current_valve.end_flow
                self.small_reset(decision=decision)
                # Set current_valve.distance to 0 on round start
                current_valve.distance = 0
                # Current Valve already selected, check it's candidates if to open or not
                # First find distance to all other valves
                possible_valves = self.calculate_distances(current_valve=current_valve, time_left=time)
                possible_valves.remove(current_valve)
                self.remove_zero_flow_valves(possible_valves)

                # END IF MAX SCORE IS HIGHER THAN ALL THE POTENTIAL VALVES COMBINED:
                if len(self.part_one_end_scores) > 0:
                    if max(self.part_one_end_scores) > decision.score + sum(
                            [valve.potential_flow for valve in possible_valves]):
                        print("NO USE")
                        decision.fully_explored = True
                        return False
                # Find best candidates
                possible_valves.sort(key=attrgetter("potential_flow"), reverse=True)
                candidates = self.get_candidates_two_point_oh(valves=possible_valves)
                # End if no options
                if len(candidates) == 0:
                    break
                for candidate in candidates:
                    decision.made_decisions[candidate] = Decision(valve=candidate,
                                                                  score_up_to_now=decision.score,
                                                                  parent=decision)
            if decision.valve.name != "AA":
                time -= 1
            if time <= 2:
                break
            # If options, decide on one, save it
            next_valve = None
            next_decision = None
            all_explored = True
            for valve in decision.made_decisions:
                if not decision.made_decisions[valve].calculated_possible_paths:
                    next_decision = decision.made_decisions[valve]
                    if next_decision.fully_explored:
                        continue
                    next_valve = valve
                    all_explored = False
                    break
            if next_valve is None or next_decision is None:
                for valve in decision.made_decisions:
                    if not decision.made_decisions[valve].fully_explored:
                        next_valve = valve
                        next_decision = decision.made_decisions[valve]
                        all_explored = False
                        break
            if all_explored or next_valve is None or next_decision is None:
                decision.fully_explored = True
                print("DEAD END!")
                return False
            # SAVE
            decision = next_decision
            current_valve = next_valve
            current_valve.distance = decision.valve_distance
            time -= current_valve.distance

        decision.fully_explored = True
        self.check_parents_for_paths_explored(decision=decision)
        self.part_one_end_scores.append(decision.score)
        self.part_one_end_scores.sort(reverse=True)
        return True

    def combinatorics(self):
        potentials = []
        current_valve = self.get_first_valve()
        valves = self.calculate_distances(current_valve=current_valve, time_left=26)
        for valve in valves:
            if valve.potential_flow > 0:
                potentials.append(valve)
        potentials.sort(key=attrgetter("distance"), reverse=True)
        combos = list(combinations(potentials, 2))
        print(len(combos))
        return combos

    def worth_it(self, remaining_valves, decision, time: int):
        if len(self.part_two_end_scores) == 0:
            return True
        max_potential_flow = decision.score
        for valve in remaining_valves:
            max_potential_flow += valve.flow * time
        return max_potential_flow >= max(self.part_two_end_scores)

    def calculate_distances_from_target(self, character: Manaphant, decision: Decision, time_left: int):
        self.small_reset(decision=decision)
        character.target.distance = 0
        self.calculate_distances(current_valve=character.target, time_left=time_left)

    def find_new_target(self, character: Manaphant, remaining_valves: List[Valve], time_left: int, decision: Decision):
        for valve in remaining_valves:
            if valve not in decision.made_decisions:
                decision.made_decisions[valve] = None
        for valve in remaining_valves:
            if decision.made_decisions[valve] is None and valve.potential_flow > 0:
                character.select_new_target(valve=valve, time_left=time_left)
                remaining_valves.remove(character.target)
                new_decision = Decision(character.target,
                                        score_up_to_now=decision.score + character.score_added,
                                        parent=decision)
                decision.made_decisions[valve] = new_decision
                return new_decision

        for valve in remaining_valves:
            if decision.made_decisions[valve] is not None and not decision.made_decisions[valve].fully_explored:
                character.select_new_target(valve=valve, time_left=time_left)
                remaining_valves.remove(character.target)
                return decision.made_decisions[valve]
        return None

    def starten_part_two(self):
        combos = self.combinatorics()
        ###
        c = 1
        i = 0

        for combo in combos:
            while True:
                self.big_reset()
                current_valve = self.get_first_valve()
                valves = self.valves.copy()
                self.calculate_distances(current_valve=current_valve, time_left=26)
                self.remove_zero_flow_valves(valves=valves)

                i += 1
                if i % 1000 == 0:
                    print(i)
                man = Manaphant()
                man.select_new_target(valve=combo[0], time_left=26)
                valves.remove(man.target)
                if man.target not in self.decision.made_decisions:
                    self.decision.made_decisions[man.target] = Decision(man.target,
                                                                        score_up_to_now=man.score_added,
                                                                        parent=self.decision)

                decision = self.decision.made_decisions[man.target]

                elephant = Manaphant()
                elephant.select_new_target(valve=combo[1], time_left=26)
                if elephant.target not in decision.made_decisions:
                    decision.made_decisions[elephant.target] = Decision(
                        elephant.target,
                        score_up_to_now=decision.score + elephant.score_added,
                        parent=decision)
                decision = decision.made_decisions[elephant.target]
                valves.remove(elephant.target)
                if decision.fully_explored:
                    break
                self.walky_venty_valvy_elephanty(man=man, elephant=elephant, decision=decision, valves=valves)
            print(f"COMBO NUMBER: {c}")
            if len(self.part_two_end_scores) > 0:
                print(f"Max Score = {self.part_two_end_scores[0]}")
            c += 1

    def walky_venty_valvy_elephanty(self, man: Manaphant, elephant: Manaphant, decision: Decision, valves: List[Valve]):
        time = 26
        decision = decision
        remaining_valves = valves
        for minute in range(1, time):
            if man.play_round():
                if len(remaining_valves) == 0 or not self.worth_it(remaining_valves, decision, time=time - minute):
                    break
                self.calculate_distances_from_target(character=man, decision=decision, time_left=time - minute)
                remaining_valves.sort(key=attrgetter("potential_flow"), reverse=True)
                # Pause the character if he is too far to do anything
                if remaining_valves[0].potential_flow == 0:
                    man.paused = True
                if man.paused and elephant.paused:
                    break
                if not man.paused:
                    new_decision = self.find_new_target(character=man,
                                                        remaining_valves=remaining_valves,
                                                        time_left=time - minute,
                                                        decision=decision)
                    if new_decision is None:
                        break
                    decision = new_decision

            if elephant.play_round():
                if len(remaining_valves) == 0 or not self.worth_it(remaining_valves, decision, time=time - minute):
                    break
                self.calculate_distances_from_target(character=elephant, decision=decision, time_left=time - minute)
                remaining_valves.sort(key=attrgetter("potential_flow"), reverse=True)
                # Pause the character if he is too far to do anything
                if remaining_valves[0].potential_flow == 0:
                    elephant.paused = True
                if man.paused and elephant.paused:
                    break
                if not elephant.paused:
                    new_decision = self.find_new_target(character=elephant,
                                                        remaining_valves=remaining_valves,
                                                        time_left=time - minute,
                                                        decision=decision)
                    if new_decision is None:
                        break
                    decision = new_decision
        decision.fully_explored = True
        self.check_parents_for_paths_explored(decision=decision)
        if len(self.part_two_end_scores) == 0:
            self.part_two_end_scores.append(decision.score)
        elif decision.score > self.part_two_end_scores[0]:
            self.part_two_end_scores.append(decision.score)
            self.part_two_end_scores.sort(reverse=True)


@time_me
def part_one():
    test = False
    filename = "test.txt" if test else "day_16.txt"
    valves = get_input(filename=filename)
    pathfinder = PathFinder(valves=valves)
    i = 0
    while not pathfinder.decision.fully_explored:
        i += 1
        print(i)
        pathfinder.walky_venty_valvy()
    return pathfinder.part_one_end_scores[0]

@time_me
def part_two():
    test = False
    filename = "test.txt" if test else "day_16.txt"
    valves = get_input(filename=filename)

    pathfinder = PathFinder(valves=valves)
    pathfinder.starten_part_two()


if __name__ == "__main__":
    print(f"Solution one is {part_one()}")
    part_two()

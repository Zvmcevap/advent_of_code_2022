from operator import itemgetter, attrgetter
from utils.stop_watch import time_me

from typing import List, Optional, Dict


def get_tunnel_data(file_string):
    with open(file_string) as f:
        sensors: List[Sensor] = []
        beacons: List[Beacon] = []

        for line in f.readlines():
            split_list = line.strip().split()
            sens_x = int(split_list[2].split("=")[1][:-1])
            sens_y = int(split_list[3].split("=")[1][:-1])
            beak_x = int(split_list[8].split("=")[1][:-1])
            beak_y = int(split_list[9].split("=")[1])

            sensor = Sensor(x=sens_x, y=sens_y)
            sensors.append(sensor)

            found_beak = False
            for beak in beacons:
                if beak.x == beak_x and beak.y == beak_y:
                    sensor.beak = beak
                    found_beak = True
            if not found_beak:
                beak = Beacon(x=beak_x, y=beak_y)
                sensor.beak = beak
                beacons.append(beak)
        return sensors


class Sensor:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y
        self.beak: Optional[Beacon] = None
        self.distance: int = 0
        self.top: int = 0
        self.bot: int = 0
        self.left: int = 0
        self.right: int = 0

    def calculate_distance(self):
        self.distance = abs(self.x - self.beak.x) + abs(self.y - self.beak.y)

    def calculate_vertices(self):
        self.top = self.y - self.distance
        self.bot = self.y + self.distance
        self.left = self.x - self.distance
        self.right = self.x + self.distance

    def __repr__(self):
        return f"S=[{self.top}-{self.y}-{self.bot}]  \t - Distance = {self.distance}"


class Beacon:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __str__(self):
        return f"B=[{self.x},{self.y}]"


class SignalFinder:
    def __init__(self, sensors=None):
        self.sensors: List[Sensor] = sensors

    def check_rows(self, row_limit: int):
        for row_that_matters in range(row_limit + 1):
            signal_line = self.find_signals_in_row(
                is_part_two=True,
                row_that_matters=row_that_matters,
                row_limit=row_limit
            )
            print(row_that_matters)
            if type(signal_line) == dict:
                return signal_line

    def find_signals_in_row(self, is_part_two: bool = False, row_that_matters: int = 2000000, row_limit: int = 0):
        coordinates: List[Dict] = []
        limit_right = row_limit
        for sens in self.sensors:
            # If same height
            if sens.y == row_that_matters:
                start = sens.left
                finish = sens.right
                coordinates = self.check_if_new_coordinate(
                    coordinates=coordinates,
                    start=start,
                    finish=finish,
                    is_part_two=is_part_two,
                    limit_right=limit_right
                )
            # If from above
            if sens.y < row_that_matters < sens.bot:
                difference = sens.bot - row_that_matters
                start = sens.x - difference
                finish = sens.x + difference
                coordinates = self.check_if_new_coordinate(
                    coordinates=coordinates,
                    start=start,
                    finish=finish,
                    is_part_two=is_part_two,
                    limit_right=limit_right
                )
            # If from bellow
            if sens.y > row_that_matters > sens.top:
                difference = row_that_matters - sens.top
                start = sens.x - difference
                finish = sens.x + difference
                coordinates = self.check_if_new_coordinate(
                    coordinates=coordinates,
                    start=start,
                    finish=finish,
                    is_part_two=is_part_two,
                    limit_right=limit_right
                )

        # Check solution
        coordinates.sort(key=itemgetter("from"))
        if is_part_two and self.calculate_signals_in_row(coordinates=coordinates) < row_limit:
            for i, x in enumerate(coordinates):
                if len(coordinates) == 1:
                    print(f"len(coords) == 1; {coordinates}")
                    find_x = x["from"] - 1 if x["from"] > 0 else x["to"] + 1
                else:
                    print(f"len(coords) == 2+; {coordinates}")
                    find_x = x["to"] + 1 if x["to"] + 1 == coordinates[i + 1]["from"] - 1 else None
                return {"y": row_that_matters, "x": find_x}
        if not is_part_two:
            return self.calculate_signals_in_row(coordinates=coordinates)

    def check_if_new_coordinate(self, coordinates: List[Dict], start: int, finish: int, is_part_two: bool, limit_right):
        new_coordinates = True
        if is_part_two:
            start = start if start >= 0 else 0
            finish = finish if finish <= limit_right else limit_right
        for x in coordinates:
            if x["from"] <= start and finish <= x["to"]:
                return coordinates
            if x["from"] <= start <= x["to"]:
                x["to"] = finish if x["to"] < finish else x["to"]
                new_coordinates = False
            if x["from"] <= finish <= x["to"]:
                x["from"] = start if start < x["from"] else x["from"]
                new_coordinates = False
        if new_coordinates:
            coordinates.append({"from": start, "to": finish})
        return coordinates

    def calculate_signals_in_row(self, coordinates):
        signal = 0
        for x in coordinates:
            signal += abs(x["from"] - x["to"])
        return signal


@time_me
def problem_solver():
    test = False
    file_string = "test.txt" if test else "day_15.txt"
    row_that_matters = 10 if test else 2000000
    row_limit = 20 if test else 4000000
    sensors = get_tunnel_data(file_string=file_string)
    for sens in sensors:
        sens.calculate_distance()
        sens.calculate_vertices()
    sensors = sorted(sensors, key=attrgetter("x"))
    signal_finder = SignalFinder(sensors=sensors)

    solve_one = signal_finder.find_signals_in_row(row_that_matters=row_that_matters)
    solve_two = signal_finder.check_rows(row_limit=row_limit)

    return solve_one, solve_two


if __name__ == "__main__":
    solution_one, beak_pos = problem_solver()
    solution_two = 4000000 * beak_pos["x"] + beak_pos["y"]
    print(f"Solution one = {solution_one}")
    print(f"Position of Beacon = {beak_pos}; Solution = {solution_two}")

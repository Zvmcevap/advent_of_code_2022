from typing import List
from operator import attrgetter
from string import ascii_lowercase


class Tile:
    def __init__(self, height: int, distance_from_origin: int = None, distance_to_end=None, row=0, column=0):
        self.height = height
        self.row = row
        self.column = column
        self.parent = None
        self.pixel = " "

        # Variable names taken from A* algo
        self.g = distance_from_origin
        self.h = distance_to_end
        self.f = None

    def update_cost(self, parent_g):
        self.g = parent_g + 1
        self.f = self.g + self.h

    def __repr__(self):
        return f"f:{self.f}[{self.row}, {self.column}] h: {self.height}"


class Pathfinder:
    def __init__(self):
        self.tile_map: List[List[Tile]] = []
        self.start = None
        self.finish = None
        self.open_list: List[Tile] = []
        self.closed_list: List[Tile] = []
        self.final_path = []

    def load_map(self):
        self.tile_map.clear()
        with open("day_12.txt") as f:
            letters = list(ascii_lowercase)
            for row, line in enumerate(f.readlines()):
                tile_line = []
                for column, letter in enumerate(line.strip()):
                    if letter == "S":
                        tile = Tile(height=0, distance_from_origin=0, row=row, column=column)
                        self.start = tile
                    elif letter == "E":
                        tile = Tile(height=len(letters) - 1, distance_to_end=0, row=row, column=column)
                        self.finish = tile
                        self.finish.pixel = "X"
                    else:
                        tile = Tile(height=letters.index(letter), row=row, column=column)
                    tile_line.append(tile)
                self.tile_map.append(tile_line)

    def prepare_map_a_star(self):
        for tile_line in self.tile_map:
            for tile in tile_line:
                tile.h = abs(self.finish.row - tile.row) + abs(self.finish.column - tile.column)

    def check_directions(self, ct: Tile, is_djikstra: bool):  # ct reformatted to fit both pathfinding algos
        possible_directions = []
        current_tile = ct
        # Check up
        if current_tile.row > 0:
            up = self.tile_map[current_tile.row - 1][current_tile.column]
            if is_djikstra:
                up, ct = current_tile, up
            if up.height - 1 <= ct.height:
                possible_directions.append(ct) if is_djikstra else possible_directions.append(up)
        # Check down
        if current_tile.row < len(self.tile_map) - 1:
            down = self.tile_map[current_tile.row + 1][current_tile.column]
            if is_djikstra:
                down, ct = current_tile, down
            if down.height - 1 <= ct.height:
                possible_directions.append(ct) if is_djikstra else possible_directions.append(down)
        # Check left
        if current_tile.column > 0:
            left = self.tile_map[current_tile.row][current_tile.column - 1]
            if is_djikstra:
                left, ct = current_tile, left
            if left.height - 1 <= ct.height:
                possible_directions.append(ct) if is_djikstra else possible_directions.append(left)
        # Check right
        if current_tile.column < len(self.tile_map[0]) - 1:
            right = self.tile_map[current_tile.row][current_tile.column + 1]
            if is_djikstra:
                right, ct = current_tile, right
            if right.height - 1 <= ct.height:
                possible_directions.append(ct) if is_djikstra else possible_directions.append(right)

        for tile in possible_directions:
            if tile in self.open_list or tile in self.closed_list:
                if is_djikstra:
                    if tile.g > current_tile.g + 1:
                        tile.g = current_tile.g + 1
                        tile.parent = current_tile
                        if tile in self.closed_list:
                            self.open_list.append(tile)
                            self.closed_list.remove(tile)
                else:
                    if tile.f > current_tile.g + 1 + tile.h:
                        tile.update_cost(current_tile.g)
                        tile.parent = current_tile
                        if tile in self.closed_list:
                            self.open_list.append(tile)
                            self.closed_list.remove(tile)
            else:
                if is_djikstra:
                    tile.g = current_tile.g + 1
                    tile.parent = current_tile
                    self.open_list.append(tile)
                else:
                    tile.update_cost(current_tile.g)
                    tile.parent = current_tile
                    self.open_list.append(tile)

        self.closed_list.append(current_tile)

    def a_star(self):
        self.load_map()
        self.prepare_map_a_star()
        self.final_path.clear()
        self.start.update_cost(-1)
        self.open_list.append(self.start)
        i = 0
        while len(self.open_list) > 0:
            self.open_list.sort(key=attrgetter("f"))
            current_tile = self.open_list[0]
            if current_tile == self.finish:
                print(f"Yay! i = {i}")
                self.make_pixels(ct=self.finish)
                return self.final_path
            self.open_list.remove(current_tile)
            self.check_directions(current_tile, is_djikstra=False)
            i += 1

    def make_pixels(self, ct: Tile):
        # check up
        if not ct.parent:
            return
        if ct.row > 0 and ct.parent == self.tile_map[ct.row - 1][ct.column]:
            ct.parent.pixel = "V"

        # Check down
        if ct.row < len(self.tile_map) - 1 and ct.parent == self.tile_map[ct.row + 1][ct.column]:
            ct.parent.pixel = "^"

        # Check left
        if ct.column > 0 and ct.parent == self.tile_map[ct.row][ct.column - 1]:
            ct.parent.pixel = ">"

        # Check right
        if ct.column < len(self.tile_map[0]) - 1 and ct.parent == self.tile_map[ct.row][ct.column + 1]:
            ct.parent.pixel = "<"

        self.final_path.append(ct)
        self.make_pixels(ct=ct.parent)

    def prepare_map_djikstra(self):
        self.load_map()
        for tile_line in self.tile_map:
            for tile in tile_line:
                tile.g = None
                tile.h = None
                tile.f = None
                tile.parent = None
        self.start = self.finish
        self.start.g = 0
        self.finish = None

    def djikstra(self):
        self.prepare_map_djikstra()
        self.open_list.clear()
        self.closed_list.clear()
        self.final_path.clear()

        self.open_list.append(self.start)
        i = 0
        while len(self.open_list) > 0:
            self.open_list.sort(key=attrgetter("g"))
            current_tile = self.open_list[0]
            if current_tile.height == 0:
                print(f"Yay! i = {i}")
                self.make_pixels(ct=current_tile)
                return self.final_path
            self.open_list.remove(current_tile)
            self.check_directions(current_tile, is_djikstra=True)
            i += 1

    def print_map(self):
        print("|" + "-" * len(self.tile_map[0]) + "|")
        for tile_line in self.tile_map:
            pixel_line = "|"
            for tile in tile_line:
                pixel_line += tile.pixel

            print(pixel_line + "|")
        print("|" + "-" * len(self.tile_map[0]) + "|")

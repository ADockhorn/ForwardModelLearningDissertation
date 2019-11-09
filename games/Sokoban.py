import logging
import copy
import random
import numpy as np
from abstractclasses.AbstractGrid import AbstractGrid
from abstractclasses.AbstractGameState import AbstractGameState, GridGameState

level_tiles = {"EMPTY": '.',
               "BOX": '*',
               "HOLE": 'o',
               "AVATAR": 'A',
               "AVATARONHOLE": 'u',
               "WALL": 'w',
               "BOXIN": '+'}


class SokobanLevel(AbstractGrid):

    def __init__(self, level_no: int = -1):
        self.playerX = -1
        self.playerY = -1

        grid_data, w, h = SokobanLevel.read_level(level_no)
        super().__init__(w, h)

        self.grid = self.set_grid(list(grid_data))

        unique, counts = np.unique(self.grid, return_counts=True)
        counts = {element: count for (element, count) in zip(unique, counts)}

        self.nBoxes = counts[level_tiles["BOX"]] if level_tiles["BOX"] in counts else 0
        self.nBoxesIn = counts[level_tiles["BOXIN"]] if level_tiles["BOXIN"] in counts else 0
        self.totalTicks = 0

    @staticmethod
    def read_level(level_no):
        grid_data = ""
        with open(f"data/Sokoban/levels/level-{level_no}.txt") as file:
            lines = file.readlines()
            dims = lines[1].split(",")
            w = int(dims[0])
            h = int(dims[1])

            for line in lines[2:]:
                grid_data += line[:-1]

        return grid_data, w, h

    def box_score(self):
        self.nBoxes -= 1
        self.nBoxesIn += 1

    def box_score_reverse(self):
        self.nBoxes += 1
        self.nBoxesIn -= 1

    def set_grid(self, level_string):
        player_loc = level_string.index(level_tiles["AVATAR"])
        if player_loc == -1:
            logging.error("ERROR: No player in level")
        else:
            self.playerX = player_loc % self.get_width()
            self.playerY = player_loc // self.get_width()
            level_string[player_loc] = level_tiles["EMPTY"]

        grid = np.array(level_string).reshape(self.get_height(), self.get_width())
        grid = np.transpose(grid, (1, 0))
        self.grid = None

        return grid

    def force_set_grid(self, level_string):
        player_loc = level_string.index(level_tiles["AVATAR"])
        if player_loc == -1:
            player_loc = level_string.index(level_tiles["AVATARONHOLE"])
        if player_loc == -1:
            logging.error("ERROR: No player in level")
        else:
            self.playerX = player_loc % self.get_width()
            self.playerY = player_loc // self.get_width()

        grid = np.array(level_string).reshape(self.get_height(), self.get_width())
        grid = np.transpose(grid, (1, 0))
        self.grid = grid

    def get_cell(self, x, y):
        logging.debug(f"get cell: ({x}, {y})")
        return self.grid[x, y]

    def set_cell(self, x, y, value):
        if self.in_limits(x, y):
            logging.error(f"Can't set cell ({x}, {y}), because it is outside the grid's boundaries")
        else:
            self.grid[x, y] = value

    def get_grid(self):
        return self.grid

    def get_difference(self, other: 'AbstractGrid'):
        # lazily assume same dimensions...
        return sum([x != y for (x, y) in zip(self.grid.flatten(), other.get_grid().flatten())])

    def count(self, char):
        return sum(sum(self.grid == char))

    def get_observation(self):
        obs = self.grid.copy()
        if obs[self.playerX, self.playerY] == level_tiles["HOLE"]:
            obs[self.playerX, self.playerY] = level_tiles["AVATARONHOLE"]
        else:
            obs[self.playerX, self.playerY] = level_tiles["AVATAR"]

        return obs

    def __str__(self) -> str:
        string = ""
        for row in range(self._height):
            row_string = self.grid[:, row].tolist()
            if row == self.playerY:
                if row_string[self.playerX] == level_tiles["HOLE"]:
                    row_string[self.playerX] = level_tiles["AVATARONHOLE"]
                else:
                    row_string[self.playerX] = level_tiles["AVATAR"]
            string += "".join(row_string) + "\n"
        return string + f"Player at: {self.playerX}, {self.playerY}; {self.nBoxesIn} boxes"

    def deep_copy(self):
        # val gc = this.copy()
        # gc.grid = grid.copyOf()
        # gc.playerX = playerX
        # gc.playerY = playerY

        # return gc
        return copy.deepcopy(self)

    def exchange(self, x, y, x2, y2):
        c1 = self.get_cell(x, y)
        c2 = self.get_cell(x2, y2)
        self.set_cell(x, y, c2)
        self.set_cell(x2, y2, c1)


class SokobanConstants:
    NIL = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    ACTIONS = [NIL, UP, RIGHT, DOWN, LEFT]

    ACTION_DESCRIPTION = {NIL: "None",
                          UP: "Up",
                          RIGHT: "Right",
                          DOWN: "Down",
                          LEFT: "Left"}

    images = {".": ['sprites/chamber_wall.png'],  # empty
              "*": ['sprites/block2.png'],
              "o": ['sprites/chamber_wall.png', 'sprites/circleEffect1.png'],
              "A": ['sprites/chamber_wall.png', 'sprites/dwarf1.png'],
              "u": ['sprites/chamber_wall.png', 'sprites/circleEffect1.png', 'sprites/dwarf1.png'],
              "w": ['sprites/wall3.png'],
              "+": ['sprites/block1.png'],
              "x": ['sprites/None.png']
              }


class Sokoban(AbstractGameState, GridGameState):

    totalTicks = 0
    observablePatterns = np.array(['x', '.', '*', 'o', 'A', 'u', 'w', '+', '1', '2', '3', '4'])

    def __init__(self, level_no=-1):
        self._tile_map = SokobanLevel(level_no)
        super().__init__()

    def next(self, action):
        if action == SokobanConstants.UP:
            self.move(0, -1)
        elif action == SokobanConstants.RIGHT:
            self.move(1, 0)
        elif action == SokobanConstants.DOWN:
            self.move(0, 1)
        elif action == SokobanConstants.LEFT:
            self.move(-1, 0)
        elif action == SokobanConstants.NIL:
            pass
        else:
            logging.error(f"INVALID ACTION: {action}")

        self._tick += 1
        Sokoban.totalTicks += 1

    def move(self, x_movement, y_movement):
        next_x = self._tile_map.playerX + x_movement
        next_y = self._tile_map.playerY + y_movement

        # Check self.level limits
        if not self._tile_map.in_limits(next_x, next_y):
            return

        destination_cell = self._tile_map.get_cell(next_x, next_y)

        logging.debug(f"Moving into: {destination_cell}")

        if destination_cell == level_tiles["WALL"]:
            return        # Moves against walls
        elif destination_cell == level_tiles["BOXIN"]:
            # Against a box in a hole. Will move if empty on the other side.
            forward_x = next_x + x_movement
            forward_y = next_y + y_movement

            if not self._tile_map.in_limits(forward_x, forward_y):
                # Pushing against outside of self.level, do nothing.
                return

            forward_cell = self._tile_map.get_cell(forward_x, forward_y)
            if forward_cell == level_tiles["WALL"]:
                return        # Moves against walls
            elif forward_cell == level_tiles["BOXIN"]:
                return        # Moves against box in place (change this for different versions of Sokoban)
            elif forward_cell == level_tiles["BOX"]:
                return        # Push against a BOX, we don't forward the push
            elif forward_cell == level_tiles["EMPTY"]:
                # PROGRESS! (I hope)
                self._tile_map.set_cell(next_x, next_y, level_tiles["HOLE"])
                self._tile_map.set_cell(forward_x, forward_y, level_tiles["BOX"])
                self._tile_map.box_score_reverse()  # Score goes down, box removed from hole
            elif forward_cell == level_tiles["HOLE"]:
                # EUREKA!
                self._tile_map.set_cell(next_x, next_y, level_tiles["HOLE"])
                self._tile_map.set_cell(forward_x, forward_y, level_tiles["BOXIN"])
                # No need to change the score, went from one hole to another
        elif destination_cell == level_tiles["EMPTY"]:
            # Move with no obstacle, ALLOWED
            pass
        elif destination_cell == level_tiles["HOLE"]:
            # Move to a hole, ALLOWED
            pass
        elif destination_cell == level_tiles["BOX"]:
            # GOOD MOVE?
            # Against a box. Will move if empty on the other side.
            forward_x = next_x + x_movement
            forward_y = next_y + y_movement
            if not self._tile_map.in_limits(forward_x, forward_y):
                # Pushing against outside of self.level, do nothing.
                return

            forward_cell = self._tile_map.get_cell(forward_x, forward_y)
            if forward_cell == level_tiles["WALL"]:
                return        # Moves against walls
            elif forward_cell == level_tiles["BOXIN"]:
                return        # Moves against box in place (change this for different versions of Sokoban)
            elif forward_cell == level_tiles["BOX"]:
                return        # Push against a BOX, we don't forward the push
            elif forward_cell == level_tiles["EMPTY"]:
                # PROGRESS! (I hope)
                self._tile_map.exchange(next_x, next_y, forward_x, forward_y)
            elif forward_cell == level_tiles["HOLE"]:
                # EUREKA!
                self._tile_map.set_cell(next_x, next_y, level_tiles["EMPTY"])
                self._tile_map.set_cell(forward_x, forward_y, level_tiles["BOXIN"])
                self._tile_map.box_score()

        self._tile_map.playerX = next_x
        self._tile_map.playerY = next_y

    def get_actions(self):
        return SokobanConstants.ACTIONS

    @property
    def get_random_action(self):
        return random.choice([SokobanConstants.DOWN, SokobanConstants.UP,
                              SokobanConstants.LEFT, SokobanConstants.RIGHT])

    def get_score(self):
        return self._tile_map.nBoxesIn

    def is_terminal(self):
        if self._tick == 100:
            return True
        return self._tile_map.nBoxes == 0

    def get_tile_map(self) -> np.ndarray:
        return self._tile_map.get_observation()

    def get_width(self) -> int:
        return self._tile_map.get_width()

    def get_height(self) -> int:
        return self._tile_map.get_height()

    @staticmethod
    def get_total_ticks():
        return Sokoban.totalTicks

    @staticmethod
    def reset_total_ticks():
        Sokoban.totalTicks = 0

    @staticmethod
    def n_actions():
        return len(SokobanConstants.ACTIONS)

    def deep_copy(self):
        return copy.deepcopy(self)

    def __str__(self):
        return self._tile_map.__str__() + "\n" + \
               (f"Score: {self.get_score()}; terminal: {self.is_terminal()}; "
                f"Player at ({self._tile_map.playerX}, {self._tile_map.playerY})")


if __name__ == "__main__":
    FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
    logging.basicConfig(format=FORMAT)

    sokoban = Sokoban()
    # THIS FAILS TO SOLVE THE LEVEL
    print(sokoban)
    sokoban.next(SokobanConstants.RIGHT)
    print(sokoban)
    sokoban.next(SokobanConstants.UP)
    sokoban.next(SokobanConstants.RIGHT)
    sokoban.next(SokobanConstants.RIGHT)
    sokoban.next(SokobanConstants.DOWN)
    sokoban.next(SokobanConstants.DOWN)
    sokoban.next(SokobanConstants.DOWN)
    sokoban.next(SokobanConstants.LEFT)
    print(sokoban)
    sokoban.next(SokobanConstants.UP)
    print(sokoban)

    sokoban = Sokoban()
    # THIS SOLVES THE LEVEL
    sokoban.next(SokobanConstants.DOWN)
    sokoban.next(SokobanConstants.DOWN)
    print(sokoban)
    sokoban.next(SokobanConstants.UP)
    sokoban.next(SokobanConstants.UP)
    sokoban.next(SokobanConstants.RIGHT)
    sokoban.next(SokobanConstants.RIGHT)
    sokoban.next(SokobanConstants.DOWN)
    sokoban.next(SokobanConstants.DOWN)
    print(sokoban)
    sokoban.next(SokobanConstants.UP)
    sokoban.next(SokobanConstants.LEFT)
    print(sokoban)

    import time

    print("speed test 1: load the level 100 times")

    start = time.time()
    for i in range(100):
        sokoban = Sokoban(-1)
    end = time.time()
    print(f"loading the level 100 times: {end-start}")

    sokoban = Sokoban(-1)

    print("speed test 1: do 1 million moves")
    start = time.time()
    for i in range(1000000):
        sokoban.next(random.choice(SokobanConstants.ACTIONS))
    end = time.time()
    print(f"doing {sokoban.totalTicks//(end-start)} moves per s")

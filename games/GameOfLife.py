import logging
import copy
import random
import numpy as np
from abstractclasses.AbstractGrid import AbstractGrid
from abstractclasses.AbstractGameState import AbstractGameState, GridGameState
from typing import Tuple
from scipy.signal import convolve2d
from itertools import product


level_tiles = {"ALIVE": 1,
               "DEAD": 0}


class GameOfLifeLevel(AbstractGrid):

    def __init__(self, grid_size: Tuple[int, int] = (10, 10)):
        super().__init__(grid_size[0], grid_size[1])
        self.score = 0
        self.grid = None
        self.set_grid((np.random.rand(*grid_size) > 0.5) * 1)
        self.nr_of_cells = self.get_width() * self.get_height()

    def set_grid(self, grid_data: np.ndarray):
        self.grid = grid_data
        self.score = np.sum(self.grid)
        return self.grid

    def force_set_grid(self, grid_data: np.ndarray):
        return self.set_grid(grid_data)

    def get_cell(self, x, y):
        logging.debug(f"get cell: ({x}, {y})")
        return self.grid[x, y]

    def set_cell(self, x, y, value):
        if x < 0 or y < 0 or x >= self._width or y >= self._height:
            logging.error(f"Can't set cell ({x}, {y}), because it is outside the grid's boundaries")
        elif value not in {0, 1}:
            logging.error(f"Can't set cell ({x}, {y}), because value {value} is not 0 or 1")
        else:
            self.grid[x, y] = value

    def get_grid(self):
        return self.grid

    def get_difference(self, other: 'AbstractGrid'):
        # lazily assume same dimensions...
        return sum([x != y for (x, y) in zip(self.grid.flatten(), other.get_grid().flatten())])

    def count(self, val):
        if val not in (0,1):
            logging.error(f"The value {val} if not 0 or 1")
        return self.score if val == 0 else self.nr_of_cells - self.score

    def get_observation(self):
        obs = self.grid.copy()
        return obs

    def __str__(self) -> str:
        return self.grid.__repr__()

    def deep_copy(self):
        return copy.deepcopy(self)


class GameOfLifeConstants:
    images = {1: ['sprites/alive_cell.png'],  # empty
              0: []}


class GameOfLife(AbstractGameState, GridGameState):

    totalTicks = 0
    observablePatterns = np.array([0, 1])

    def __init__(self, grid_size=(10, 10)):
        self._tile_map = GameOfLifeLevel(grid_size)
        self.actions = list(product(range(self._tile_map.get_width()), range(self._tile_map.get_height())))
        self.get_score()

        super().__init__()

    def next(self, action=(-1, -1)):
        self._tick += 1

        X = self._tile_map.get_grid()
        if self._tile_map.in_limits(*action):
            self._tile_map.set_cell(*action, 1 - self._tile_map.get_cell(*action))

        # thanks to: https://jakevdp.github.io/blog/2013/08/07/conways-game-of-life/
        neighbors_count = convolve2d(X, np.ones((3, 3)), mode='same', boundary='wrap') - X
        self._tile_map.set_grid((neighbors_count == 3) | (X & (neighbors_count == 2)))

        GameOfLife.totalTicks += 1

    def get_actions(self):
        return self.actions

    def get_score(self):
        return self._tile_map.score

    def is_terminal(self):
        return self._tile_map.score == 0

    def n_ticks(self):
        return self._tick

    def get_tile_map(self) -> np.ndarray:
        return self._tile_map.get_observation()

    def get_width(self) -> int:
        return self._tile_map.get_width()

    def get_height(self) -> int:
        return self._tile_map.get_height()

    @staticmethod
    def get_total_ticks():
        return GameOfLife.totalTicks

    @staticmethod
    def reset_total_ticks():
        GameOfLife.totalTicks = 0

    def n_actions(self):
        return len(self.actions)

    def deep_copy(self):
        return copy.deepcopy(self)

    def __str__(self):
        return self._tile_map.__str__() + "\n" + \
               f"Score: {self.get_score()}; terminal: {self.is_terminal()}"


if __name__ == "__main__":
    FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
    logging.basicConfig(format=FORMAT)

    gameoflife = GameOfLife(grid_size=(4, 4))

    import time

    print("speed test 1: do 1 million moves")
    start = time.time()
    for i in range(1000000):
        gameoflife.next(random.choice(gameoflife.actions))
    end = time.time()
    print(f"doing {gameoflife.totalTicks//(end-start)} moves per s")

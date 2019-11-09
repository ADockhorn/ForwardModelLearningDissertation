from abc import ABC, abstractmethod
from abstractclasses.AbstractGameState import GridGameState
import numpy as np
from typing import Union


class AbstractNeighborhoodPattern(ABC):

    def __init__(self, span):
        super().__init__()
        self._span = span
        self._pattern_mask = self.get_mask()
        self._ext_pattern_mask = np.transpose(np.array([self._pattern_mask, self._pattern_mask, self._pattern_mask]), (1,2,0))

        self._pattern_elements = np.sum(self._pattern_mask)
        self._width = span*2+1
        self._height = span*2+1

    @abstractmethod
    def get_mask(self):
        pass

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_num_elements(self):
        return self._pattern_elements

    def get_pattern(self, game_state_grid: np.ndarray, x: int, y: int):
        ext_game_state_grid = np.pad(game_state_grid, self._span, "constant", constant_values="x")
        return self.get_pattern_of_extended_game_state(ext_game_state_grid, x, y)

    def get_pattern_of_extended_game_state(self, ext_game_state_grid: np.ndarray, x: int, y: int, include_z: bool = False):
        if not include_z:
            return ext_game_state_grid[self._span + x - self._span: self._span + x + self._span + 1,
                                       self._span + y - self._span: self._span + y + self._span + 1][self._pattern_mask]
        else:
            return ext_game_state_grid[self._span + x - self._span: self._span + x + self._span + 1,
                                       self._span + y - self._span: self._span + y + self._span + 1, :][self._ext_pattern_mask].flatten()

    def pattern_to_img(self, pattern):
        image = np.zeros((self._span*2+1, self._span*2+1, 3), dtype=np.uint8)
        image[self._ext_pattern_mask] = pattern
        return image

    def get_patterns_for_position_list(self, game_state_grid: np.ndarray, positions):
        if len(game_state_grid.shape) == 3:  # image array
            ext_game_state_grid = np.pad(game_state_grid, [(self._span, self._span), (self._span, self._span), (0, 0)],
                                         "constant", constant_values=0)
            patterns = np.zeros((len(positions), self._pattern_elements*3), dtype=ext_game_state_grid.dtype)
            for idx, (x, y) in enumerate(positions):
                patterns[idx, :] = self.get_pattern_of_extended_game_state(ext_game_state_grid, x, y, True)
        else:
            ext_game_state_grid = np.pad(game_state_grid, self._span, "constant", constant_values="x")
            patterns = np.zeros((len(positions), self._pattern_elements), dtype=ext_game_state_grid.dtype)
            for idx, (x, y) in enumerate(positions):
                patterns[idx, :] = self.get_pattern_of_extended_game_state(ext_game_state_grid, x, y)
        return patterns

    def get_all_patterns(self, game_state: Union[GridGameState, np.ndarray], action=None,
                         next_game_state: Union[GridGameState, np.ndarray, None] = None):
        """
        returns the square-neighborhood-environment
        second to last column is the action
        last column is the outcome
        """
        if isinstance(game_state, GridGameState):
            game_state_grid = game_state.get_tile_map()
        else:
            game_state_grid = game_state
        if next_game_state is not None and isinstance(game_state, GridGameState):
            target = next_game_state.get_tile_map()
        else:
            target = next_game_state

        patterns = self.get_patterns_for_position_list(game_state_grid, [(x, y) for x in range(game_state_grid.shape[0])
                                                                         for y in range(game_state_grid.shape[1])])

        if action is not None and next_game_state is not None:
            # one row per cell, one column per element in the neighborhood + action + target
            train_data = np.zeros((game_state_grid.shape[1] * game_state_grid.shape[0],
                                   patterns.shape[1] + 2), dtype=game_state_grid.dtype)
            train_data[:, :-2] = patterns
            train_data[:, -2] = action
            train_data[:, -1] = target.flatten()
        elif action is not None or next_game_state is not None:
            # one row per cell, one column per element in the neighborhood + (action or target)
            train_data = np.zeros((game_state_grid.shape[1] * game_state_grid.shape[0],
                                   patterns.shape[1] + 1), dtype=game_state_grid.dtype)
            train_data[:, :-1] = patterns
            if action is not None:
                train_data[:, -1] = action
            else:
                train_data[:, -1] = target.flatten()
        else:
            # one row per cell, one column per element in the neighborhood + action
            return patterns

        return train_data


class SquareNeighborhoodPattern(AbstractNeighborhoodPattern):

    def __init__(self, span):
        super().__init__(span)
        self._span = span

    def get_mask(self):
        return np.array([[True for _ in range(self._span*2+1)] for _ in range(self._span*2+1)])

    """
    def get_pattern_of_extended_game_state(self, ext_game_state_grid: np.ndarray, x: int, y: int):
        return ext_game_state_grid[self._span + x - self._span: self._span + x + self._span + 1,
                                   self._span + y - self._span: self._span + y + self._span + 1].flatten()
    """


class CrossNeighborhoodPattern(AbstractNeighborhoodPattern):

    def __init__(self, span):
        super().__init__(span)

    def get_mask(self):
        return np.array([[True if x == self._span or y == self._span else False
                          for x in range(self._span * 2+1)] for y in range(self._span * 2 + 1)])


class GeneralizedNeighborhoodPattern(AbstractNeighborhoodPattern):

    def __init__(self, span, k=2):
        self.k = k
        super().__init__(span)

    def get_mask(self):
        return np.array([[True if x == self._span or y == self._span or
                        ((abs(self._span-x)/self._span)**self.k +
                         (abs(self._span-y)/self._span)**self.k)**(1/self.k) <= 1
                          else False for x in range(self._span*2+1)] for y in range(self._span*2+1)])


if __name__ == "__main__":
    # create GridGame objects
    from games.Sokoban import Sokoban, SokobanConstants
    sokoban = Sokoban()
    sokoban.next(SokobanConstants.UP)
    sokoban2 = sokoban.deep_copy()
    sokoban2.next(SokobanConstants.UP)

    # generate patterns
    test_span = 2
    pattern_extractor = GeneralizedNeighborhoodPattern(test_span, k=0.1)

    print("extracted patterns:")
    print(pattern_extractor.get_all_patterns(sokoban, action=None, next_game_state=sokoban2))

    # visualize patterns
    from games.TileMapVisualizer import TileMapVisualizer
    import matplotlib.pyplot as plt

    tsv = TileMapVisualizer(SokobanConstants.images, 24)
    tsv.visualize_game_state(sokoban)
    tsv.visualize_game_state(sokoban2)
    fig, ax = tsv.visualize_all_pattern(sokoban, pattern_extractor)
    plt.show()

    pattern_extractor2 = GeneralizedNeighborhoodPattern(0, k=0.1)
    fig, ax = tsv.visualize_all_pattern(sokoban2, pattern_extractor2)
    plt.show()

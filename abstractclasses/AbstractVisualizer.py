from abc import ABC, abstractmethod
from abstractclasses.AbstractGameState import AbstractGameState


class AbstractGameStateVisualizer(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def visualize_game_state(self, game_state: AbstractGameState, axis=None):
        pass


class AbstractTileMapVisualizer(AbstractGameStateVisualizer):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def visualize_tile_map(self, game_state: AbstractGameState, axis=None):
        pass

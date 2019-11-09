from abc import ABC, abstractmethod


class AbstractGrid(ABC):

    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        super().__init__()

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    @abstractmethod
    def get_grid(self):
        pass

    @abstractmethod
    def set_grid(self, grid_data):
        pass

    @abstractmethod
    def force_set_grid(self, grid_data):
        pass

    @abstractmethod
    def get_observation(self):
        pass

    @abstractmethod
    def get_cell(self, x: int, y: int):
        pass

    @abstractmethod
    def set_cell(self, x: int, y: int, cell):
        pass

    @abstractmethod
    def get_difference(self, other: 'AbstractGrid'):
        pass

    @abstractmethod
    def deep_copy(self):
        pass

    def in_limits(self, x, y):
        return not (x < 0 or x >= self._width or y < 0 or y > self._height)

    @abstractmethod
    def __str__(self) -> str:
        pass

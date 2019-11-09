from abc import ABC, abstractmethod
from abstractclasses.AbstractGameState import AbstractGameState


class AbstractForwardModel(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def fit(self):
        pass

    @abstractmethod
    def predict(self, game_state: AbstractGameState, action=None):
        pass

    @abstractmethod
    def predict_n_steps(self, game_state: AbstractGameState, action_list):
        pass

    @abstractmethod
    def add_transition(self, previous_game_state: AbstractGameState, action, game_state: AbstractGameState):
        pass

    @abstractmethod
    def get_data_set(self):
        pass

    @abstractmethod
    def is_trained(self):
        pass

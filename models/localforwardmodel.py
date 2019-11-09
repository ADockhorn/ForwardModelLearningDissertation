from abstractclasses.AbstractForwardModel import AbstractForwardModel
from abstractclasses.AbstractGameState import AbstractGameState, GridGameState
from abstractclasses.AbstractNeighborhoodPattern import AbstractNeighborhoodPattern
import numpy as np
from sklearn import preprocessing
from typing import Any, Union, Dict, List


class LocalForwardModel(AbstractForwardModel):

    def __init__(self, classifier, pattern_extractor: AbstractNeighborhoodPattern, possibleObservations):
        super().__init__()
        self._pattern_extractor = pattern_extractor
        self._classifier = classifier
        self._is_trained = False
        self._use_unique_values = True

        if possibleObservations is not None:
            self.possibleObservations = possibleObservations
            self.featureEncoder = preprocessing.LabelEncoder()
            self.featureEncoder.fit(self.possibleObservations)
            self._data_set = np.chararray((0, self._pattern_extractor.get_num_elements() + 2))
        else:
            self._data_set = np.zeros((0, self._pattern_extractor.get_num_elements()*3 + 1))

    def fit(self):
        if self._data_set.dtype != np.dtype('int64'):
            transformed = self.featureEncoder.transform(self._data_set.flatten())
            transformed = transformed.reshape(self._data_set.shape)
            self._classifier.fit(transformed[:, :-1], transformed[:, -1])
        else:
            self._classifier.fit(self._data_set[:, :-1], self._data_set[:, -1])
        self._is_trained = True
        pass

    def predict(self, game_state: Union[GridGameState and AbstractGameState, np.ndarray],
                action=None) -> Union[np.ndarray, Dict[Any, np.ndarray]]:
        if action is None:
            assert type(game_state) is not np.ndarray, "action cannot be deduced in case game_state " \
                                                       "is not an AbstractGameState object"

            results = {}
            for action in game_state.get_actions():
                results[action] = self._predict_action(game_state, action)
            return results
        else:
            return self._predict_action(game_state, action)

    def _predict_action(self, game_state: GridGameState, action) -> np.ndarray:
        testing_data = self._pattern_extractor.get_all_patterns(game_state, action)

        if testing_data.dtype == np.dtype('int64'):
            return self.predict(testing_data)
        else:
            transformed = self.featureEncoder.transform(testing_data.flatten())
            transformed = transformed.reshape(testing_data.shape)

            prediction = self._classifier.predict(transformed)

            return self.featureEncoder.inverse_transform(prediction)

    def predict_n_steps(self, game_state: Union[GridGameState and AbstractGameState, np.ndarray],
                        action_list) -> List[np.ndarray]:
        if isinstance(game_state, GridGameState):
            observation = game_state.get_tile_map()
        else:
            observation = game_state
        results = []
        for action in action_list:
            observation = self._predict_action(observation, action).reshape(observation.shape)
            results.append(observation)
        return results

    def add_transition(self, previous_game_state: Union[GridGameState, np.ndarray], action,
                       game_state: Union[GridGameState, np.ndarray, None]):
        new_train_data = self._pattern_extractor.get_all_patterns(previous_game_state, action, game_state)
        if self._use_unique_values:
            unique = np.unique(new_train_data, axis=0)
            self._data_set = np.unique(np.concatenate((unique, self._data_set)), axis=0)
        else:
            self._data_set = np.concatenate((new_train_data, self._data_set))

    def get_data_set(self):
        return self._data_set

    def get_model(self):
        return self._classifier

    def get_pattern_extractor(self):
        return self._pattern_extractor

    def is_trained(self):
        return self._is_trained


if __name__ == "__main__":
    pass

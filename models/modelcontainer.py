from abstractclasses.AbstractForwardModel import AbstractForwardModel
from abstractclasses.AbstractGameState import AbstractGameState, GridGameState
import numpy as np
from sklearn import preprocessing
from typing import Union, List


class ModelContainer(AbstractForwardModel):

    def __init__(self, classifier_list, pattern_extractor_list, observations):
        super().__init__()
        self._pattern_extractors = pattern_extractor_list
        self._classifier_list = classifier_list

        self._is_trained = False
        self._use_unique_values = True
        self._data_set = [np.chararray((0, pe.get_num_elements() + 2)) for pe in pattern_extractor_list]

        self.possibleObservations = observations
        self.featureEncoder = preprocessing.LabelEncoder()
        self.featureEncoder.fit(self.possibleObservations)

    def fit(self):
        if self._data_set.dtype != np.dtype('int64'):
            transformed = self.featureEncoder.transform(self._data_set.flatten())
            transformed = transformed.reshape(self._data_set.shape)
            for classifier in self._classifier_list:
                classifier.fit(transformed[:, :-1], transformed[:, -1])
        else:
            for classifier in self._classifier_list:
                classifier.fit(self._data_set[:, :-1], self._data_set[:, -1])
        self._is_trained = True
        pass

    def predict(self, game_state: Union[AbstractGameState, GridGameState], action=None):
        if action is None:
            results = {}
            for action in game_state.get_actions():
                results[action] = self._predict_action(game_state, action)
            return results
        else:
            return self._predict_action(game_state, action)

    def _predict_action(self, game_state: GridGameState, action) -> List[np.ndarray]:
        predictions = []

        testing_data = self._pattern_extractor.get_all_patterns(game_state, action)

        if testing_data.dtype == np.dtype('int64'):
            return self.predict(testing_data)
        else:
            transformed = self.featureEncoder.transform(testing_data.flatten())
            transformed = transformed.reshape(testing_data.shape)

            for classifier in self._classifier_list:
                prediction = classifier.predict(transformed)
                predictions.append(self.featureEncoder.inverse_transform(prediction))
        return predictions

    def predict_n_steps(self, game_state: AbstractGameState, action_list):
        raise Exception()

    def add_transition(self, previous_game_state: GridGameState, action, game_state: GridGameState):
        for idx, pe in enumerate(self._pattern_extractors):
            new_train_data = pe.get_all_patterns(previous_game_state, action, game_state)
            if self._use_unique_values:
                unique = np.unique(new_train_data, axis=0)
                self._data_set[idx] = np.unique(np.concatenate((unique, self._data_set[idx])), axis=0)
            else:
                self._data_set[idx] = np.concatenate((new_train_data, self._data_set[idx]))

    def get_data_set(self):
        return self._data_set

    def get_models(self):
        return self._classifier_list

    def get_pattern_extractor(self):
        return self._pattern_extractors

    def is_trained(self):
        return self._is_trained


if __name__ == "__main__":
    pass

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
import numpy as np


class GlobalScoreModel:
    def __init__(self, possible_observations):
        self.model = None

        self._data_set = np.zeros((0, len(possible_observations) * 4 + 1))
        # first n elements = how often do obj exist in observation
        # second n elements = how often is the obj unchanged
        # third n elements = how often did cells become of type obj
        # fourth n elements = how often did cells become something else when previously being of type obj

        self.possibleObservations = {obj: index for index, obj in enumerate(possible_observations)}
        self.num_elements = len(self.possibleObservations)

    def fit(self):
        # self.model = LinearRegression().fit(self._data_set[:, :-1], self._data_set[:, -1])
        self.model = DecisionTreeRegressor().fit(self._data_set[:, :-1], self._data_set[:, -1])

    def add_transition(self, prev_obs, obs, score):
        self._data_set = np.unique(np.concatenate((self.create_vector(prev_obs, obs, score), self._data_set)), axis=0)

    def create_vector(self, prev_obs, obs, score=None):
        if score is not None:
            new_data = np.zeros((1, self.num_elements * 4 + 1))
            new_data[:, -1] = score
        else:
            new_data = np.zeros((1, self.num_elements * 4))

        for ind, obj in enumerate(self.possibleObservations):
            new_data[0, ind] = np.sum(obs == obj)

        for prev, now in zip(prev_obs.flatten(), obs.flatten()):
            if prev == now:
                new_data[0, self.num_elements + self.possibleObservations[prev]] += 1
            else:
                new_data[0, self.num_elements * 2 + self.possibleObservations[now]] += 1
                new_data[0, self.num_elements * 3 + self.possibleObservations[prev]] -= 1

        return new_data

    def predict(self, prev_obs, obs):
        if self.model is not None:
            return self.model.predict(self.create_vector(prev_obs, obs))[0]
        else:
            raise AssertionError("score model not trained yet. first call fit()")

    def get_dataset(self):
        return self._data_set

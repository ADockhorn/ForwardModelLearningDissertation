import numpy as np
from sklearn import preprocessing
from utils.numpy_utilities import is_numeric
import logging


class ForwardModel:

    def __init__(self, classifier, possibleObservations = None):
        self.trained = False
        self.classifier = classifier

        self.possibleObservations = np.array(['x', '.', '*', 'o', 'A', 'u', 'w', '+', '1', '2', '3', '4'])
        self.featureEncoder = preprocessing.LabelEncoder()
        self.featureEncoder.fit(self.possibleObservations)
        pass

    def fit(self, training_data: np.array, training_labels=None):
        if training_data.dtype != np.dtype('int64'):
            transformed = self.featureEncoder.transform(training_data.flatten())
            transformed = transformed.reshape(training_data.shape)
            self.classifier.fit(transformed[:, :-1], transformed[:, -1])
        else:
            self.classifier.fit(training_data[:, :-1], training_data[:, -1])
#        logging.debug(f"tree trained: nr of leaves = {self.classifier.get_n_leaves()},
        #        depth = {self.classifier.get_depth()}")
        self.trained = True

    def predict(self, testing_data: np.array):
        assert isinstance(testing_data, np.ndarray), "testing_data is not a numpy array"

        if testing_data.dtype == np.dtype('int64'):
            return self.predict(testing_data)
        else:
            transformed = self.featureEncoder.transform(testing_data.flatten())
            transformed = transformed.reshape(testing_data.shape)

            prediction = self.classifier.predict(transformed)

            return self.featureEncoder.inverse_transform(prediction)

    def predict_n_steps(self, start_state, actions, steps):
        assert isinstance(steps, int) and steps >= 1, "steps needs to be a positive integer"

        predicted_observation = self.classifier.predict(testing_data)
        for i in range(steps):
            predicted_observation = self.classifier.predict(observation)
            observation = predicted_observation

    def add_transitions(self):
        pass

    def get_transitions(self):
        pass

    def get_model(self):
        pass


if __name__ == "__main__":
    from sklearn.neighbors import NearestNeighbors
    ForwardModel(NearestNeighbors(n_neighbors=2, algorithm='ball_tree'))

    from sklearn.neighbors import KNeighborsClassifier

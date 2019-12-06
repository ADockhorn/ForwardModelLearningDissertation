from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

from sklearn import preprocessing
from sklearn.model_selection import cross_validate
from sklearn.model_selection import GridSearchCV

from agents.RandomAgent import RandomAgent
from games.GVGAIConstants import get_object_dict, get_images
from games.gvgai_environment import GVGAIEnvironment
from tqdm import trange
from models.modelcontainer import ModelContainer
from abstractclasses.AbstractNeighborhoodPattern import *
from gym import envs
from tqdm import tqdm

import logging
import numpy as np
import pickle
import os


def store_data_sets(game_name, data_sets):
    with open(f"results/{game_name}/patterns_data_set.txt", "wb") as f:
        pickle.dump(data_sets, f)

def store_grid_search_results(game_name, results):
    with open(f"results/{game_name}/grid_search.txt", "wb") as f:
        pickle.dump(results, f)

def load_data_sets(game_name):
    with open(f"results/{game_name}/patterns_data_set.txt", "rb") as f:
        return pickle.load(f)


def create_data_sets(game_name, max_ticks=200, levels=(0, 1, 2, 3, 4), repetitions=5):
    agent = RandomAgent()
    fm = ModelContainer([], [CrossNeighborhoodPattern(i) for i in range(1, 4)] +
                        [SquareNeighborhoodPattern(i) for i in range(1, 4)] +
                        [GeneralizedNeighborhoodPattern(i, 1) for i in range(1, 4)],
                        observations=np.append(np.array(list(get_object_dict(game_name).values())),
                                               np.array(["0", "1", "2", "3", "4", "5", "x"])))

    for level in levels:
        for rep in range(repetitions):

            game = GVGAIEnvironment(game_name, level, 0)
            observation, total_score, _, sso = game.reset()
            previous_observation = None

            for tick in trange(max_ticks, desc="ticks", ncols=100):
                current_action = agent.get_next_action(observation, game.get_actions())
                observation, _, is_over, _ = game.step(current_action)
                if is_over:
                    break
                if previous_observation is not None:
                    fm.add_transition(previous_observation, current_action, observation.get_grid())
                previous_observation = observation.get_grid()

    store_data_sets(game_name, fm.get_data_set())
    return fm.get_data_set()


def measure_accuracy():
    pass


def measure_corrected_accuracy():
    pass


def record_data(game_name):
    if not os.path.exists(f"results/{game_name}/"):
        os.mkdir(f"results/{game_name}/")

    if os.path.exists(f"results/{game_name}/lock.txt"):
        return None

    data = None
    if os.path.exists(f"results/{game_name}/patterns_data_set.txt"):
        data = load_data_sets(game_name)
    else:
        with open(f"results/{game_name}/lock.txt", "wb") as f:
            pickle.dump([0], f)
        data = create_data_sets(game_name)

    if os.path.exists(f"results/{game_name}/lock.txt"):
        os.remove(f"results/{game_name}/lock.txt")
    return data


if __name__ == "__main__":
    os.chdir("/".join(os.getcwd().split("/")[:-1]))

    classifiers_names = ["Nearest Neighbors", 
                         #"Linear SVM", "RBF SVM",
                         "Decision Tree", "Random Forest", "AdaBoost",
                         "Naive Bayes"]

    classifiers = [
        KNeighborsClassifier(),
        #SVC(),
        #SVC(),
        DecisionTreeClassifier(),
        RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
        AdaBoostClassifier(),
        GaussianNB()]

    parameters = [
        {"n_neighbors": [1, 5, 10]},
        #{'C': [1, 10, 100], 'gamma': [0.001, 0.0001], 'kernel': ['linear']},
        #{'C': [1, 10, 100], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
        {"max_depth": [1, 5, 10, None], "splitter": ["best", "random"]},
        {"max_depth": [1, 5, 10, None], "n_estimators": [5, 10, 100]},
        {"n_estimators": [5, 10, 100]},
        {"priors": [None]}
    ]

    grid_based_games = []
    with open("data/GVGAI/grid-based-games.txt", "r") as file:  # Use file to refer to the file object
        for s in file.readlines():
            if len(s) > 1:
                grid_based_games.append(s[:-1])

    for game_name in grid_based_games:
        results = {}

        data_sets = record_data(game_name)
        if data_sets is None:
            continue
        if os.path.exists(f"results/{game_name}/grid_search.txt"):
            with open(f"results/{game_name}/grid_search.txt", "rb") as f:
                results = pickle.load(f)

        with open(f"results/{game_name}/lock.txt", "wb") as f:
            pickle.dump([0], f)

        print(game_name)
        for cla_name, cla, parameter_grid in tqdm(zip(classifiers_names, classifiers, parameters), ncols=100):
            if cla_name not in results:
                results[cla_name] = {"grid_search": [], "best_parameters": None, "best_mean_accuracy": 0,
                                     "best_cv_values": None, "best_data_set": None}
            print(cla_name)

            for i, (data_set_name, data_set) in enumerate(zip([f"Cross_{i}" for i in range(1, 4)] +
                    [f"Square_{i}" for i in range(1, 4)] +
                    [f"Diamond_{i}" for i in range(1, 4)], data_sets)):
                if len(results[cla_name]["grid_search"]) >= i+1:
                    continue
                else:
                    unique_values = np.unique(data_set)
                    preprocessor = preprocessing.LabelEncoder()
                    preprocessor.fit(unique_values)
                    transformed = preprocessor.transform(data_set.flatten())
                    transformed = transformed.reshape(data_set.shape)
                    np.random.shuffle(transformed)

                    clf = GridSearchCV(cla, parameter_grid, cv=10, n_jobs=-1)
                    clf.fit(transformed[:, :-1], transformed[:, -1])
                    results[cla_name]["grid_search"].append(clf.cv_results_)

                    best_idx = np.argmax(clf.cv_results_["mean_test_score"])
                    best_parameters = clf.cv_results_["params"][best_idx]
                    best_mean_accuracy = clf.cv_results_["mean_test_score"][best_idx]

                    if best_mean_accuracy > results[cla_name]["best_mean_accuracy"]:
                        results[cla_name]["best_mean_accuracy"] = best_mean_accuracy
                        results[cla_name]["best_parameters"] = best_parameters
                        results[cla_name]["best_data_set"] = data_set_name

                        stats = np.array([clf.cv_results_[f'split{x}_test_score'] for x in range(10)])
                        results[cla_name]["best_cv_values"] = stats[:, best_idx]

                    store_grid_search_results(game_name, results)

        if os.path.exists(f"results/{game_name}/lock.txt"):
            os.remove(f"results/{game_name}/lock.txt")

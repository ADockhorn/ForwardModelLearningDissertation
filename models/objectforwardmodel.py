import gym
import gym_gvgai
import matplotlib.pyplot as plt
import numpy as np

from sklearn.tree import DecisionTreeClassifier

from abstractclasses.AbstractNeighborhoodPattern import SquareNeighborhoodPattern
from models.globalscoremodel import GlobalScoreModel
from models.localforwardmodel import LocalForwardModel
from games.GVGAIConstants import get_images, get_object_dict
from games.gvgai_environment import GVGAIEnvironment
from agents.RHEA import RHEAAgent
from agents.BFSAgent import BFSAgent
from agents.RandomAgent import RandomAgent
from matplotlib import animation
from gym import envs
from games.gvgai_environment import train_model
import os
import pickle
from agents.AgentParameters import *
import logging
from tqdm import tqdm, trange
import random
from typing import List
from sklearn.tree import DecisionTreeClassifier


class ObjectGameState:
    def __init__(self, next_state_lists, width, height):
        self.state = next_state_lists
        self.width = width
        self.height = height


class ObjectBasedForwardModel:
    def __init__(self, classifier, object_types=None):
        self.trained = False
        self.base_classifier = classifier
        self.classifiers = dict()
        self.training_data = dict()
        self.avatar_itypes = set()

    def fit(self):
        for itype in self.training_data:
            if len(self.training_data[itype]) > 0:
                if itype in self.classifiers:
                    # update classifiers
                    if itype in self.avatar_itypes:
                        self.classifiers[itype][0].fit(self.training_data[itype][:, :-4], self.training_data[itype][:, -4])
                        self.classifiers[itype][1].fit(self.training_data[itype][:, :-4], self.training_data[itype][:, -3])
                        self.classifiers[itype][2].fit(self.training_data[itype][:, :-4], self.training_data[itype][:, -2])
                        self.classifiers[itype][3].fit(self.training_data[itype][:, :-4], self.training_data[itype][:, -1])
                    else:
                        self.classifiers[itype][0].fit(self.training_data[itype][:, :-3], self.training_data[itype][:, -3])
                        self.classifiers[itype][1].fit(self.training_data[itype][:, :-3], self.training_data[itype][:, -2])
                        self.classifiers[itype][2].fit(self.training_data[itype][:, :-3], self.training_data[itype][:, -1])
                    pass
                else:
                    # create new classifiers
                    if itype in self.avatar_itypes:
                        itype_pred = self.base_classifier()
                        x_pred = self.base_classifier()
                        y_pred = self.base_classifier()
                        death_pred = self.base_classifier()

                        itype_pred.fit(self.training_data[itype][:, :-4], self.training_data[itype][:, -4])
                        x_pred.fit(self.training_data[itype][:, :-4], self.training_data[itype][:, -3])
                        y_pred.fit(self.training_data[itype][:, :-4], self.training_data[itype][:, -2])
                        death_pred.fit(self.training_data[itype][:, :-4], self.training_data[itype][:, -1])

                        self.classifiers[itype] = [itype_pred, x_pred, y_pred, death_pred]
                    else:
                        x_pred = self.base_classifier()
                        y_pred = self.base_classifier()
                        death_pred = self.base_classifier()

                        x_pred.fit(self.training_data[itype][:, :-3], self.training_data[itype][:, -3])
                        y_pred.fit(self.training_data[itype][:, :-3], self.training_data[itype][:, -2])
                        death_pred.fit(self.training_data[itype][:, :-3], self.training_data[itype][:, -1])

                        self.classifiers[itype] = [x_pred, y_pred, death_pred]
        self.trained = True

    def predict(self, sso, action):
        if type(sso) != ObjectGameState:
            state = sso.origObservationGrid
            _, height, width, = sso.observationGrid.shape
        else:
            state = sso.state
            width = sso.width
            height = sso.height

        objects = {element["obsID"]: [element, i, j] for i, row in enumerate(state) for j, cell in enumerate(row) for element in cell}

        avatar = None
        avatar_x = 0
        avatar_y = 0
        for obj, [objectinfo, x_grid, y_grid] in objects.items():
            if objectinfo["category"] == 0:
                avatar = obj
                avatar_x = x_grid
                avatar_y = y_grid
                break

        next_state = [[[] for j in range(height)] for i in range(width)]

        for object_id, [objectinfo, x_grid, y_grid] in objects.items():
            print(object_id)
            neighbor_up = max([element["itype"] for element in state[x_grid][y_grid-1]], default=-1) if y_grid-1 >= 0 else -1
            neighbor_down = max([element["itype"] for element in state[x_grid][y_grid+1]], default=-1) if y_grid+1 < height else -1
            neighbor_left = max([element["itype"] for element in state[x_grid-1][y_grid]], default=-1) if x_grid-1 >= 0 else -1
            neighbor_right = max([element["itype"] for element in state[x_grid+1][y_grid]], default=-1) if x_grid+1 < width else -1

            entry = [x_grid, y_grid, neighbor_up, neighbor_down, neighbor_left, neighbor_right]
            if object_id != avatar:
                entry.extend([x_grid - avatar_x, y_grid - avatar_y, action])
            else:
                entry.extend([action])


            if self.classifiers[objectinfo["itype"]][-1].predict(np.array(entry).reshape(1, -1))[0]:
                x_grid = x_grid + self.classifiers[objectinfo["itype"]][-3].predict(np.array(entry).reshape(1, -1))[0]
                y_grid = y_grid + self.classifiers[objectinfo["itype"]][-2].predict(np.array(entry).reshape(1, -1))[0]
                if objectinfo["itype"] in self.avatar_itypes:
                    objectinfo["itype"] = self.classifiers[objectinfo["itype"]][-4].predict(np.array(entry).reshape(1, -1))[0]
                if 0 <= x_grid < width and 0 <= y_grid < height:
                    next_state[x_grid][y_grid].append(objectinfo)
                else:
                    print("out of bounce")
            else:
                print("object died")
        return ObjectGameState(next_state, width, height), self.predict_score(None)

    def predict_score(self, object_changes):
        return 0

    def add_transitions(self, previous_observation, current_action, sso):
        new_objects = []
        destroyed_objects = []
        updated_objects = []

        old_object_state = {element["obsID"]: element for row in previous_observation.origObservationGrid for cell in row for element in cell}
        new_object_state = {element["obsID"]: element for row in sso.origObservationGrid for cell in row for element in cell}
        old_grid_position = {element["obsID"]: [i, j] for i, row in enumerate(previous_observation.origObservationGrid) for j, cell in enumerate(row) for element in cell}
        new_grid_position = {element["obsID"]: [i, j] for i, row in enumerate(sso.origObservationGrid) for j, cell in enumerate(row) for element in cell}

        all_objects = set(old_object_state.keys()).union(set(new_object_state.keys()))
        for obj in all_objects:
            if obj in old_object_state:
                if obj not in new_object_state:
                    destroyed_objects.append(obj)
                else:
                    updated_objects.append(obj)
            else:
                new_objects.append(obj)

        avatar = None
        prev_avatar = None
        for obj in updated_objects:
            if old_object_state[obj]["category"] == 0:
                if new_object_state[obj]["itype"] not in self.avatar_itypes:
                    self.avatar_itypes.add(new_object_state[obj]["itype"])
                avatar = obj
                prev_avatar = obj
                break
        else:
            for obj in new_objects:
                if new_object_state[obj]["category"] == 0:
                    if new_object_state[obj]["itype"] not in self.avatar_itypes:
                        self.avatar_itypes.add(new_object_state[obj]["itype"])
                    avatar = obj
                    break
            for obj in destroyed_objects:
                if old_object_state[obj]["category"] == 0:
                    if old_object_state[obj]["itype"] not in self.avatar_itypes:
                        self.avatar_itypes.add(old_object_state[obj]["itype"])
                    prev_avatar = obj
                    break

        avatar_x, avatar_y = old_grid_position[prev_avatar]

        _, heigth, width, = sso.observationGrid.shape

        new_training_data = dict()
        for obj in all_objects:
            if obj in new_objects:
                continue
            if obj == prev_avatar:
                x_grid_new, y_grid_new = new_grid_position[avatar]
            else:
                x_grid_new, y_grid_new = new_grid_position.get(obj, old_grid_position[obj])

            x_grid, y_grid = old_grid_position[obj]
            x_diff = x_grid_new - x_grid
            y_diff = y_grid_new - y_grid

            neighbor_up = max([element["itype"] for element in previous_observation.origObservationGrid[x_grid][y_grid-1]], default=-1) if y_grid-1 >= 0 else -1
            neighbor_down = max([element["itype"] for element in previous_observation.origObservationGrid[x_grid][y_grid+1]], default=-1) if y_grid+1 < heigth else -1
            neighbor_left = max([element["itype"] for element in previous_observation.origObservationGrid[x_grid-1][y_grid]], default=-1) if x_grid-1 >= 0 else -1
            neighbor_right = max([element["itype"] for element in previous_observation.origObservationGrid[x_grid+1][y_grid]], default=-1) if x_grid+1 < width else -1

            entry = [x_grid, y_grid, neighbor_up, neighbor_down, neighbor_left, neighbor_right]
            if obj == avatar:
                entry.extend([current_action, new_object_state[obj]["itype"], x_diff, y_diff, sso.isAvatarAlive])
            else:
                if obj in destroyed_objects:
                    entry.extend([x_grid - avatar_x, y_grid - avatar_y, current_action, x_diff, y_diff, False])
                else:
                    entry.extend([x_grid - avatar_x, y_grid - avatar_y, current_action, x_diff, y_diff, True])

            if old_object_state[obj]["itype"] in new_training_data:
                new_training_data[old_object_state[obj]["itype"]].append(entry)
            else:
                new_training_data[old_object_state[obj]["itype"]] = [entry]

        for i in new_training_data:
            if i in self.training_data:
                self.training_data[i] = np.unique(np.concatenate((np.array(new_training_data[i]), self.training_data[i])), axis=0)
            else:
                self.training_data[i] = np.array(new_training_data[i])


    def get_model(self):
        pass


if __name__ == "__main__":

    # evaluation_games = ["decepticoins"] # ["bait", "decepticoins", "painter"]
    game_name = "bait"
    agent = RandomAgent()

    fm = ObjectBasedForwardModel(DecisionTreeClassifier, [])
    game = GVGAIEnvironment(game_name, 0, 0)

    observation, total_score, _, sso = game.reset()

    previous_observation = None
    tick = 0
    for tick in range(1000):
        current_action = random.choice(game.get_actions())
        observation, score, is_over, sso = game.step(current_action)
        #observation, score, is_over, sso = game.step(3)
        #observation, score, is_over, sso = game.step(2)
        #observation, score, is_over, sso = game.step(3)
        #observation, score, is_over, previous_observation = game.step(1)
        #observation, score, is_over, sso = game.step(3)

        total_score += score

        if previous_observation is not None:
            fm.add_transitions(previous_observation, current_action, sso)
            if tick % 10 == 0:
                fm.fit()

        if is_over:
            break

        previous_observation = sso

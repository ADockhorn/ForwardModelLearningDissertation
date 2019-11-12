import gym
import gym_gvgai
import matplotlib.pyplot as plt
import numpy as np
import time
from tqdm import trange

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
from sklearn.linear_model import LinearRegression
from agents.BFSObjectAgent import BFSObjectAgent
from models.objectgamestate import ObjectGameState


class ObjectBasedForwardModel:
    def __init__(self, classifier, object_types=None):
        self.trained = False
        self.base_classifier = classifier
        self.classifiers = dict()
        self.to_predict = dict()
        self.training_data = dict()
        self.avatar_itypes = set()
        self.immovable_itypes = set()
        self._is_trained = False

        self.score_model = LinearRegression()
        self.score_training_data = np.empty((0, 61))

    def is_trained(self):
        return self._is_trained

    def fit(self):
        self._is_trained = True

        self.score_model.fit(self.score_training_data[:, :-1], self.score_training_data[:, -1])
        for itype in self.training_data:
            if len(self.training_data[itype]) > 0:
                if itype in self.classifiers:
                    # update classifiers
                    if itype in self.avatar_itypes:
                        self.classifiers[itype][0].fit(self.training_data[itype][:, :-4], self.training_data[itype][:, -4])
                        self.classifiers[itype][1].fit(self.training_data[itype][:, :-4], self.training_data[itype][:, -3])
                        self.classifiers[itype][2].fit(self.training_data[itype][:, :-4], self.training_data[itype][:, -2])
                        self.classifiers[itype][3].fit(self.training_data[itype][:, :-4], self.training_data[itype][:, -1])
                        self.to_predict[itype] = True
                    elif itype in self.immovable_itypes:
                        self.classifiers[itype][2].fit(self.training_data[itype][:, :-1], self.training_data[itype][:, -1])
                        self.to_predict[itype] = self.to_predict[itype] or len(np.unique(self.training_data[itype][:, -1])) != 1
                    else:
                        self.classifiers[itype][0].fit(self.training_data[itype][:, :-3], self.training_data[itype][:, -3])
                        self.classifiers[itype][1].fit(self.training_data[itype][:, :-3], self.training_data[itype][:, -2])
                        self.classifiers[itype][2].fit(self.training_data[itype][:, :-3], self.training_data[itype][:, -1])

                        self.to_predict[itype] = self.to_predict[itype] or \
                                                 len(np.unique(self.training_data[itype][:, -3])) != 1 or \
                                                 len(np.unique(self.training_data[itype][:, -2])) != 1 or \
                                                 len(np.unique(self.training_data[itype][:, -1])) != 1
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
                        self.to_predict[itype] = True
                    elif itype in self.immovable_itypes:
                        death_pred = self.base_classifier()
                        death_pred.fit(self.training_data[itype][:, :-1], self.training_data[itype][:, -1])
                        self.classifiers[itype] = [None, None, death_pred]
                        self.to_predict[itype] = len(np.unique(self.training_data[itype][:, -1])) != 1
                    else:
                        x_pred = self.base_classifier()
                        y_pred = self.base_classifier()
                        death_pred = self.base_classifier()

                        x_pred.fit(self.training_data[itype][:, :-3], self.training_data[itype][:, -3])
                        y_pred.fit(self.training_data[itype][:, :-3], self.training_data[itype][:, -2])
                        death_pred.fit(self.training_data[itype][:, :-3], self.training_data[itype][:, -1])

                        self.classifiers[itype] = [x_pred, y_pred, death_pred]
                        self.to_predict[itype] = len(np.unique(self.training_data[itype][:, -3])) != 1 or \
                                                 len(np.unique(self.training_data[itype][:, -2])) != 1 or \
                                                 len(np.unique(self.training_data[itype][:, -1])) != 1
        self.trained = True

    def predict(self, sso, action):
        if type(sso) != ObjectGameState:
            state = sso.origObservationGrid
            _, height, width, = sso.observationGrid.shape
        else:
            state = sso.state
            width = sso.width
            height = sso.height
        death_penalty = 0

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

        living_objects = [0]*30
        died_objects_per_type = [0]*30

        for object_id, [objectinfo, x_grid, y_grid] in objects.items():
            living_objects[objectinfo["itype"]] += 1
            if objectinfo["itype"] not in self.to_predict or self.to_predict[objectinfo["itype"]] is False:
                next_state[x_grid][y_grid].append(objectinfo)
                continue

            neighbor_up = max([element["itype"] for element in state[x_grid][y_grid-1]], default=-1) if y_grid-1 >= 0 else -1
            neighbor_down = max([element["itype"] for element in state[x_grid][y_grid+1]], default=-1) if y_grid+1 < height else -1
            neighbor_left = max([element["itype"] for element in state[x_grid-1][y_grid]], default=-1) if x_grid-1 >= 0 else -1
            neighbor_right = max([element["itype"] for element in state[x_grid+1][y_grid]], default=-1) if x_grid+1 < width else -1

            entry = [x_grid, y_grid, neighbor_up, neighbor_down, neighbor_left, neighbor_right]
            if object_id != avatar:
                if objectinfo["itype"] in self.immovable_itypes:
                    entry.extend([action])
                else:
                    entry.extend([x_grid - avatar_x, y_grid - avatar_y, action])
            else:
                entry.extend([action])

            if self.classifiers[objectinfo["itype"]][-1].predict(np.array(entry).reshape(1, -1))[0]:
                if objectinfo["itype"] not in self.immovable_itypes:
                    x_grid = x_grid + self.classifiers[objectinfo["itype"]][-3].predict(np.array(entry).reshape(1, -1))[0]
                    y_grid = y_grid + self.classifiers[objectinfo["itype"]][-2].predict(np.array(entry).reshape(1, -1))[0]
                if objectinfo["itype"] in self.avatar_itypes:
                    pred_itype = self.classifiers[objectinfo["itype"]][-4].predict(np.array(entry).reshape(1, -1))[0]
                    if pred_itype != objectinfo["itype"]:
                        objectinfo["itype"] = pred_itype
                        died_objects_per_type[pred_itype] += 1
                if 0 <= x_grid < width and 0 <= y_grid < height:
                    next_state[x_grid][y_grid].append(objectinfo)
                else:
                    pass
                    #print("out of bounce")
            else:
                if objectinfo["itype"] in self.avatar_itypes:
                    death_penalty = 10
                died_objects_per_type[objectinfo["itype"]] += 1
                #print("object died")

        return ObjectGameState(next_state, width, height), self.predict_score(living_objects, died_objects_per_type) - death_penalty

    def predict_score(self, living_objects, died_objects):
        return self.score_model.predict(np.array([living_objects + died_objects]))

    def add_transitions(self, previous_observation, current_action, sso, score):
        new_objects = []
        destroyed_objects = []
        updated_objects = []

        living_objects = [0]*30
        died_objects_per_type = [0]*30

        immovable_itypes = {element.itype for type in previous_observation.immovablePositions for element in type if element is not None}
        self.immovable_itypes = self.immovable_itypes.union(immovable_itypes)

        old_object_state = {element["obsID"]: element for row in previous_observation.origObservationGrid for cell in row for element in cell}
        new_object_state = {element["obsID"]: element for row in sso.origObservationGrid for cell in row for element in cell}
        old_grid_position = {element["obsID"]: [i, j] for i, row in enumerate(previous_observation.origObservationGrid) for j, cell in enumerate(row) for element in cell}
        new_grid_position = {element["obsID"]: [i, j] for i, row in enumerate(sso.origObservationGrid) for j, cell in enumerate(row) for element in cell}

        all_objects = set(old_object_state.keys()).union(set(new_object_state.keys()))
        for obj in all_objects:
            if obj in old_object_state:
                living_objects[old_object_state[obj]["itype"]] += 1
                if obj not in new_object_state:
                    died_objects_per_type[old_object_state[obj]["itype"]] += 1
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
            if obj == prev_avatar and obj != avatar:
                continue
                #x_grid_new, y_grid_new = new_grid_position[avatar]
            #else:
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
            elif old_object_state[obj]["itype"] in self.immovable_itypes:
                entry.extend([current_action, obj not in destroyed_objects])
            else:
                entry.extend([x_grid - avatar_x, y_grid - avatar_y, current_action, x_diff, y_diff, obj not in destroyed_objects])

            if old_object_state[obj]["itype"] in new_training_data:
                new_training_data[old_object_state[obj]["itype"]].append(entry)
            else:
                new_training_data[old_object_state[obj]["itype"]] = [entry]

        for i in new_training_data:
            if i in self.training_data:
                self.training_data[i] = np.unique(np.concatenate((np.array(new_training_data[i]), self.training_data[i])), axis=0)
            else:
                self.training_data[i] = np.array(new_training_data[i])

        self.score_training_data = np.unique(np.concatenate((np.array([living_objects+died_objects_per_type+[int(score)]]), self.score_training_data)), axis=0)

    def get_model(self):
        pass


if __name__ == "__main__":

    game_name = "decepticoins"
    agent = RandomAgent()

    fm = ObjectBasedForwardModel(DecisionTreeClassifier, [])

    for level in range(3):
        game = GVGAIEnvironment(game_name, level, 0)

        for rep in range(2):
            observation, total_score, _, sso = game.reset()
            previous_observation = None
            tick = 0
            training_time = 0
            for tick in range(200):
                current_action = random.choice(game.get_actions())
                observation, score, is_over, sso = game.step(current_action)

                total_score += score
                start_time = time.time()
                if previous_observation is not None:
                    fm.add_transitions(previous_observation, current_action, sso, score)
                end_time = time.time()
                training_time += end_time - start_time

                if is_over:
                    break

                previous_observation = sso
            print("points", total_score, "ticks", tick, "mean_time", training_time/tick)
        game.close()
    fm.fit()

    print()
    print("now evaluate agent")
    #set up agent
    from agents.AgentParameters import BFS_AGENT_PARAMETERS

    bfs = BFSObjectAgent(**BFS_AGENT_PARAMETERS)
    bfs._expansions = 100
    bfs.set_forward_model(fm)

    for level in range(3):
        game = GVGAIEnvironment(game_name, level, 0)
        fig, axis = plt.subplots(1, 1)
        plt.axis("off")
        ims = []

        observation, total_score, _, sso = game.reset()
        search_time = 0
        for tick in trange(200, ncols=150):
            ims.append([plt.imshow(sso.image)])

            start_time = time.time()
            current_action = bfs.get_next_action(sso, [1, 2, 3, 4])
            end_time = time.time()

            observation, score, is_over, sso = game.step(current_action)
            total_score += score
            search_time += end_time - start_time

            if is_over:
                break

        print("points", total_score, "ticks", tick, "mean_time", search_time / tick)
        anim = animation.ArtistAnimation(fig, ims, interval=100, blit=False, repeat=False)
        anim.save(f'test_{level}.mp4')
        game.close()

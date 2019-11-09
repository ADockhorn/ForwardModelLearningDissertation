import gym
import gym_gvgai
import matplotlib.pyplot as plt
import numpy as np
from abstractclasses.AbstractGrid import AbstractGrid
from typing import Dict, Tuple, List
import logging
import copy
import logging
from sklearn.tree import DecisionTreeClassifier
from abstractclasses.AbstractNeighborhoodPattern import CrossNeighborhoodPattern, SquareNeighborhoodPattern
from models.localforwardmodel import LocalForwardModel
import random
import time
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC
from games.TileMapVisualizer import TileMapVisualizer
from games.GVGAIConstants import *
from tqdm import trange, tqdm


class GVGAIGrid(AbstractGrid):

    def __init__(self, width, height, grid_dict: Dict, grid_data=None):
        self.grid_dict = grid_dict
        self.grid = None

        if grid_data is not None:
            self.set_grid(grid_data)

        super().__init__(width, height)

    def get_grid(self):
        return self.grid

    def set_grid(self, level_string):
        self.force_set_grid(np.array([[self.grid_dict.get(obj, "x") for obj in s.split(",")]
                                      for s in level_string.split("\n")]).transpose())

    def force_set_grid(self, grid_data):
        self.grid = grid_data

    def get_observation(self):
        return self.grid.copy()

    def get_cell(self, x: int, y: int):
        if not self.in_limits(x, y):
            logging.error(f"Can't get cell ({x}, {y}), because it is outside the grid's boundaries")
        return self.grid[x, y]

    def set_cell(self, x: int, y: int, cell):
        if not self.in_limits(x, y):
            logging.error(f"Can't get cell ({x}, {y}), because it is outside the grid's boundaries")
        self.grid[x, y] = cell

    def get_difference(self, other: 'AbstractGrid'):
        return sum([x != y for (x, y) in zip(self.grid.flatten(), other.get_grid().flatten())])

    def deep_copy(self):
        return copy.deepcopy(self)

    def get_identifier(self):
        return "".join(self.grid.flatten().tolist())

    def __str__(self) -> str:
        string = ""
        for row in range(self._height):
            row_string = self.grid[:, row].tolist()
            string += "".join(row_string) + "\n"
        return string


class GVGAIEnvironment:

    def __init__(self, game, level, version):
        self.env = gym.make(f"gvgai-{game}-lvl{level}-v{version}")
        self.env.reset()
        self.image, _, _, self.info = self.env.step(0)

        self.height = int(self.image.shape[0]/10)
        self.width = int(self.image.shape[1]/10)
        self.tick = 1
        self.game_title = f"{game}-lvl{level}-v{version}"
        self.game_name = game
        sso = self.info["sso"]

        self.available_actions = list(range(0, len(self.info["sso"].availableActions)+1))
        # self.tsv = TileMapVisualizer(GVGAIConstants.images[game], 10)

    def step(self, action) -> Tuple[AbstractGrid, int, bool, None]:
        image, score, is_over, self.info = self.env.step(action)
        self.image = image
        self.tick += 1
        self.available_actions = list(range(0, len(self.info["sso"].availableActions)+1))
        return GVGAIGrid(self.width, self.height, get_object_dict(self.game_name),
                         self.env.render(mode="ascii")), score, is_over, self.info["sso"]

    def get_actions(self):
        return self.available_actions

    def reset(self):
        self.env.reset()
        obs, score, is_done, info = self.env.step(0)
        return GVGAIGrid(self.width, self.height, get_object_dict(self.game_name),
                         self.env.render(mode="ascii")), score, is_done, info["sso"]

    def render(self):
        plt.imshow(self.image)
        plt.axis("off")
        plt.title(self.game_title)
        plt.show()

    def close(self):
        # plt.close(self.fig)
        self.env.close()
        pass


def transform_to_grid(obs, object_dict=None):
    if object_dict is None:
        objects = set([obj for s in obs.split("\n") for obj in s.split(",")])
        object_dict = {obj: ind for ind, obj in enumerate(objects)}
        return np.array([[object_dict[obj] for obj in s.split(",")] for s in obs.split("\n")]), object_dict
    return np.array([[object_dict.get(obj, "x") for obj in s.split(",")] for s in obs.split("\n")]), object_dict


def find_all_strings(game_name, version):
    all_objects = set()
    for level in range(5):
        game = GVGAIEnvironment(game_name, level, version)

        for i in range(1000):
            game.reset()
            for j in range(10):
                _, _, is_over, info = game.step(random.choice(game.get_actions()))
                objects = {obj for s in info.observationString.split("\n") for obj in s.split(",")}
                all_objects = all_objects.union(objects)
                if is_over:
                    break
        game.close()

    return all_objects


def train_model(fm, game_name: str, levels: List[int], version: int, rep: int = 10, ticks: int = 100,
                sm=None):
    logging.debug("train forward model")
    for level in tqdm(levels, desc="levels", ncols=100):
        game = GVGAIEnvironment(game_name, level, version)

        for i in trange(rep, desc="repetitions", ncols=100):
            game.reset()
            previous_observation = None
            for i in trange(ticks, desc="ticks", ncols=100):
                current_action = random.choice(game.get_actions())
                observation, score, is_over, _ = game.step(current_action)
                observation = observation.get_grid()
                if previous_observation is not None:
                    fm.add_transition(previous_observation, current_action, observation)
                    if sm is not None:
                        sm.add_transition(previous_observation, observation, score)

                previous_observation = observation
                if is_over:
                    break
        game.close()

    fm.fit()
    if sm is not None:
        sm.fit()
        return fm, sm

    return fm


def test_model(fm, game, levels, version, rep=10, ticks=100, agent=None, retrain=False):
    statistics = {"accuracy": None,
                  "dynamic_accuracy": None}

    for level in levels:
        env = gym.make(f"gvgai-{game}-lvl{level}-v{version}")
        env.reset()
        env.step(0)

        pixel_shape = env.render(mode="rgb_array").shape
        height = int(pixel_shape[0]/10)
        width = int(pixel_shape[1]/10)

        observation = GVGAIGrid(width, height, get_object_dict(game), env.render(mode="ascii")).grid
        states = []
        state_predictions = [None]
        previous_observation = None
        predicted_states = []

        for i in range(100):
            current_action = random.choice(range(1, 5))
            logging.info(f"tick: {i}")
            pred = fm.predict(observation, current_action)
            pred_state = GVGAIGrid(width, height, get_object_dict(game))
            pred_state.force_set_grid(pred.reshape(width, height))
            predicted_states.append(pred_state)
            _, reward, done, info = env.step(current_action)
            state = GVGAIGrid(width, height, get_object_dict(game), env.render(mode="ascii"))
            states.append(state)
            observation = state.grid

        differences = 0
        for state, pred_state in zip(states, predicted_states):
            differences += state.get_difference(pred_state)
        print(f"mean difference level {level} = {differences/len(states)}")


if __name__ == "__main__":
    import os
    os.chdir("/".join(os.getcwd().split("/")[:-1]))

    FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)

    game = "butterflies"
    version = 0
    # objects = find_all_strings(game, version)
    # print(objects)

    forward_model = LocalForwardModel(DecisionTreeClassifier(),
        CrossNeighborhoodPattern(2),
        possibleObservations=np.append(np.array(list(get_object_dict(game).values())), np.array(["0", "1", "2", "3", "4", "x"])))

    start = time.time()
    train_model(forward_model, game, [0, 1, 2], 0)
    end = time.time()
    #logging.info(f"training model took {end-start} seconds")

    game = GVGAIEnvironment("butterflies", 1, version)
    a, b, c, d = game.step(0)

    fig, ax = plt.subplots(2, 4)
    fig.set_figheight(5)
    fig.set_figwidth(12)

    ax[0, 1].imshow(d.image)
    ax[0, 1].set_axis_off()
    tsv = TileMapVisualizer(GVGAIConstants.images, 24)
    tsv.visualize_observation_grid(a, 28, 11, axis=ax[0, 2])

    for action in range(1, 5):
        pred = forward_model.predict(a, action).reshape(28, 11)
        tsv.visualize_observation_grid(pred, 28, 11, axis=ax[1, action-1])
    ax[0, 0].set_axis_off()
    ax[0, 3].set_axis_off()
    plt.tight_layout()
    plt.show()


    """
    score = 0
    for i in range(10):
        state, reward, isOver, debug = env.step(env.action_space.sample())
        score += reward
        if isOver:
            break

        plt.imshow(env.render(mode="rgb_array"))
        plt.axis("off")
        plt.title("%s | Step: %d %s" % (game, i, score))
        plt.show()

        a, _ = transform_to_grid(env.render(mode="ascii"), get_object_dict(game))
        print(a)

    env.close()
    """

    # train model

    # test
    # sokoban test sequence
    actions = [2, 3, 3, 1, 3, 2, 2, 2, 2, 2, 3, 2]

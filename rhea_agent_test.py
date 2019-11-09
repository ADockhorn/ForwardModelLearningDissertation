from abstractclasses.AbstractGameState import AbstractGameState
from abstractclasses.AbstractGrid import AbstractGrid
from abstractclasses.AbstractForwardModel import AbstractForwardModel
import copy
import random
import numpy

import gym
import gym_gvgai
import matplotlib.pyplot as plt
import numpy as np

from sklearn.tree import DecisionTreeClassifier
from abstractclasses.AbstractNeighborhoodPattern import CrossNeighborhoodPattern, SquareNeighborhoodPattern
from models.localforwardmodel import LocalForwardModel
import random
from games.TileMapVisualizer import TileMapVisualizer
from games.GVGAIConstants import GVGAIConstants
from games.gvgai_environment import GVGAIEnvironment
from agents.RHEA import RHEAAgent
from agents.BFSAgent import BFSAgent
from matplotlib import animation
import math


class ForwardModelEnvironment(AbstractGameState):

    def __init__(self, fm: AbstractForwardModel, state: AbstractGrid, sm):
        self.fm = fm
        self.state = state
        self.width = state.get_width()
        self.height = state.get_height()
        self._tick = 0
        self.sm = sm

        super().__init__()

    def get_tick(self):
        return self._tick

    def next(self, action):
        self.state.force_set_grid(self.fm.predict(self.state.get_grid(), action).reshape(self.width, self.height))

    def get_actions(self):
        return [1, 2, 3, 4]

    @property
    def get_random_action(self):
        return random.choice(self.get_actions())

    def get_score(self, previousObs, obs):
        # return self.width * self.height - np.sum(self.state.get_grid() == "g")
        return self.sm.predict(previousObs, obs)

    def is_terminal(self):
        return "g" not in self.state.get_grid()

    def deep_copy(self):
        return copy.deepcopy(self)

    def evaluate_rollout(self, action_sequence, discount_factor):
        discounted_return = 0
        if discount_factor is None:
            for idx, action in enumerate(action_sequence):
                prevObs = self.state.get_grid()
                self.next(action)
                discounted_return += self.get_score(prevObs, self.state.get_grid())
        else:
            for idx, action in enumerate(action_sequence):
                prevObs = self.state.get_grid()
                self.next(action)
                discounted_return += self.get_score(prevObs, self.state.get_grid()) * math.pow(discount_factor, idx)

        return discounted_return


from sklearn.linear_model import LinearRegression

class GlobalScoreModel:
    def __init__(self, possibleObservations):
        self.model = None

        self._data_set = np.zeros((0, len(possibleObservations)*3+1))
        # first n elements = how often is the obj unchanged
        # second n elements = how often did cells become of type obj
        # third n elements = how often did cells become something else when previously being of type obj

        self.possibleObservations = {obj: index for index, obj in enumerate(possibleObservations)}
        self.num_elements = len(self.possibleObservations)

    def fit(self):
        self.model = LinearRegression().fit(self._data_set[:, :-1], self._data_set[:, -1])

    def add_transition(self, previousObs, obs, score):
        self._data_set = np.unique(np.concatenate((self.create_vector(previousObs, obs, score), self._data_set)), axis=0)

    def create_vector(self, previousObs, obs, score=None):
        if score is not None:
            new_data = np.zeros((1, self.num_elements * 3 + 1))
            new_data[:, -1] = score
        else:
            new_data = np.zeros((1, self.num_elements * 3))

        for prev, now in zip(previousObs.flatten(), obs.flatten()):
            if prev == now:
                new_data[0, self.possibleObservations[prev]] += 1
            else:
                new_data[0, self.num_elements + self.possibleObservations[now]] += 1
                new_data[0, self.num_elements * 2 + self.possibleObservations[prev]] -= 1

        return new_data

    def predict(self, previousObs, obs):
        if self.model is not None:
            return self.model.predict(self.create_vector(previousObs, obs))[0]
        else:
            raise AssertionError("score model not trained yet. first call fit()")

    def get_dataset(self):
        return self._data_set


if __name__ == "__main__":
    game = "painter"
    num_evals = 30
    rollout_length = 5
    mutation_probability = 0.1

    forward_model = LocalForwardModel(DecisionTreeClassifier(), CrossNeighborhoodPattern(2),
        possibleObservations=np.append(np.array(list(GVGAIConstants.get_object_dict(game).values())), np.array(["0", "1", "2", "3", "4", "x"])))
    score_model = GlobalScoreModel(possibleObservations=np.append(np.array(list(GVGAIConstants.get_object_dict(game).values())), np.array(["0", "1", "2", "3", "4", "x"])))

    from games.gvgai_environment import train_model
    train_model(forward_model, game, levels=[0, 1, 2], version=0, rep=3, ticks=200, sm=score_model)

    if False:
        env = GVGAIEnvironment(game, 0, 0)
        obs, score, _, sso = env.reset()
        for tick in range(100):
            fms = ForwardModelEnvironment(forward_model, obs.deep_copy(), score_model)
            fms.deep_copy().evaluate_rollout([1], None)
            obs, score, _, _ = env.step(random.choice(env.available_actions))


    if False:
        for level in range(5):
            fig, axis = plt.subplots(1, 1)
            plt.axis("off")
            ims = []

            env = GVGAIEnvironment(game, level, 0)
            a, score, _, sso = env.reset()
            for tick in range(1000):
                ttl = axis.text(0.5, 1.01, f"{game} | score = {score} | tick = {tick}", horizontalalignment='center',
                                verticalalignment='bottom', transform=axis.transAxes)
                ims.append([plt.imshow(sso.image), ttl])

                fms = ForwardModelEnvironment(forward_model, a.deep_copy(), score_model)
                rhea = RHEAAgent(fms, rollout_length, mutation_probability, num_evals)
                a, score, is_done, sso = env.step(rhea._get_next_action())

                if is_done:
                    ims.append([plt.imshow(sso.image), ttl])
                    print(f"game won after {tick} ticks")
                    break
            else:
                print(f"game not won after {tick} ticks")

            anim = animation.ArtistAnimation(fig, ims, interval=100, blit=False, repeat=False)
            anim.save(f'{game}_{level}_rhea_agent.mp4')


    if False:
        for level in range(5):
            fig, axis = plt.subplots(1, 1)
            plt.axis("off")
            ims = []

            env = GVGAIEnvironment(game, level, 0)
            a, score, _, sso = env.reset()
            for tick in range(100):
                ttl = axis.text(0.5, 1.01, f"{game} | score = {score} | tick = {tick}", horizontalalignment='center',
                                verticalalignment='bottom', transform=axis.transAxes)
                ims.append([plt.imshow(sso.image), ttl])

                fms = ForwardModelEnvironment(forward_model, a.deep_copy(), score_model)
                bfs = BFSAgent(fms, 3)
                a, score, is_done, sso = env.step(bfs._get_next_action())

                if is_done:
                    ims.append([plt.imshow(sso.image), ttl])
                    print(f"game won after {tick} ticks")
                    break
            else:
                print(f"game not won after {tick} ticks")

            anim = animation.ArtistAnimation(fig, ims, interval=100, blit=False, repeat=False)
            anim.save(f'videos/{game}_{level}_bfs_agent.mp4')

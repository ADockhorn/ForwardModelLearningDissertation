import gym
import gym_gvgai
import matplotlib.pyplot as plt
import numpy as np

from sklearn.tree import DecisionTreeClassifier

from abstractclasses.AbstractNeighborhoodPattern import SquareNeighborhoodPattern
from agents.BFSObjectAgent import BFSObjectAgent
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

from models.objectforwardmodel import ObjectBasedForwardModel


def load_results(game_name: str):
    with open(f"results/{game_name}/transfer_learning_model_extraction.txt", "rb") as f:
        return pickle.load(f)


def save_results(game_name, results):
    with open(f"results/{game_name}/transfer_learning_model_extraction.txt", "wb") as f:
        pickle.dump(results, f)


def train_transfer_learning_models(lfm, sm, obfm, game_name):
    ticks_per_level = 5000
    max_ticks_per_level = 100
    levels = [0, 1, 2]

    if os.path.exists(f"results/{game_name}/transfer_learning_model_extraction.txt"):
        with open(f"results/{game_name}/transfer_learning_model_extraction.txt", "rb") as f:
            results = pickle.load(f)
        if "local_forward_model" in results:
            lfm = results["local_forward_model"]
            sm = results["score_model"]
            obfm = results["object_based_model"]
    else:
        results = {"ticks_per_level": [0]*len(levels),
                   "repetitions_per_level": [0]*len(levels)}
    save_results(game_name, results)

    for level in levels:

        pbar = tqdm(total=ticks_per_level, desc=f"{game_name}, level {level}, ticks",  ncols=200)
        pbar.update(results["ticks_per_level"][level])
        ticks = results["ticks_per_level"][level]

        while ticks < ticks_per_level:
            game = GVGAIEnvironment(game_name, level, 0)

            observation, total_score, is_over, sso = game.reset()

            previous_observation_lfm = None
            previous_observation_ob = None
            ticks_since_restart = 0

            for i in range(max_ticks_per_level):
                ticks += 1
                ticks_since_restart += 1
                pbar.update(1)

                current_action = random.choice(game.get_actions())

                observation, score, is_over, sso = game.step(current_action)
                total_score += score

                if previous_observation_lfm is not None:
                    lfm.add_transition(previous_observation_lfm, current_action, observation.get_grid())
                    obfm.add_transitions(previous_observation_ob, current_action, sso, score)

                    if is_over and game.info["sso"].gameWinner == "PLAYER_WINS":
                        sm.add_transition(previous_observation_lfm, observation.get_grid(), score + 1000)
                    else:
                        sm.add_transition(previous_observation_lfm, observation.get_grid(), score)

                if is_over or ticks == ticks_per_level or ticks_since_restart == 500:
                    break

                previous_observation_ob = sso
                previous_observation_lfm = observation.get_grid()

            game.close()
            results["ticks_per_level"][level] = ticks
            results["repetitions_per_level"][level] += 1
            results["local_forward_model"] = lfm
            results["score_model"] = sm
            results["object_based_model"] = obfm
            #save_results(game_name, results)
        pbar.close()

    save_results(game_name, results)

    print("fit models")

    lfm.fit()
    obfm.fit()
    sm.fit()

    lfm._data_set = None
    sm._data_set = None
    obfm.score_training_data = None
    obfm.training_data = None

    print("store models")
    with open(f"results/{game_name}/models/transfer_learning_model_lfm.txt", "wb") as f:
        pickle.dump({"forward_model": lfm, "score_model": sm}, f)

    with open(f"results/{game_name}/models/transfer_learning_model_obfm.txt", "wb") as f:
        pickle.dump({"forward_model": obfm}, f)


if __name__ == "__main__":
    grid_based_games = []
    with open("data/GVGAI/grid-based-games.txt", "r") as file:  # Use file to refer to the file object
        for s in file.readlines():
            if len(s) > 1:
                grid_based_games.append(s[:-1])

    evaluation_games = []
    for game in grid_based_games:
        n_levels = len([env_spec.id for env_spec in envs.registry.all() if env_spec.id.startswith(f"gvgai-{game}-")])
        if len(get_images(game)) > 25 or n_levels < 3:
            logging.info(f"game {game} was excluded")
            continue
        evaluation_games.append(game)

    for game_name in evaluation_games:

        if not os.path.exists(f"results/{game_name}/"):
            os.mkdir(f"results/{game_name}/")
        if os.path.exists(f"results/{game_name}/transfer_learning_model_extraction_lock.txt") or \
            os.path.exists(f"results/{game_name}/models/transfer_learning_model_lfm.txt") or \
            os.path.exists(f"results/{game_name}/models/transfer_learning_model_obfm.txt"):
            continue
        else:
            with open(f"results/{game_name}/transfer_learning_model_extraction_lock.txt", "wb") as f:
                pickle.dump([0], f)

        print(f"processing {game_name}")

        lfm = LocalForwardModel(DecisionTreeClassifier(), SquareNeighborhoodPattern(3),
                                possibleObservations=np.append(
                                              np.array(list(get_object_dict(game_name).values())),
                                              np.array(["0", "1", "2", "3", "4", "5", "x"])))
        sm = GlobalScoreModel(possible_observations=np.append(np.array(list(get_object_dict(game_name).values())),
                                                              np.array(["0", "1", "2", "3", "4", "5", "x"])))
        obfm = ObjectBasedForwardModel(DecisionTreeClassifier, [])

        train_transfer_learning_models(lfm, sm, obfm, game_name)

        if os.path.exists(f"results/{game_name}/transfer_learning_model_extraction_lock.txt"):
            os.remove(f"results/{game_name}/transfer_learning_model_extraction_lock.txt")

        break

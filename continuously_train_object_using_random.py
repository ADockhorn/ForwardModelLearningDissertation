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


def save_results(game_name, results):
    with open(f"results/{game_name}/ob_continuous_results_{AGENT_NAME}.txt", "wb") as f:
        pickle.dump(results, f)


def continuously_train_model(agent, fm, game_name: str, levels: List[int], version: int):
    logging.debug("train forward model")

    ticks_per_level = 2000
    max_ticks_per_level = 300

    if os.path.exists(f"results/{game_name}/ob_continuous_results_{AGENT_NAME}.txt"):
        with open(f"results/{game_name}/ob_continuous_results_{AGENT_NAME}.txt", "rb") as f:
            results = pickle.load(f)
        if "forward_model" in results:
            fm = results["forward_model"]
    else:
        results = {"ticks_per_level": [0] * len(levels),
                   "repetitions_per_level": [0] * len(levels)}

    save_results(game_name, results)

    for level in tqdm(levels):

        pbar = tqdm(total=ticks_per_level, desc=f"{game_name}, level {level}, ticks",  ncols=200)
        pbar.update(results["ticks_per_level"][level])
        ticks = results["ticks_per_level"][level]

        while ticks < ticks_per_level:
            agent.re_initialize()

            game = GVGAIEnvironment(game_name, level, version)

            observation, total_score, _, sso = game.reset()

            previous_observation = None

            for i in range(max_ticks_per_level):
                ticks += 1

                pbar.update(1)
                current_action = random.choice(game.get_actions())

                observation, score, is_over, sso = game.step(current_action)
                total_score += score

                if previous_observation:
                    fm.add_transitions(previous_observation, current_action, sso, score)

                if is_over or ticks == ticks_per_level:
                    break

                previous_observation = sso

            game.close()
            results["forward_model"] = fm
            results["ticks_per_level"][level] = ticks
            results["repetitions_per_level"][level] += 1
            save_results(game_name, results)
        pbar.close()
    fm.fit()
    results["forward_model"] = fm
    save_results(game_name, results)

    fm.training_data = None
    print("store models")
    with open(f"results/{game_name}/models/ob_forward_model_RANDOM.txt", "wb") as f:
        pickle.dump(fm, f)



if __name__ == "__main__":
    grid_based_games = []
    with open("data/GVGAI/grid-based-games.txt", "r") as file:  # Use file to refer to the file object
        for s in file.readlines():
            if len(s) > 1:
                grid_based_games.append(s[:-1])

    agents = [RandomAgent(), RHEAAgent(**RHEA_AGENT_PARAMETERS), BFSAgent(**BFS_AGENT_PARAMETERS)]

    evaluation_games = []
    for game in grid_based_games:
        n_levels = len([env_spec.id for env_spec in envs.registry.all() if env_spec.id.startswith(f"gvgai-{game}-")])
        if len(get_images(game)) > 25 or n_levels < 3:
            logging.info(f"game {game} was excluded")
            continue
        evaluation_games.append(game)

    for game_name in evaluation_games:
        AGENT_NAME = "RANDOM"
        agent = RandomAgent()

        # setup file paths for the results
        if not os.path.exists(f"results/{game_name}/"):
            os.mkdir(f"results/{game_name}/")
        #if os.path.exists(f"results/{game_name}/ob_continuous_results_lock_{AGENT_NAME}.txt") or \
        #    os.path.exists(f"results/{game_name}/ob_continuous_results_{AGENT_NAME}.txt"):
        #    continue
        if os.path.exists(f"results/{game_name}/models/ob_forward_model_{AGENT_NAME}.txt"):
            print("skip ", game_name)
            continue
        else:
            with open(f"results/{game_name}/ob_continuous_results_lock_{AGENT_NAME}.txt", "wb") as f:
                pickle.dump([0], f)

        print(f"processing {game_name}")

        forward_model = ObjectBasedForwardModel(DecisionTreeClassifier, [])
        agent.set_forward_model(forward_model)

        continuously_train_model(agent, forward_model, game_name=game_name, levels=[0, 1, 2, 3, 4], version=0)

        if os.path.exists(f"results/{game_name}/ob_continuous_results_lock_{AGENT_NAME}.txt"):
            os.remove(f"results/{game_name}/ob_continuous_results_lock_{AGENT_NAME}.txt")

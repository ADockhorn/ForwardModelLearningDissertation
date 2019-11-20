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


def load_models(game_name):
    with open(f"results/{game_name}/models/lfm_forward_model_RANDOM.txt", "rb") as f:
        results_lfm = pickle.load(f)

    return results_lfm["forward_model"], results_lfm["score_model"]


def load_results(game_name: str):
    with open(f"results/{game_name}/training_results/constant_lfm_{agent_name}.txt", "rb") as f:
        return pickle.load(f)


def save_results(game_name, results):
    with open(f"results/{game_name}/training_results/constant_lfm_{agent_name}.txt", "wb") as f:
        pickle.dump(results, f)


def evaluate_lfm(agent, game_name, agent_name):
    levels = [0, 1, 2, 3, 4]
    if os.path.exists(f"results/{game_name}/training_results/constant_lfm_{agent_name}.txt"):
        with open(f"results/{game_name}/training_results/constant_lfm_{agent_name}.txt", "rb") as f:
            results = pickle.load(f)
        if f"LFM_{agent_name}" not in results:
            results[f"LFM_{agent_name}"] = {"scores": np.zeros((len(levels), 10)),
                                            "game_won": np.zeros((len(levels), 10)),
                                            "ticks": np.zeros((len(levels), 10))}
    else:
        results = {f"LFM_{agent_name}": {"scores": np.zeros((len(levels), 10)),
                                         "game_won": np.zeros((len(levels), 10)),
                                         "ticks": np.zeros((len(levels), 10))}}

    save_results(game_name, results)

    for rep in range(10):
        for level_idx, level in enumerate(levels):
            if results[f"LFM_{agent_name}"]["ticks"][level_idx, rep]:
                continue

            game = GVGAIEnvironment(game_name, level, 0)
            agent.re_initialize()
            observation, total_score, is_over, sso = game.reset()
            pbar = tqdm(2000, desc=f"{agent_name}, {game_name}, rep {rep}, level {level}, ticks", ncols=100)
            for tick in range(2000):
                pbar.update(1)

                current_action = agent.get_next_action(observation, game.get_actions())

                observation, score, is_over, sso = game.step(current_action)
                total_score += score

                if is_over and game.info["sso"].gameWinner == "PLAYER_WINS":
                    results[f"LFM_{agent_name}"]["game_won"][level_idx, rep] = 1

                if is_over:
                    break

            game.close()
            results[f"LFM_{agent_name}"]["scores"][level_idx, rep] = total_score
            results[f"LFM_{agent_name}"]["ticks"][level_idx, rep] = tick
            pbar.close()
            save_results(game_name, results)

    save_results(game_name, results)


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

        if not os.path.exists(f"results/{game_name}/models/lfm_forward_model_RANDOM.txt"):
            continue
        if not os.path.exists(f"results/{game_name}/lfm_learning_model_evaluation_lock_BFS.txt"):
            with open(f"results/{game_name}/lfm_learning_model_evaluation_lock_BFS.txt", "wb") as f:
                pickle.dump([0], f)

            print(f"processing {game_name}, BFS")

            lfm, sm = load_models(game_name)

            for agent, agent_name in zip([BFSAgent(**BFS_AGENT_PARAMETERS)], ["BFS"]):
                agent.set_forward_model(lfm)
                agent.set_score_model(sm)
                evaluate_lfm(agent, game_name, agent_name)

            if os.path.exists(f"results/{game_name}/lfm_learning_model_evaluation_lock_BFS.txt"):
                os.remove(f"results/{game_name}/lfm_learning_model_evaluation_lock_BFS.txt")

        if not os.path.exists(f"results/{game_name}/lfm_learning_model_evaluation_lock_RHEA.txt"):
            with open(f"results/{game_name}/lfm_learning_model_evaluation_lock_RHEA.txt", "wb") as f:
                pickle.dump([0], f)

            print(f"processing {game_name}, RHEA")

            lfm, sm = load_models(game_name)

            for agent, agent_name in zip([RHEAAgent(**RHEA_AGENT_PARAMETERS)], ["RHEA"]):
                agent.set_forward_model(lfm)
                agent.set_score_model(sm)
                evaluate_lfm(agent, game_name, agent_name)

            if os.path.exists(f"results/{game_name}/lfm_learning_model_evaluation_lock_RHEA.txt"):
                os.remove(f"results/{game_name}/lfm_learning_model_evaluation_lock_RHEA.txt")

        break

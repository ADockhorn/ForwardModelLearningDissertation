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


def load_results(game_name: str):
    with open(f"results/{game_name}/lfm_results.txt", "rb") as f:
        return pickle.load(f)


def save_results(game_name, results):
    with open(f"results/{game_name}/lfm_results.txt", "wb") as f:
        pickle.dump(results, f)


def load_fm_sm(game_name):
    fm = None
    with open(f"results/{game_name}/forward_model.txt", "rb") as f:
        fm = pickle.load(f)
    sm = None
    with open(f"results/{game_name}/score_model.txt", "rb") as f:
        sm = pickle.load(f)
    return fm, sm


def evaluate_agent(agent, agent_name, game_name: str, levels: List[int], version: int):
    logging.debug("train forward model")

    max_ticks = 2000
    repetitions = 10
    n_levels = 5

    if os.path.exists(f"results/{game_name}/lfm_results.txt"):
        results = load_results(game_name)
    else:
        results = dict()
    if agent_name not in results:
        results[agent_name] = {"scores": np.zeros((n_levels, repetitions)),
                   "ticks": np.zeros((n_levels, repetitions)),
                   "game_won": np.zeros((n_levels, repetitions))}
    save_results(game_name, results)

    for rep in range(repetitions):
        for level in tqdm(levels, desc="levels", ncols=100):
            if results[agent_name]["ticks"][level, rep] != 0:
                continue

            agent.re_initialize()
            agent._discount_factor = 0.95

            game = GVGAIEnvironment(game_name, level, version)

            observation, total_score, _, sso = game.reset()

            tick = 0
            for tick in trange(max_ticks, desc="ticks", ncols=100):
                current_action = agent.get_next_action(observation, game.get_actions())

                observation, score, is_over, sso = game.step(current_action)
                total_score += score

                if is_over:
                    if game.info["sso"].gameWinner == "PLAYER_WINS":
                        results[agent_name]["game_won"][level, rep] = 1
                    break

            results[agent_name]["ticks"][level, rep] = tick
            results[agent_name]["scores"][level, rep] = total_score

            game.close()

            agent.re_initialize()
            save_results(game_name, results)


if __name__ == "__main__":
    grid_based_games = []
    with open("data/GVGAI/grid-based-games.txt", "r") as file:  # Use file to refer to the file object
        for s in file.readlines():
            if len(s) > 1:
                grid_based_games.append(s[:-1])

    # filter games that have too complex state representations and games that do not provide 5 levels
    evaluation_games = []
    for game in grid_based_games:
        n_levels = len([env_spec.id for env_spec in envs.registry.all() if env_spec.id.startswith(f"gvgai-{game}-")])
        if len(get_images(game)) > 25 or n_levels < 3:
            logging.info(f"game {game} was excluded")
            continue
        evaluation_games.append(game)

    agents = [RandomAgent(), RHEAAgent(**RHEA_AGENT_PARAMETERS), BFSAgent(**BFS_AGENT_PARAMETERS)]
    for game_name in evaluation_games:

        if not os.path.exists(f"results/{game_name}/forward_model.txt"):
            print(f"game {game_name} cannot be evaluated yet, since the BFS model is not trained yet")
            continue
        if os.path.exists(f"results/{game_name}/lfm_results_lock.txt"):
            print(f"game {game_name} is evaluated by another thread")
            continue
        else:
            with open(f"results/{game_name}/lfm_results_lock.txt", "wb") as f:
                pickle.dump([0], f)

            print(f"evaluate game {game_name}")

        for agent, AGENT_NAME in tqdm(zip(agents, ["Random", "RHEA", "BFS"])):
            forward_model, score_model = load_fm_sm(game_name)

            agent.set_forward_model(forward_model)
            agent.set_score_model(score_model)

            evaluate_agent(agent, AGENT_NAME, game_name=game_name, levels=[0, 1, 2, 3, 4], version=0)

        if os.path.exists(f"results/{game_name}/lfm_results_lock.txt"):
            os.remove(f"results/{game_name}/lfm_results_lock.txt")

        break

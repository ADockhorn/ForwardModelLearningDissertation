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
from agents.RHEAObject import RHEAObjectAgent
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
from agents.MCTSObject import MCTSObjectAgent


def load_models(game_name):
    with open(f"results/{game_name}/models/ob_forward_model_RANDOM.txt", "rb") as f:
        fm = pickle.load(f)

    return fm


def load_results(game_name, agent_name, levels):
    results = dict()
    if os.path.exists(f"results/{game_name}/training_results/constant_obfm_{agent_name}.txt"):
        with open(f"results/{game_name}/training_results/constant_obfm_{agent_name}.txt", "rb") as f:
            results = pickle.load(f)
        if f"OBFM_{agent_name}" not in results:
            results[f"OBFM_{agent_name}"] = {"scores": np.zeros((len(levels), 10)),
                                             "game_won": np.zeros((len(levels), 10)),
                                             "ticks": np.zeros((len(levels), 10))}
    else:
        if os.path.exists(f"results/{game_name}/constant_result_ob_RANDOM.txt"):
            with open(f"results/{game_name}/constant_result_ob_RANDOM.txt", "rb") as f:
                prev_results = pickle.load(f)
            if agent_name in prev_results:
                results = {f"OBFM_{agent_name}": prev_results[agent_name]}
            else:
                results = {f"OBFM_{agent_name}": {"scores": np.zeros((len(levels), 10)),
                                                  "game_won": np.zeros((len(levels), 10)),
                                                  "ticks": np.zeros((len(levels), 10))}}
        else:
            results = {f"OBFM_{agent_name}": {"scores": np.zeros((len(levels), 10)),
                                              "game_won": np.zeros((len(levels), 10)),
                                              "ticks": np.zeros((len(levels), 10))}}
    return results


def save_results(game_name, results):
    with open(f"results/{game_name}/training_results/constant_obfm_{agent_name}.txt", "wb") as f:
        pickle.dump(results, f)


def evaluate_obfm(agent, game_name, agent_name):
    levels = [0, 1, 2, 3, 4]
    results = load_results(game_name, agent_name, levels)

    save_results(game_name, results)

    for rep in range(10):
        for level_idx, level in enumerate(levels):
            if results[f"OBFM_{agent_name}"]["ticks"][level_idx, rep]:
                continue

            game = GVGAIEnvironment(game_name, level, 0)
            agent.re_initialize()
            observation, total_score, is_over, sso = game.reset()
            pbar = tqdm(2000, desc=f"{agent_name}, {game_name}, rep {rep}, level {level}, ticks", ncols=100)
            for tick in range(2000):
                pbar.update(1)

                current_action = agent.get_next_action(sso, game.get_actions())

                observation, score, is_over, sso = game.step(current_action)
                total_score += score

                if is_over and game.info["sso"].gameWinner == "PLAYER_WINS":
                    results[f"OBFM_{agent_name}"]["game_won"][level_idx, rep] = 1

                if is_over:
                    break

            game.close()
            results[f"OBFM_{agent_name}"]["scores"][level_idx, rep] = total_score
            results[f"OBFM_{agent_name}"]["ticks"][level_idx, rep] = tick
            pbar.close()
            save_results(game_name, results)

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

    """
    agents = [RandomAgent(), RHEAObjectAgent(**RHEA_AGENT_PARAMETERS), BFSObjectAgent(**BFS_AGENT_PARAMETERS)]
    for game_name in evaluation_games:

        if not os.path.exists(f"results/{game_name}/models/ob_forward_model_RANDOM.txt"):
            print(f"game {game_name} cannot be evaluated yet, since the RANDOM model is not trained yet")
            continue
        if os.path.exists(f"results/{game_name}/constant_result_ob_lock_RANDOM.txt"):
            print(f"game {game_name} is evaluated by another thread")
            continue
        else:
            with open(f"results/{game_name}/constant_result_ob_lock_RANDOM.txt", "wb") as f:
                pickle.dump([0], f)

            print(f"evaluate game {game_name}")

        for agent, AGENT_NAME in zip(agents, ["Random", "RHEA", "BFS"]):
            if AGENT_NAME == "RHEA":
                continue
            forward_model = load_fm(game_name)
            agent.set_forward_model(forward_model)
            evaluate_agent(agent, AGENT_NAME, game_name=game_name, levels=[0, 1, 2, 3, 4], version=0)

        if os.path.exists(f"results/{game_name}/constant_result_ob_lock_RANDOM.txt"):
            os.remove(f"results/{game_name}/constant_result_ob_lock_RANDOM.txt")
    """


    for game_name in evaluation_games:

        if not os.path.exists(f"results/{game_name}/models/ob_forward_model_RANDOM.txt"):
            continue

        if not os.path.exists(f"results/{game_name}/obfm_model_evaluation_lock_BFS.txt"):
            with open(f"results/{game_name}/obfm_model_evaluation_lock_BFS.txt", "wb") as f:
                pickle.dump([0], f)

            print(f"processing {game_name}, BFS")

            obfm = load_models(game_name)

            for agent, agent_name in zip([BFSObjectAgent(**BFS_AGENT_PARAMETERS)], ["BFS"]):
                agent.set_forward_model(obfm)
                agent.set_score_model(obfm)
                evaluate_obfm(agent, game_name, agent_name)

            if os.path.exists(f"results/{game_name}/obfm_model_evaluation_lock_BFS.txt"):
                os.remove(f"results/{game_name}/obfm_model_evaluation_lock_BFS.txt")

        if not os.path.exists(f"results/{game_name}/obfm_model_evaluation_lock_RHEA.txt"):
            with open(f"results/{game_name}/obfm_model_evaluation_lock_RHEA.txt", "wb") as f:
                pickle.dump([0], f)

            print(f"processing {game_name}, RHEA")

            obfm = load_models(game_name)

            for agent, agent_name in zip([RHEAObjectAgent(**RHEA_AGENT_PARAMETERS)], ["RHEA"]):
                agent.set_forward_model(obfm)
                agent.set_score_model(obfm)
                evaluate_obfm(agent, game_name, agent_name)

            if os.path.exists(f"results/{game_name}/obfm_model_evaluation_lock_RHEA.txt"):
                os.remove(f"results/{game_name}/obfm_model_evaluation_lock_RHEA.txt")

        if not os.path.exists(f"results/{game_name}/obfm_model_evaluation_lock_MCTS.txt"):
            with open(f"results/{game_name}/obfm_model_evaluation_lock_MCTS.txt", "wb") as f:
                pickle.dump([0], f)

            print(f"processing {game_name}, MCTS")

            obfm = load_models(game_name)

            for agent, agent_name in zip([MCTSObjectAgent()], ["MCTS"]):
                agent.set_forward_model(obfm)
                agent.set_score_model(obfm)
                evaluate_obfm(agent, game_name, agent_name)

            if os.path.exists(f"results/{game_name}/obfm_model_evaluation_lock_MCTS.txt"):
                os.remove(f"results/{game_name}/obfm_model_evaluation_lock_MCTS.txt")

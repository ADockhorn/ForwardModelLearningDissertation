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
    with open(f"results/{game_name}/continuous_results_{AGENT_NAME}.txt", "rb") as f:
        return pickle.load(f)


def save_results(game_name, results):
    with open(f"results/{game_name}/continuous_results_{AGENT_NAME}.txt", "wb") as f:
        pickle.dump(results, f)


def continuously_train_model(agent, fm, game_name: str, levels: List[int], version: int, sm):
    logging.debug("train forward model")

    max_ticks = 2000
    repetitions = 20
    n_levels = 5

    if os.path.exists(f"results/{game_name}/continuous_results_{AGENT_NAME}.txt"):
        results = load_results(game_name)
        forward_model = results["forward_model"]
        score_model = results["score_model"]
    else:
        results = {"scores": np.zeros((n_levels, repetitions)),
                   "ticks": np.zeros((n_levels, repetitions)),
                   "game_won": np.zeros((n_levels, repetitions))}
    save_results(game_name, results)

    replays = dict()
    if os.path.exists(f"results/{game_name}/videos/replays_{AGENT_NAME}.txt"):
        with open(f"results/{game_name}/videos/replays_{AGENT_NAME}.txt", "rb") as f:
            replays = pickle.load(f)
    else:
        replays = {level: {rep: [] for rep in range(repetitions)} for level in range(n_levels)}

    for rep in range(repetitions):
        for level in tqdm(levels, desc="levels", ncols=100):
            if results["ticks"][level, rep] != 0:
                continue

            agent.re_initialize()
            agent._discount_factor = 0.95

            game = GVGAIEnvironment(game_name, level, version)

            observation, total_score, _, sso = game.reset()

            fig, axis = plt.subplots(1, 1)
            plt.axis("off")
            ims = []
            replays[level][rep] = [observation.get_grid()]

            previous_observation = None
            tick = 0
            for tick in trange(max_ticks, desc="ticks", ncols=100):
                ttl = axis.text(0.5, 1.01, f"{game_name} | total score = {total_score} | tick = {tick}",
                                horizontalalignment='center',
                                verticalalignment='bottom', transform=axis.transAxes)
                ims.append([plt.imshow(sso.image), ttl])

                if fm.is_trained():
                    current_action = agent.get_next_action(observation, game.get_actions())
                else:
                    current_action = random.choice(game.get_actions())

                observation, score, is_over, sso = game.step(current_action)
                replays[level][rep].append(observation.get_grid())
                total_score += score

                if previous_observation is not None and AGENT_NAME != "RANDOM":
                    fm.add_transition(previous_observation, current_action, observation.get_grid())
                    if not fm.is_trained() or np.any(observation.get_grid().flatten() != fm.predict(previous_observation, current_action)):
                        fm.fit()

                    if is_over and game.info["sso"].gameWinner == "PLAYER_WINS":
                        sm.add_transition(previous_observation, observation.get_grid(), score+1000)
                        results["game_won"][level, rep] = 1
                    else:
                        sm.add_transition(previous_observation, observation.get_grid(), score)
                    sm.fit()

                if is_over:
                    break

                previous_observation = observation.get_grid()

            with open(f"results/{game_name}/videos_{AGENT_NAME}/replays_{AGENT_NAME}.txt", "wb") as f:
                pickle.dump(replays, f)

            results["ticks"][level, rep] = tick
            results["scores"][level, rep] = total_score

            anim = animation.ArtistAnimation(fig, ims, interval=100, blit=False, repeat=False)
            anim.save(f'results/{game_name}/videos_{AGENT_NAME}/{rep*len(levels)+level}_DTRegressor_discounted_Continuous_{AGENT_NAME}.mp4')
            plt.close()
            game.close()

            agent.re_initialize()
            results["agent"] = agent
            results["score_model"] = sm
            results["forward_model"] = fm
            save_results(game_name, results)


if __name__ == "__main__":
    grid_based_games = []
    with open("data/GVGAI/grid-based-games.txt", "r") as file:  # Use file to refer to the file object
        for s in file.readlines():
            if len(s) > 1:
                grid_based_games.append(s[:-1])

    agents = [RandomAgent(), RHEAAgent(**RHEA_AGENT_PARAMETERS), BFSAgent(**BFS_AGENT_PARAMETERS)]

    # filter games that have too complex state representations and games that do not provide 5 levels
    evaluation_games = []
    for game in grid_based_games:
        n_levels = len([env_spec.id for env_spec in envs.registry.all() if env_spec.id.startswith(f"gvgai-{game}-")])
        if len(get_images(game)) > 25 or n_levels < 3:
            logging.info(f"game {game} was excluded")
            continue
        evaluation_games.append(game)

   # evaluation_games = ["decepticoins"] # ["bait", "decepticoins", "painter"]
    for game_name in tqdm(evaluation_games, desc="games", ncols=100):
        AGENT_NAME = "RHEA"
        #agent = BFSAgent(**BFS_AGENT_PARAMETERS)
        #agent = RandomAgent()
        agent = RHEAAgent(**RHEA_AGENT_PARAMETERS)

        # setup file paths for the results
        if not os.path.exists(f"results/{game_name}/"):
            os.mkdir(f"results/{game_name}/")
        if not os.path.exists(f"results/{game_name}/videos_{AGENT_NAME}"):
            os.mkdir(f"results/{game_name}/videos_{AGENT_NAME}")
        if os.path.exists(f"results/{game_name}/continuous_results_lock_{AGENT_NAME}.txt"):
            continue
        else:
            with open(f"results/{game_name}/continuous_results_lock_{AGENT_NAME}.txt", "wb") as f:
                pickle.dump([0], f)

        print(f"processing {game_name}")

        forward_model = LocalForwardModel(DecisionTreeClassifier(), SquareNeighborhoodPattern(3),
                                          possibleObservations=np.append(
                                              np.array(list(get_object_dict(game_name).values())),
                                              np.array(["0", "1", "2", "3", "4", "5", "x"])))
        score_model = GlobalScoreModel(possible_observations=np.append(np.array(list(get_object_dict(game_name).values())),
                                                                       np.array(["0", "1", "2", "3", "4", "5", "x"])))

        agent.set_forward_model(forward_model)
        agent.set_score_model(score_model)

        continuously_train_model(agent, forward_model, game_name=game_name, levels=[0, 1, 2, 3, 4], version=0,
                                 sm=score_model)

        if os.path.exists(f"results/{game_name}/continuous_results_lock_{AGENT_NAME}.txt"):
            os.remove(f"results/{game_name}/continuous_results_lock_{AGENT_NAME}.txt")

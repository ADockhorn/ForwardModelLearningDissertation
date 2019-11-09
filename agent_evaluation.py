import gym
import gym_gvgai
import matplotlib.pyplot as plt
import numpy as np

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier

from abstractclasses.AbstractNeighborhoodPattern import CrossNeighborhoodPattern
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


def load_results(game_name: str):
    with open(f"results/{game_name}/results.txt", "rb") as f:
        return pickle.load(f)


def save_results(game_name, results):
    with open(f"results/{game_name}/results.txt", "wb") as f:
        pickle.dump(results, f)


def initialize_results(game, n_levels, repetitions):
    # load previous results or initialize new result file
    if os.path.exists(f"results/{game}/results.txt"):
        results = load_results(game)
    else:
        results = {"forward_model": None,
                   "score_model": None,
                   "win_model": None,
                   "scores": {agent.get_agent_name(): np.zeros((n_levels, repetitions)) for agent in agents},
                   "ticks": {agent.get_agent_name(): np.zeros((n_levels, repetitions)) for agent in agents},
                   "game_won": {agent.get_agent_name(): np.zeros((n_levels, repetitions)) for agent in agents}}

    # if
    if results["forward_model"] is None or results["score_model"] is None:
        logging.info("train new forward model")
        forward_model = LocalForwardModel(DecisionTreeClassifier(), CrossNeighborhoodPattern(2),
                                          possibleObservations=np.append(
                                              np.array(list(get_object_dict(game).values())),
                                              np.array(["0", "1", "2", "3", "4", "5", "x"])))
        score_model = GlobalScoreModel(possible_observations=np.append(np.array(list(get_object_dict(game).values())),
                                                                       np.array(["0", "1", "2", "3", "4", "5", "x"])))

        train_model(forward_model, game, levels=[0, 1, 2], version=0, rep=3, ticks=200, sm=score_model)
        results["forward_model"] = forward_model
        results["score_model"] = score_model
        save_results(game, results)

    return results


def evaluate_game_playing_performance(agent, game, n_levels, results, visualize_result=True):
    agent_name = agent.get_agent_name()

    for level in trange(n_levels, desc="levels", ncols=100):
        for rep in trange(REPETITIONS, desc="repetitions", ncols=100):

            if results["game_won"][agent_name][level, rep] != 0:
                continue

            tick = 0
            env = GVGAIEnvironment(game, level, 0)
            grid, total_score, _, sso = env.reset()
            if visualize_result:
                fig, axis = plt.subplots(1, 1)
                plt.axis("off")
                ims = []

                for tick in trange(MAX_TICKS, desc="game ticks", ncols=100):
                    ttl = axis.text(0.5, 1.01, f"{game} | total score = {total_score} | tick = {tick}",
                                    horizontalalignment='center',
                                    verticalalignment='bottom', transform=axis.transAxes)
                    ims.append([plt.imshow(sso.image), ttl])

                    grid, score, is_done, sso = env.step(agent.get_next_action(grid, env.get_actions()))
                    total_score += score
                    if is_done:
                        results["game_won"][agent_name][level, rep] = 1
                        ims.append([plt.imshow(sso.image), ttl])
                        break
                else:
                    results["game_won"][agent_name][level, rep] = -1

                anim = animation.ArtistAnimation(fig, ims, interval=100, blit=False, repeat=False)
                anim.save(f'results/{game}/videos/{level}_{rep}_{agent_name.replace(" ", "_")}.mp4')
                plt.close()
            else:
                for tick in trange(MAX_TICKS, desc="game ticks", ncols=100):
                    grid, score, is_done, sso = env.step(agent.get_next_action(grid, env.get_actions()))
                    total_score += score
                    if is_done:
                        results["game_won"][agent_name][level, rep] = 1
                        break
                else:
                    results["game_won"][agent_name][level, rep] = -1

            results["ticks"][agent_name][level, rep] = tick
            results["scores"][agent_name][level, rep] = total_score
            env.close()
            save_results(game, results)
        break


if __name__ == "__main__":
    logging.basicConfig(filename='game-playing-results.log', filemode='a',
                        format='%(name)s - %(levelname)s - %(message)s')
    logging.info("starting evaluation")

    # evaluation setup
    REPETITIONS = 10
    MAX_TICKS = 100

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

    # evaluate algorithm on remaining games
    for game in tqdm(evaluation_games, desc="games", ncols=100):
        n_levels = len([env_spec.id for env_spec in envs.registry.all() if env_spec.id.startswith(f"gvgai-{game}-")])

        # setup file paths for the results
        if not os.path.exists(f"results/{game}/"):
            os.mkdir(f"results/{game}/")
            os.mkdir(f"results/{game}/videos")

        results = initialize_results(game, n_levels, REPETITIONS)
        forward_model = results["forward_model"]
        score_model = results["score_model"]

        results["game_won"]["BFS Agent"] = np.zeros((n_levels, REPETITIONS))

        # evaluate game
        logging.info(f"evaluate {game}")
        for agent in tqdm(agents, desc="agents", ncols=100):
            agent.set_forward_model(forward_model)
            agent.set_score_model(score_model)

            evaluate_game_playing_performance(agent, game, n_levels, results)

        break
    print("evaluation done")

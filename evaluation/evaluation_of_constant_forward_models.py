import os
import pickle
from gym import envs
from games.GVGAIConstants import get_images
import logging
import gym
import gym_gvgai
import numpy as np


if __name__ == "__main__":
    os.chdir("/".join(os.getcwd().split("/")[:-1]))

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


    game_results = {game: dict() for game in evaluation_games}

    for game in evaluation_games:
        if os.path.exists(f"results/{game}/constant_result_ob_RANDOM.txt"):
            with open(f"results/{game}/constant_result_ob_RANDOM.txt", "rb") as f:
                results = pickle.load(f)
            # print(game, results["BFS"]["ticks"])
            valid = results["BFS"]["ticks"] > 0
            if np.sum(valid) == 50:
                print(game, "done")
            else:
                #print(game, "not done")
                pass
            #print(game, np.mean(results["BFS"]["scores"][valid]) / np.mean(results["Random"]["scores"]))
            #if sum(sum(results["BFS"]["ticks"] > 0)) == 50:
            #    print(game, "completely done")
            #print(game, sum(sum(results["BFS"]["ticks"] > 0)))
        else:
            #print(game, "not even started yet")
            pass

    # load results of a random agent playing all levels
    for game in evaluation_games:
        if os.path.exists(f"results/{game}/continuous_results_RANDOM.txt"):
            with open(f"results/{game}/continuous_results_RANDOM.txt", "rb") as f:
                results = pickle.load(f)
            if results["ticks"][-1, -1] > 0:
                print(game, "done")
            else:
                print(game, "not done yet")
        else:
            print(game, "not even started yet")

    # load results of a LFM BFS Agent continuous Learning
    for game in evaluation_games:
        if os.path.exists(f"results/{game}/continuous_results_BFS.txt"):
            with open(f"results/{game}/continuous_results_BFS.txt", "rb") as f:
                results = pickle.load(f)
            if results["ticks"][4][10] > 0:
                print(game, "done")
            else:
                print(game, "not done yet")
        else:
            print(game, "not even started yet")

    # load results of a OB BFS Agent continuous Learning
    for game in evaluation_games:
        if os.path.exists(f"results/{game}/training_results/continuous_ob_training_results_BFS.txt"):
            with open(f"results/{game}/training_results/continuous_ob_training_results_BFS.txt", "rb") as f:
                results = pickle.load(f)
            if results["ticks"][4][10] > 0:
                print(game, "done")
            else:
                print(game, "not done yet")
        else:
            print(game, "not even started yet")

    # load results of a OB BFS Agent continuous Learning
    for game in evaluation_games:
        if os.path.exists(f"results/{game}/training_results/continuous_lfm_training_results_BFS.txt"):
            with open(f"results/{game}/training_results/continuous_lfm_training_results_BFS.txt", "rb") as f:
                results = pickle.load(f)
            if results["ticks"][4][10] > 0:
                print(game, "done")
            else:
                print(game, "not done yet")
        else:
            print(game, "not even started yet")
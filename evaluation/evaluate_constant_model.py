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


    ranks = [[0]*4, [0]*4, [0]*4, [0]*4]
    points = [0]*4
    index = {"Random": 0, "LFM_BFS": 1, "LFM_RHEA": 2, "OBFM_BFS": 3}
    for i, game in enumerate(evaluation_games):
        results = dict()

        if os.path.exists(f"results/{game}/constant_result_ob_RANDOM.txt"):
            with open(f"results/{game}/constant_result_ob_RANDOM.txt", "rb") as f:
                results_random = pickle.load(f)
            results["Random"] = (np.mean(results_random["Random"]["game_won"]),
                                 np.mean(results_random["Random"]["scores"]),
                                 np.mean(results_random["Random"]["ticks"]))

            if os.path.exists(f"results/{game}/training_results/constant_lfm_BFS.txt"):
                with open(f"results/{game}/training_results/constant_lfm_BFS.txt", "rb") as f:
                    results_bfs = pickle.load(f)
                valid = results_bfs["LFM_BFS"]["ticks"] > 0
                results["LFM_BFS"] = (np.mean(results_bfs["LFM_BFS"]["game_won"][valid]),
                                      np.mean(results_bfs["LFM_BFS"]["scores"][valid]),
                                      np.mean(results_bfs["LFM_BFS"]["ticks"][valid]))

            if os.path.exists(f"results/{game}/training_results/constant_lfm_RHEA.txt"):
                with open(f"results/{game}/training_results/constant_lfm_RHEA.txt", "rb") as f:
                    results_rhea = pickle.load(f)
                valid = results_rhea["LFM_RHEA"]["ticks"] > 0
                results["LFM_RHEA"] = (np.mean(results_rhea["LFM_RHEA"]["game_won"][valid]),
                                      np.mean(results_rhea["LFM_RHEA"]["scores"][valid]),
                                      np.mean(results_rhea["LFM_RHEA"]["ticks"][valid]))

            if "BFS" in results_random:
                valid = results_random["BFS"]["ticks"] > 0
                results["OBFM_BFS"] = (np.mean(results_random["BFS"]["game_won"][valid]),
                                       np.mean(results_random["BFS"]["scores"][valid]),
                                       np.mean(results_random["BFS"]["ticks"][valid]))
            """
            print(game)
            for agent in results:
                print(" & ".join([agent] + [str(round(x, 2)) for x in results[agent]]) + " \\\\")

            print()
            print()"""

            res = [[x] + [round(y,2) for y in results[x]] for x in results]
            o = sorted(range(len(res)), key=lambda k: (res[k][1], res[k][2], res[k][3]), reverse=True)
            print(game, [res[x][0] for x in o])

            for p, x in zip([25, 18, 15, 12], o):
                #print(points, res[x][0])
                points[index[res[x][0]]] += p

            for i, x in enumerate(o):
                #print(i, x)
                ranks[index[res[x][0]]][i] += 1
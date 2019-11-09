import pickle
import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from games.GVGAIConstants import get_object_dict, get_images
from gym import envs
import gym
import gym_gvgai


def load_grid_search_results_agent(game_name, agent):
    with open(f"results/{game_name}/continuous_results{agent}.txt", "rb") as f:
        return pickle.load(f)

def load_grid_search_results(game_name):
    with open(f"results/{game_name}/continuous_results.txt", "rb") as f:
        return pickle.load(f)


if __name__ == "__main__":
    os.chdir("/".join(os.getcwd().split("/")[:-1]))

    grid_based_games = []
    with open("data/GVGAI/grid-based-games.txt", "r") as file:  # Use file to refer to the file object
        for s in file.readlines():
            if len(s) > 1:
                grid_based_games.append(s[:-1])
    print(grid_based_games)

    # filter games that have too complex state representations and games that do not provide 5 levels
    evaluation_games = []
    for game in grid_based_games:
        n_levels = len([env_spec.id for env_spec in envs.registry.all() if env_spec.id.startswith(f"gvgai-{game}-")])
        if len(get_images(game)) > 25 or n_levels < 3:
            continue
        if not os.path.exists(f"results/{game}/grid_search.txt"):
            continue
        evaluation_games.append(game)

    games = evaluation_games
    print(games)

    for game in games:
        game = "catapults"
        results_random = load_grid_search_results_random(game)
        results_bfs = load_grid_search_results(game)

        plt.plot(results_random["ticks"].flatten(), label="Random")
        plt.plot(results_bfs["ticks"].flatten(), label="BFS")
        plt.legend()
        plt.show()

        plt.plot(results_random["game_won"].flatten(), label="Random")
        plt.plot(results_bfs["game_won"].flatten(), label="BFS")
        plt.legend()
        plt.show()

        plt.plot(results_random["scores"].flatten() / results_random["ticks"].flatten(), label="Random")
        plt.plot(results_bfs["scores"].flatten() / results_bfs["ticks"].flatten(), label="BFS")
        plt.legend()
        plt.show()

        for i in range(5):
            print(np.mean(results_random["game_won"][i]), np.mean(results_bfs["game_won"][i]))


            plt.scatter(results_random["scores"][i], results_random["ticks"][i])
            plt.scatter(results_bfs["scores"][i], results_bfs["ticks"][i])
            plt.show()
        print()
        break


    points = []
    wins = {"BFS": [], "RHEA": [], "RANDOM": []}
    for game in games:
        results_random = load_grid_search_results_random(game)
        points.append(np.sum(results_random["scores"]) / np.sum(results_random["ticks"]))
        wins.append(np.mean(results_random["game_won"]))
        break
    plt.scatter(range(len(games)), points)
    plt.scatter(range(len(games)), wins)
    plt.show()

    sns.heatmap(np.array([points, wins]), linewidths=.5, square=True)
    plt.show()

    game = "bait"
    results_bfs = load_grid_search_results_agent(game, "")
    results_random = load_grid_search_results_agent(game, "_RANDOM")
    results_rhea = load_grid_search_results_agent(game, "_RHEA")
    wins = {"BFS": [], "RHEA": [], "RANDOM": []}

    plt.subplot()
    for level in range(5):
        for data, name in zip([results_random, results_bfs, results_rhea], ["Random", "BFS", "RHEA"]):
            plt.plot([np.mean(data["game_won"][level][(i * 4):(((i + 1) * 4))]) for i in range(5)], label=name)
        plt.legend()
        plt.show()

    [results_bfs["scores"][0][(i * 4):(((i + 1) * 4))] for i in range(5)]
    [results_bfs["ticks"][0][(i * 4):(((i + 1) * 4))] for i in range(5)]
    [results_bfs["scores"][0][(i * 4):(((i + 1) * 4))] / results_bfs["ticks"][0][(i * 4):(((i + 1) * 4))] for i in range(5)]

    for level in range(5):
        for data, name in zip([results_random, results_bfs, results_rhea], ["Random", "BFS", "RHEA"]):
            plt.plot([np.mean(data["scores"][level][(i * 4):(((i + 1) * 4))] / data["ticks"][level][(i * 4):(((i + 1) * 4))]) for i in range(5)], label=name)
        plt.title(f"level {level}")
        plt.legend()
        plt.show()

    win_matrix = []

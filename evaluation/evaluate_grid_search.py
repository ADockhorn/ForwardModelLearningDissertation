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


def load_grid_search_results(game_name):
    with open(f"results/{game_name}/grid_search.txt", "rb") as f:
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
    """
    for game in games:
        data = load_grid_search_results(game)

        plt.style.use('bmh')
        fig = plt.figure(figsize=(15, 4))
        from matplotlib import gridspec

        gs = gridspec.GridSpec(1, 2, width_ratios=[5, 9])
        ax1 = plt.subplot(gs[0])

        alg_data = {alg: np.array([x["mean_test_score"] for x in data[alg]["grid_search"]]).flatten() for alg in data}
        dataset_data = {i: np.concatenate([data[alg]["grid_search"][i]["mean_test_score"] for alg in data]) for i in
                        range(9)}

        ax1.set_facecolor("w")
        #ax.tick_params(direction='out', length=6, width=10, colors='r',
        #               grid_color='r', grid_alpha=0.5)
        plt.vlines(range(5), 0.0, 1.05, linestyles="dashed", colors="0.7", linewidth=1.5)
        sns.violinplot(data=np.array([alg_data[x] for x in alg_data]).transpose(), inner="quart", cut=0, color="0.6",
                       linewidth=1.5,  width=1.0, scale="area", ax=ax1)
        sns.despine()
        ax1.set_yticks([i * 0.2 for i in range(6)])
        ax1.set_xticks(np.arange(5))
        ax1.set_xticklabels([alg for alg in data], rotation=45, ha="right")
        plt.ylim((0, 1.05))
        ax1.yaxis.grid(True, which='major')
        ax1.tick_params(which='major', length=5, direction="out", width=1.5, color="0.7")

        ax2 = plt.subplot(gs[1])
        ax2.set_facecolor("w")
        plt.vlines(range(9), 0.0, 1.05, linestyles="dashed", colors="0.7", linewidth=1.5)

        sns.violinplot(data=np.array([dataset_data[i] for i in range(9)]).transpose(), inner="quart", cut=0, color="0.6",
                       linewidth=1.5,  width=0.8, scale="area", ax=ax2)
        sns.despine()
        ax2.set_yticks([i * 0.2 for i in range(6)])
        plt.gca().set_xticks(np.arange(9))
        plt.ylim((0, 1.05))
        ax2.yaxis.grid(True, which='major')
        ax2.tick_params(which='major', length=5, direction="out", width=1.5, color="0.7")
        ax2.set_xticklabels([f"Cross Pattern {i}" for i in range(1, 4)] +
                            [f"Square Pattern {i}" for i in range(1, 4)] +
                            [f"Diamond Pattern {i}" for i in range(1, 4)], rotation=45, ha="right")
        #plt.title(f"average data set performance - {game}")
        plt.ylim((0, 1.05))

        plt.tight_layout()
        #plt.title(f"average algorithm performance - {game}")
        plt.savefig(f"results/algorithm-and-dataset-performance-{game}.pdf")
        #plt.savefig(f"results/algorithm-and-dataset-performance-{game}.png")
        plt.show()


    grid_search_results = {game: load_grid_search_results(game) for game in evaluation_games}
    plt.style.use('bmh')
    fig = plt.figure(figsize=(15, 4))
    from matplotlib import gridspec
    gs = gridspec.GridSpec(1, 2, width_ratios=[5, 9])
    ax1 = plt.subplot(gs[0])
    data = load_grid_search_results(game)

    alg_data = {alg: [] for alg in data}
    [alg_data[alg].append(np.array([x["mean_test_score"] for x in grid_search_results[game][alg]["grid_search"]]).flatten()) for game in grid_search_results for alg in grid_search_results[game]]
    alg_data = {alg: np.concatenate(alg_data[alg]) for alg in alg_data}
    dataset_data = {i: [] for i in range(9)}
    [dataset_data[i].append(grid_search_results[game][alg]["grid_search"][i]["mean_test_score"]) for game in grid_search_results for alg in grid_search_results[game] for i in range(9) ]
    dataset_data = {i: np.concatenate(dataset_data[i]) for i in range(9)}


    sns.violinplot(data=np.array([alg_data[x] for x in alg_data]).transpose(), inner="quart", cut=0, color="0.7",
                   linewidth=1.5,  width=1.0, scale="area")
    ax = plt.gca()
    ax.set_facecolor("w")
    plt.vlines(range(5), 0.0, 1.05, linestyles="dashed", colors="0.7", linewidth=1.5)

    sns.despine()
    ax.set_yticks([i * 0.2 for i in range(6)])
    plt.gca().set_xticks(np.arange(5))
    plt.gca().set_xticklabels([alg for alg in data], rotation=45, ha="right")
    plt.ylim((0, 1.05))
    ax.yaxis.grid(True, which='major')
    ax.tick_params(which='major', length=5, direction="out", width=1.5, color="0.7")

    ax2 = plt.subplot(gs[1])
    sns.violinplot(data=np.array([dataset_data[i] for i in range(9)]).transpose(), inner="quart", cut=0, color="0.7",
                   linewidth=1.5,  width=0.8, scale="area", ax=ax2)
    ax = plt.gca()
    ax.set_facecolor("w")
    plt.vlines(range(9), 0.0, 1.05, linestyles="dashed", colors="0.7", linewidth=1.5)

    sns.despine()
    ax.set_yticks([i * 0.2 for i in range(6)])
    plt.gca().set_xticks(np.arange(9))
    plt.ylim((0, 1.05))
    ax.yaxis.grid(True, which='major')
    ax.tick_params(which='major', length=5, direction="out", width=1.5, color="0.7")
    plt.gca().set_xticklabels([f"Cross Pattern {i}" for i in range(1, 4)] +
                              [f"Square Pattern {i}" for i in range(1, 4)] +
                              [f"Diamond Pattern {i}" for i in range(1, 4)], rotation=45, ha="right")
    #plt.title(f"average data set performance - {game}")
    plt.ylim((0, 1.05))
    plt.tight_layout()
    plt.savefig(f"results/average-algorithm-and-dataset-performance.pdf")
    plt.savefig(f"results/average-algorithm-and-dataset-performance.png")
    plt.show()
    """

    best_per_game = []
    for game in games:
        data = load_grid_search_results(game)
        best = (0, None)
        for alg in data:
            if data[alg]["best_mean_accuracy"] > best[0]:
                best = (data[alg]["best_mean_accuracy"], alg, data[alg]["best_parameters"], data[alg]["best_data_set"])
        print(f"{game} & {best[1]} & {best[2]} & {best[3]} & {best[0].round(2)} \\\\")
        best_per_game.append(best[0])

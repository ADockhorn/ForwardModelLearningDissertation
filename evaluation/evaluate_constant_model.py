import os
import pickle
from gym import envs
from games.GVGAIConstants import get_images
import logging
import gym
import gym_gvgai
import numpy as np
from figures.plot_gameplay_results import annotate_heatmap, heatmap


if __name__ == "__main__":
    os.chdir("/".join(os.getcwd().split("/")[:-1]))

    grid_based_games = []
    with open("data/GVGAI/grid-based-games.txt", "r") as file:  # Use file to refer to the file object
        for s in file.readlines():
            if len(s) > 1:
                grid_based_games.append(s[:-1])

    evaluation_games = []
    for game in grid_based_games:
        if game in {"cookmepasta", "brainman"}:
            continue
        n_levels = len([env_spec.id for env_spec in envs.registry.all() if env_spec.id.startswith(f"gvgai-{game}-")])
        if len(get_images(game)) > 25 or n_levels < 3:
            logging.info(f"game {game} was excluded")
            continue
        evaluation_games.append(game)

    ranks = [[0]*5, [0]*5, [0]*5, [0]*5, [0]*5]
    points = [0]*5
    index = {"Random": 0, "LFM_BFS": 1, "LFM_RHEA": 2, "OBFM_BFS": 3, "OBFM_RHEA": 4}
    game_results = np.zeros((30, 5))

    for i, game in enumerate(evaluation_games):

        results = dict()

        if os.path.exists(f"results/{game}/constant_result_ob_RANDOM.txt"):
            with open(f"results/{game}/constant_result_ob_RANDOM.txt", "rb") as f:
                results_random = pickle.load(f)
            results["Random"] = (np.mean(results_random["Random"]["game_won"]),
                                 np.mean(results_random["Random"]["scores"]),
                                 np.mean(results_random["Random"]["ticks"]))

        elif os.path.exists(f"results/{game}/continuous_results_RANDOM.txt"):
            with open(f"results/{game}/continuous_results_RANDOM.txt", "rb") as f:
                results_random = pickle.load(f)
            results["Random"] = (np.mean(results_random["game_won"]),
                                 np.mean(results_random["scores"]),
                                 np.mean(results_random["ticks"]))

        if "Random" in results:
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

            if os.path.exists(f"results/{game}/training_results/constant_obfm_BFS.txt"):
                with open(f"results/{game}/training_results/constant_obfm_BFS.txt", "rb") as f:
                    results_bfs = pickle.load(f)
                valid = results_bfs["OBFM_BFS"]["ticks"] > 0
                results["OBFM_BFS"] = (np.mean(results_bfs["OBFM_BFS"]["game_won"][valid]),
                                       np.mean(results_bfs["OBFM_BFS"]["scores"][valid]),
                                       np.mean(results_bfs["OBFM_BFS"]["ticks"][valid]))

            if os.path.exists(f"results/{game}/training_results/constant_obfm_RHEA.txt"):
                with open(f"results/{game}/training_results/constant_obfm_RHEA.txt", "rb") as f:
                    results_rhea = pickle.load(f)
                valid = results_rhea["OBFM_RHEA"]["ticks"] > 0
                results["OBFM_RHEA"] = (np.mean(results_rhea["OBFM_RHEA"]["game_won"][valid]),
                                        np.mean(results_rhea["OBFM_RHEA"]["scores"][valid]),
                                        np.mean(results_rhea["OBFM_RHEA"]["ticks"][valid]))
            """
            print(game)
            for agent in results:
                print(" & ".join([agent] + [str(round(x, 2)) for x in results[agent]]) + " \\\\")

            print()
            print()"""

            res = [[x] + [round(y, 2) for y in results[x]] for x in results]
            o = sorted(range(len(res)), key=lambda k: (res[k][1], res[k][2], res[k][3]), reverse=True)
            print(game, [res[x][0] for x in o])

            for p, x in zip([25, 18, 15, 12, 10], o):
            ##for p, x in zip([5, 4, 3, 2, 1], o):
                #print(points, res[x][0])
                points[index[res[x][0]]] += p

            for j, x in enumerate(o):
                #print(i, x)
                ranks[index[res[x][0]]][j] += 1
                game_results[i, index[res[x][0]]] = j
    print(ranks)
    print(points)

    import matplotlib.pyplot as plt

    import matplotlib.font_manager as font_manager
    plt.rc('pgf', texsystem='lualatex')
    plt.rc('text', usetex=True)
    plt.rc('text.latex', preamble=r'\usepackage{amsmath}\usepackage{kmath}\usepackage{kerkis}\renewcommand\sfdefault\rmdefault')
    font_path = '/home/alex/fonts/kerkis.ttf'
    prop = font_manager.FontProperties(fname=font_path)


    grid = dict(height_ratios=[5], width_ratios=[15])
    fig, ax = plt.subplots(ncols=1, nrows=1, gridspec_kw = grid)
    fig.set_figheight(4)
    fig.set_figwidth(10)
    im, cbar = heatmap(game_results[0:15, :].transpose()+1, ["Random", "LFM-BFS", "LFM-RHEA", "OBFM-BFS", "OBFM-RHEA"],
                       evaluation_games[:15], ax=ax, vmin=1, vmax=5, cbar=False, cmap=plt.cm.get_cmap('viridis_r', 5),
                       cbar_kw={"ticks": [1, 2, 3, 4, 5]})
    annotate_heatmap(im, game_results[:15, :].transpose()+1, valfmt="{x:1.0f}", threshold=3, threshold2=10)
    plt.savefig("figures/game-playing/agent-ranks-games-1-15.pdf")
    plt.savefig("figures/game-playing/agent-ranks-games-1-15.png")
    plt.show()

    grid = dict(height_ratios=[5], width_ratios=[15])
    fig, ax = plt.subplots(ncols=1, nrows=1, gridspec_kw = grid)
    fig.set_figheight(4)
    fig.set_figwidth(10)
    im, cbar = heatmap(game_results[15:, :].transpose()+1, ["Random", "LFM-BFS", "LFM-RHEA", "OBFM-BFS", "OBFM-RHEA"],
                       evaluation_games[15:], ax=ax, vmin=1, vmax=5, cbar=False, cmap=plt.cm.get_cmap('viridis_r', 5),
                       cbar_kw={"ticks": [1, 2, 3, 4, 5]})
    annotate_heatmap(im, game_results[15:, :].transpose()+1, valfmt="{x:1.0f}", threshold=3, threshold2=10)
    plt.savefig("figures/game-playing/agent-ranks-games-16-30.pdf")
    plt.savefig("figures/game-playing/agent-ranks-games-16-30.png")
    plt.show()

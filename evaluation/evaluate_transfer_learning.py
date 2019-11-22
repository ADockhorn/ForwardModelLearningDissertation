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

    print("\\begin{table}")
    print("\\caption{Transfer-learning performance per agent}")
    print("\\label{app:transfer-learning-results-per-game}")
    for i, game in enumerate(evaluation_games):
        if os.path.exists(f"results/{game}/constant_result_ob_RANDOM.txt"):
            with open(f"results/{game}/transfer_learning_model_evaluation.txt", "rb") as f:
                results_transfer = pickle.load(f)

            with open(f"results/{game}/constant_result_ob_RANDOM.txt", "rb") as f:
                results_random = pickle.load(f)
            results_transfer["Random"] = {"scores": results_random["Random"]["scores"][3:],
                                          "ticks": results_random["Random"]["ticks"][3:],
                                          "game_won": results_random["Random"]["game_won"][3:]}


            # print(game, results["BFS"]["ticks"])
            for agent in results_transfer:
                valid = results_transfer[agent]["ticks"] > 0
                results_transfer[agent]["average"] = (np.mean(results_transfer[agent]["game_won"][valid]),
                                                      np.mean(results_transfer[agent]["scores"][valid]),
                                                      np.mean(results_transfer[agent]["ticks"][valid]))

            if "LFM_BFS" in results_transfer and "OBFM_BFS" in results_transfer:
                print("""\\begin{subtable}{.48\\textwidth}
\\resizebox{\\textwidth}{!}{%
\\begin{tabular}{lccc}
    \\toprule
    agent & win-rate & score & ticks\\\\
    \midrule +
    Random & """ + " & ".join([str(x) for x in results_transfer["Random"]["average"]]) + """\\\\
    BFS-LFM & """ + " & ".join([str(x) for x in results_transfer["LFM_BFS"]["average"]]) +  """\\\\
    BFS-OBFM & """  + " & ".join([str(x) for x in results_transfer["OBFM_BFS"]["average"]]) +  """\\\\
    \\bottomrule
\end{tabular}
}
\subcaption{"""+game+"""}%
\end{subtable}"""
                )
            else:
                print("""\\begin{subtable}{.48\\textwidth}
\\resizebox{\\textwidth}{!}{%
\\begin{tabular}{lccc}
    \\toprule
    agent & win-rate & score & ticks\\\\
    \midrule +
    Random & """ + " & ".join([str(x) for x in results_transfer["Random"]["average"]]) + """\\\\
    BFS-LFM & """ + " & ".join([str(x) for x in results_transfer["LFM_BFS"]["average"]]) + """\\\\
    \\bottomrule
\end{tabular}
}
\subcaption{""" + game + """}%
\end{subtable}"""
                )
            if i % 2 == 1:
                print("")

    print("\\end{table}")

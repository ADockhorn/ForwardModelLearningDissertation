from gym import envs
from games.gvgai_environment import train_model
from games.GVGAIConstants import get_images, get_object_dict
import os
import pickle


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
            continue
        evaluation_games.append(game)

    for game in evaluation_games:
        if os.path.exists(f"results/{game}/continuous_results.txt"):
            with open(f"results/{game}/continuous_results.txt", "rb") as f:
                results = pickle.load(f)
                if results["ticks"][-1][-1] != 0:
                    fm = results["forward_model"]
                    fm._data_set = None
                    with open(f"results/{game}/forward_model.txt", "wb") as fmf:
                        pickle.dump(fm, fmf)

                    sm = results["score_model"]
                    sm._data_set = None
                    with open(f"results/{game}/score_model.txt", "wb") as smf:
                        pickle.dump(sm, smf)

        if os.path.exists(f"results/{game}/continuous_learning.txt"):
            with open(f"results/{game}/continuous_learning.txt", "rb") as results_file:
                combined = pickle.load(results_file)
        else:
            combined = dict()
        if os.path.exists(f"results/{game}/continuous_results_RHEA.txt"):
            with open(f"results/{game}/continuous_results_RHEA.txt", "rb") as f:
                results = pickle.load(f)
                if results["ticks"][-1][-1] != 0:
                    results.pop("forward_model", None)
                    results.pop("score_model", None)
                    results.pop("agent", None)
                    combined["RHEA"] = results

        if os.path.exists(f"results/{game}/continuous_results_RANDOM.txt"):
            with open(f"results/{game}/continuous_results_RANDOM.txt", "rb") as f:
                results = pickle.load(f)
                if results["ticks"][-1][-1] != 0:
                    results.pop("forward_model", None)
                    results.pop("score_model", None)
                    results.pop("agent", None)
                    combined["Random"] = results

        if os.path.exists(f"results/{game}/continuous_results.txt"):
            with open(f"results/{game}/continuous_results.txt", "rb") as f:
                results = pickle.load(f)
                if results["ticks"][-1][-1] != 0:
                    results.pop("forward_model", None)
                    results.pop("score_model", None)
                    results.pop("agent", None)
                    combined["BFS"] = results

        with open(f"results/{game}/continuous_learning.txt", "wb") as results_file:
            pickle.dump(combined, results_file)
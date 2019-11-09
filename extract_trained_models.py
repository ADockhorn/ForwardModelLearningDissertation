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
        if os.path.exists(f"results/{game}/continuous_results.txt") and \
                os.path.exists(f"results/{game}/videos/100_DTRegressor_discounted_ContinuousBFS.mp4"):
            with open(f"results/{game}/continuous_results.txt", "rb") as f:
                results = pickle.load(f)

                fm = results["forward_model"]
                fm._data_set = None
                with open(f"results/{game}/forward_model.txt", "wb") as fmf:
                    pickle.dump(fm, fmf)

                sm = results["score_model"]
                sm._data_set = None
                with open(f"results/{game}/score_model.txt", "wb") as smf:
                    pickle.dump(sm, smf)

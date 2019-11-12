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
        if not os.path.exists(f"results/{game}/models/"):
            os.mkdir(f"results/{game}/models/")

        if os.path.exists(f"results/{game}/ob_continuous_results_RANDOM.txt") and not os.path.exists(f"results/{game}/ob_continuous_results_lock_RANDOM.txt"):
            with open(f"results/{game}/ob_continuous_results_RANDOM.txt", "rb") as f:
                print(game)
                results = pickle.load(f)
                fm = results["forward_model"]
                fm.training_data = None
                fm.score_training_data = None

                with open(f"results/{game}/models/ob_forward_model_RANDOM.txt", "wb") as fmf:
                    pickle.dump(fm, fmf)

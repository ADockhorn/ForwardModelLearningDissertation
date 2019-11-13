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

    # continuous random model
    print("extract object-based forward models learned by a random agent")
    for game in evaluation_games:
        if not os.path.exists(f"results/{game}/models/"):
            os.mkdir(f"results/{game}/models/")

        if os.path.exists(f"results/{game}/ob_continuous_results_RANDOM.txt"):
            with open(f"results/{game}/ob_continuous_results_RANDOM.txt", "rb") as f:
                results = pickle.load(f)

                training_results = dict()
                training_results["scores"] = results["scores"]
                training_results["ticks"] = results["ticks"]
                training_results["game_won"] = results["game_won"]
                if not os.path.exists(f"results/{game}/training_results/"):
                    os.mkdir(f"results/{game}/training_results/")
                with open(f"results/{game}/training_results/continuous_ob_training_results_RANDOM.txt", "wb") as file:
                    pickle.dump(training_results, file)

                if results["ticks"][-1, -1] != 0:
                    if not os.path.exists(f"results/{game}/ob_continuous_results_lock_RANDOM.txt"):
                        print(game, "is not done with training, but no lock exists")
                    continue
                else:
                    print(game, "extract continuous learning forward model")

                fm = results["forward_model"]
                fm.training_data = None
                fm.score_training_data = None

                with open(f"results/{game}/models/ob_forward_model_RANDOM.txt", "wb") as fmf:
                    pickle.dump(fm, fmf)
        else:
            print(game, "random ob forward model is not done with training")

    print()
    print("extract object-based forward models learned by a BFS agent")
    # continuous BFS model
    for game in evaluation_games:
        if not os.path.exists(f"results/{game}/models/"):
            os.mkdir(f"results/{game}/models/")

        if os.path.exists(f"results/{game}/ob_continuous_results_BFS.txt"):
            with open(f"results/{game}/ob_continuous_results_BFS.txt", "rb") as f:
                results = pickle.load(f)

                training_results = dict()
                training_results["scores"] = results["scores"]
                training_results["ticks"] = results["ticks"]
                training_results["game_won"] = results["game_won"]
                if not os.path.exists(f"results/{game}/training_results/"):
                    os.mkdir(f"results/{game}/training_results/")
                with open(f"results/{game}/training_results/continuous_ob_training_results_BFS.txt", "wb") as file:
                    pickle.dump(training_results, file)

                if results["ticks"][-1, -1] != 0:
                    if not os.path.exists(f"results/{game}/ob_continuous_results_lock_BFS.txt"):
                        print(game, "is not done with training, but no lock exists")
                    continue
                else:
                    print(game, "extract continuous learning object based forward model")

                fm = results["forward_model"]
                fm.training_data = None
                fm.score_training_data = None

                with open(f"results/{game}/models/ob_forward_model_BFS.txt", "wb") as fmf:
                    pickle.dump(fm, fmf)

        else:
            print(game, "bfs ob forward model has not been trained yet")
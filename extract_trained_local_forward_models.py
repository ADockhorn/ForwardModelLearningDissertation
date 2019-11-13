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

        # extract existing continuous results of previous files
        if os.path.exists(f"results/{game}/continuous_results.txt"):
            with open(f"results/{game}/continuous_results.txt", "rb") as f:
                results = pickle.load(f)

                if results["ticks"][-1][-1] != 0:
                    fm = results["forward_model"]
                    fm._data_set = None
                    with open(f"results/{game}/old_local_forward_model.txt", "wb") as fmf:
                        pickle.dump(fm, fmf)

                    sm = results["score_model"]
                    sm._data_set = None
                    with open(f"results/{game}/old_local_score_model.txt", "wb") as smf:
                        pickle.dump(sm, smf)

    print("extract local forward models learned by a random agent")
    for game in evaluation_games:
        # extract results from training a local forward model using a random agent
        if os.path.exists(f"results/{game}/continuous_results_RANDOM.txt"):
            with open(f"results/{game}/continuous_results_RANDOM.txt", "rb") as f:
                results = pickle.load(f)

                training_results = dict()
                training_results["scores"] = results["scores"]
                training_results["ticks"] = results["ticks"]
                training_results["game_won"] = results["game_won"]
                if not os.path.exists(f"results/{game}/training_results/"):
                    os.mkdir(f"results/{game}/training_results/")
                with open(f"results/{game}/training_results/results_RANDOM.txt", "wb") as file:
                    pickle.dump(training_results, file)

                if results["ticks"][-1, -1] != 0:
                    print(game, "is not done with playing every level")
                    continue

    print("extract local forward models learned by a BFS agent")
    for game in evaluation_games:
        # extract results from training a local forward model using a random agent
        if os.path.exists(f"results/{game}/continuous_results_BFS.txt"):
            with open(f"results/{game}/continuous_results_BFS.txt", "rb") as f:
                results = pickle.load(f)

                training_results = dict()
                training_results["scores"] = results["scores"]
                training_results["ticks"] = results["ticks"]
                training_results["game_won"] = results["game_won"]
                if not os.path.exists(f"results/{game}/training_results/"):
                    os.mkdir(f"results/{game}/training_results/")
                with open(f"results/{game}/training_results/continuous_lfm_training_results_BFS.txt", "wb") as file:
                    pickle.dump(training_results, file)

                if results["ticks"][-1, -1] != 0:
                    if not os.path.exists(f"results/{game}/continuous_results_lock_BFS.txt"):
                        print(game, "is not done with training, but no lock exists")
                    continue
                else:
                    print(game, "extract continuous learning local forward model")

                fm = results["forward_model"]
                fm._data_set = None
                with open(f"results/{game}/models/local_forward_model_BFS.txt", "wb") as fmf:
                    pickle.dump(fm, fmf)

                sm = results["score_model"]
                sm._data_set = None
                with open(f"results/{game}/models/local_score_model_BFS.txt", "wb") as fmf:
                    pickle.dump(sm, fmf)


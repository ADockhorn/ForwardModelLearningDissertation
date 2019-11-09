import numpy as np
import pickle
import os
from games.GVGAIConstants import get_object_dict, get_images
from gym import envs
import gym
import gym_gvgai


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

for game in evaluation_games:
    print(r"""\begin{subfigure}[c]{1.0\textwidth}
    \includegraphics[width=1.0\textwidth]{graphics/pdf/forward-model-learning/algorithm-and-dataset-performance-""" + game + r""".pdf}
    \subcaption{GVGAI game ``""" + game + r"""''}
\end{subfigure}""")
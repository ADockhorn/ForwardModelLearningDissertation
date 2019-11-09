from gym import envs
import gym_gvgai
from games.gvgai_environment import GVGAIEnvironment
import random


if __name__ == "__main__":

    import matplotlib.pyplot as plt

    grid_based_games = []
    with open("data/GVGAI/grid-based-games.txt", "r") as file:  # Use file to refer to the file object
        for line in file.readlines():
            if line:
                grid_based_games.append(line[:-1])

    level = 0
    version = 0
    for game in grid_based_games:
        env = GVGAIEnvironment(game, level, version)
        _, _, _, sso = env.step(random.choice(env.get_actions()))
        plt.imshow(sso.image)
        plt.axis("off")
        # plt.title(f"{game}-{level}-{version}")
        plt.tight_layout()
        plt.savefig(f"figures/GVGAI/{game}-{level}-{version}.png")
        plt.savefig(f"figures/GVGAI/{game}-{level}-{version}.pdf")
        plt.show()

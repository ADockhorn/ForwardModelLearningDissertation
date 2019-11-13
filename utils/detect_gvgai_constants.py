from games.gvgai_environment import GVGAIEnvironment
import random
import os
import numpy
import string
from gym import envs
import gym_gvgai


if __name__ == "__main__":

    all_envs = envs.registry.all()

    grid_based_games = []
    with open("data/GVGAI/grid-based-games.txt", "r") as file:  # Use file to refer to the file object
        for s in file.readlines():
            if len(s) > 1:
                grid_based_games.append(s[:-1])

    f_trans_dict = open("trans_dict.txt", "w")
    f_images = open("images.txt", "w")

    for game in grid_based_games:
        if game != "painter":
            continue

        sprite_set = dict()
        with open(f"data/GVGAI/games/{game}.txt") as file:
            while "SpriteSet" not in file.readline():
                continue
            while True:
                line = file.readline()
                if "InteractionSet" in line:
                    break
                if "img" not in line:
                    continue
                strings = line.lstrip().rstrip().split(" ")
                for s in strings:
                    if s.startswith("img"):
                        if "autotiling" in line:
                            if s.split("=")[1].split("/")[1] == "dirtwall":
                                sprite_set[strings[0]] = "sprites/" + "oryx/dirtWall" + "_15.png"
                            else:
                                sprite_set[strings[0]] = "sprites/" + s.split("=")[1] + "_15.png"
                        else:
                            if os.path.isfile("sprites/" + s.split("=")[1] + ".png"):
                                sprite_set[strings[0]] = "sprites/" + s.split("=")[1] + ".png"
                            else:
                                sprite_set[strings[0]] = "sprites/" + s.split("=")[1] + "_0.png"

        cells = set()
        for level, name in enumerate([env_spec.id for env_spec in all_envs if env_spec.id.startswith(f"gvgai-{game}-")]):

            env = GVGAIEnvironment(game, level, 0)

            for i in range(5):
                sso = None
                for j in range(200):
                    _, _, is_done, sso = env.step(random.choice(env.get_actions()))
                    a = {obj for s in sso.observationString.split("\n") for obj in s.split(",")}
                    cells = cells.union(a)

                    if is_done:
                        break

        trans_dict = {x: i for i, x in zip(cells, string.ascii_lowercase)}
        reverse_trans_dict = {x: i for i, x in trans_dict.items()}

        images = {key: [sprite_set.get("ground", sprite_set.get("floor"))] + sorted([sprite_set[y] for y in obj_string.split(" ") if y in sprite_set], reverse=True)
                  for key, obj_string in trans_dict.items()}

        f_images.write(f"if game == '{game}': \n\treturn ")
        f_images.write(str(images))
        f_images.write("\n")
        f_images.write("\n")

        f_trans_dict.write(f"if game == '{game}': \n\treturn ")
        f_trans_dict.write(str(reverse_trans_dict))
        f_trans_dict.write("\n")
        f_trans_dict.write("\n")

    f_trans_dict.close()
    f_images.close()

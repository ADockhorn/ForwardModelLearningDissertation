from games.gvgai_environment import GVGAIEnvironment
import random
import matplotlib.pyplot as plt
import numpy as np
import os


def find_all_strings(game_name, version):
    all_objects = set()
    for level in range(5):
        game = GVGAIEnvironment(game_name, level, version)

        for i in range(1000):
            game.reset()
            for j in range(10):
                _, _, is_over, info = game.step(random.choice(game.get_actions()))
                objects = {obj for s in info.observationString.split("\n") for obj in s.split(",")}
                all_objects = all_objects.union(objects)
                if is_over:
                    break
        game.close()

    return all_objects


if __name__ == "__main__":
    grid_based_games = []
    with open("data/GVGAI/grid-based-games.txt", "r") as file:  # Use file to refer to the file object
        for s in file.readlines():
            if len(s) > 1:
                grid_based_games.append(s[:-1])

    for game in grid_based_games:

        level = 0
        version = 0

        #strings = find_all_strings(game, version)

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
                for string in strings:
                    if string.startswith("img"):
                        if "autotiling" in line:
                            if string.split("=")[1].split("/")[1] == "dirtwall":
                                sprite_set[strings[0]] = "sprites/" + "oryx/dirtWall" + "_15.png"
                            else:
                                sprite_set[strings[0]] = "sprites/" + string.split("=")[1] + "_15.png"
                        else:
                            if os.path.isfile("sprites/" + string.split("=")[1] + ".png"):
                                sprite_set[strings[0]] = "sprites/" + string.split("=")[1] + ".png"
                            else:
                                sprite_set[strings[0]] = "sprites/" + string.split("=")[1] + "_0.png"

        from games.TileMapVisualizer import TileMapVisualizer
        tsv = TileMapVisualizer(None, 24)

        #fig, ax = plt.subplots(5, 2)
        fig = plt.figure()
        import matplotlib.gridspec as gridspec
        gs1 = gridspec.GridSpec(5, 2)
        gs1.update(wspace=0.025, hspace=0.05)

        env = GVGAIEnvironment(game, level, version)
        for i in range(5):
            sso = None
            for j in range(10):
                _, _, _, sso = env.step(random.choice(env.get_actions()))

            a = np.array([[obj for obj in s.split(",")]
                          for s in sso.observationString.split("\n")]).transpose()

            trans_dict = {x: i for i, x in enumerate(set(a.flatten()))}
            reverse_trans_dict = {x: i for i, x in trans_dict.items()}

            b = np.zeros(a.shape)
            for x in range(b.shape[0]):
                for y in range(b.shape[1]):
                    b[x, y] = trans_dict[a[x, y]]

            images = {x: [sprite_set["floor"]] + [sprite_set[y] for y in reverse_trans_dict[x].split(" ") if y in sprite_set] for x in
                      set(b.flatten())}

            ax1 = plt.subplot(gs1[int(i*2)])
            ax2 = plt.subplot(gs1[int(i*2+1)])

            ax1.imshow(sso.image)
            ax1.set_axis_off()
            tsv.visualize_observation_grid(b, b.shape[0], b.shape[1], axis=ax2, tile_dict=images)
            ax2.set_axis_off()
        fig.set_figheight(a.shape[1]/10*5*4)
        fig.set_figwidth(a.shape[0]/10*2*4)
        plt.savefig(f"figures/GVGAI/games/plot_{game}.png")
        plt.savefig(f"figures/GVGAI/games/plot_{game}.pdf")
        env.close()
        plt.show()

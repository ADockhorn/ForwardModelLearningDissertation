import pygame
from games.Sokoban import Sokoban, SokobanConstants
import numpy as np
import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import ExtraTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from games.TileMapVisualizer import TileMapVisualizer
import matplotlib.pyplot as plt
from abstractclasses.AbstractNeighborhoodPattern import CrossNeighborhoodPattern
from models.localforwardmodel import LocalForwardModel
from models.modelcontainer import ModelContainer


import os
os.chdir("C:/Users/dockhorn/PycharmProjects/ForwardModelLearning")


class SokobanSprite(pygame.sprite.Sprite):
    images = {".": 'sprites/chamber_wall.png',
              "*": 'sprites/block2.png',
              "o": 'sprites/circleEffect1.png',
              "A": 'sprites/dwarf1.png',
              "u": 'sprites/circleEffect1.png',
              "w": 'sprites/wall3.png',
              "+": 'sprites/block1.png'
              }

    TILE_SIZE = 24

    def __init__(self, tile, x, y):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([SokobanSprite.TILE_SIZE, SokobanSprite.TILE_SIZE])
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))

        # Instead we could load a proper picture of a car...
        self.image = pygame.image.load(SokobanSprite.images[tile]).convert_alpha()

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.x = x * SokobanSprite.TILE_SIZE
        self.rect.y = y * SokobanSprite.TILE_SIZE


if __name__ == "__main__":
    game = Sokoban()
    w, h = game.get_width(), game.get_height()
    previous_state = game.deep_copy()

    tick = 0

    models = {"DT": DecisionTreeClassifier(), "ET": ExtraTreeClassifier(), "SVC": SVC(gamma="auto"),
              "kNN": KNeighborsClassifier()}

    fm = ModelContainer([models[x] for x in models], CrossNeighborhoodPattern(2),
                        game.observablePatterns)

    predictions = None
    errors_per_tick = np.zeros((101, len(fm.get_models())))

    fig, axes = plt.subplots(1, len(fm.get_models())+1)
    tsv = TileMapVisualizer(SokobanConstants.images, 24)

    while tick < 100:
        tick += 1

        # choose a random action
        action = random.choice([1, 2, 3, 4])

        if action is not None:

            if fm.is_trained():
                predictions = fm.predict(game, action)

            game.next(action)

            if predictions is not None:


                for model_idx, prediction in enumerate(predictions):
                    if tick % 10 == 0:
                        tsv.visualize_observation_grid(prediction.reshape(w, h), w, h, axes[model_idx+1])

                    #print(f"correctly predicted tiles: {sum(prediction == game.level.get_observation().flatten())}")

                    errors_per_tick[tick, model_idx] =\
                        (errors_per_tick[tick-1, model_idx] + 56 - sum(prediction == game._tile_map.get_observation().flatten()))

                if tick % 10 == 0:
                    tsv.visualize_game_state(game, axes[0])
                    plt.draw()
                    fig.canvas.flush_events()
                    fig.show()

            fm.add_transition(previous_state, action, game)
            fm.fit()

            previous_state = game.deep_copy()

        print(tick)


    import matplotlib.pyplot as plt

    plt.plot(range(len(errors_per_tick)), errors_per_tick)
    plt.plot(range(len(errors_per_tick)), [x*2 for x in range(len(errors_per_tick))])
    plt.legend(list(models.keys()) + ["baseline"])
    plt.show()

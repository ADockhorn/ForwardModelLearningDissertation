import pygame
from games.Sokoban import Sokoban, SokobanConstants
import numpy as np
from models.forwardmodel import ForwardModel
import random
from sklearn.tree import DecisionTreeClassifier
from games.TileMapVisualizer import TileMapVisualizer
import matplotlib.pyplot as plt
from abstractclasses.AbstractNeighborhoodPattern import CrossNeighborhoodPattern
from models.localforwardmodel import LocalForwardModel


class SokobanSprite(pygame.sprite.Sprite):
    images = {".": '../sprites/chamber_wall.png',
              "*": '../sprites/block2.png',
              "o": '../sprites/circleEffect1.png',
              "A": '../sprites/dwarf1.png',
              "u": '../sprites/circleEffect1.png',
              "w": '../sprites/wall3.png',
              "+": '../sprites/block1.png'
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

        # Instead we could load a proper pciture of a car...
        self.image = pygame.image.load(SokobanSprite.images[tile]).convert_alpha()

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        self.rect.x = x * SokobanSprite.TILE_SIZE
        self.rect.y = y * SokobanSprite.TILE_SIZE


if __name__ == "__main__":
    game = Sokoban()
    previous_state = game.deep_copy()

    # initialize pygame
    #import os
    #os.environ["SDL_VIDEODRIVER"] = "dummy"

    pygame.init()
    pygame.display.init()

    display = pygame.display.set_mode((1, 1), pygame.NOFRAME)
    surf = pygame.Surface((game.get_width() * SokobanSprite.TILE_SIZE,
                                       game.get_height() * SokobanSprite.TILE_SIZE)).convert()

    #pygame.display.set_caption("Sokoban")
    clock = pygame.time.Clock()
    print(game)


    carryOn = True
    human_control = True
    visualize_result = True
    use_unique_values = True
    moved = True


    tick = 0


    fm = LocalForwardModel(DecisionTreeClassifier(), CrossNeighborhoodPattern(2),
                           np.array(['x', '.', '*', 'o', 'A', 'u', 'w', '+', '1', '2', '3', '4']))
    # fm = ForwardModel(AdaBoostClassifier(
    #     DecisionTreeClassifier(),
    #     n_estimators=5,
    #     learning_rate=1))

    prediction = None
    errors_per_tick = [0]


    fig, ax1 = plt.subplots(1, 1)
    plt.show(block=False)
    tsv = TileMapVisualizer(SokobanConstants.images, 24)


    while carryOn:
        action = SokobanConstants.LEFT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carryOn = False
                break
            elif human_control and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:  # Pressing the x Key will quit the game
                    carryOn = False
                    break
                elif event.key == pygame.K_LEFT and action is None:
                    action = SokobanConstants.LEFT
                elif event.key == pygame.K_UP and action is None:
                    action = SokobanConstants.UP
                elif event.key == pygame.K_DOWN and action is None:
                    action = SokobanConstants.DOWN
                elif event.key == pygame.K_RIGHT and action is None:
                    action = SokobanConstants.RIGHT

        if action is None and human_control is False:
            action = random.choice([1, 2, 3, 4])

        if action is not None:

            if fm.is_trained():
                prediction = fm.predict(game, action)

            tick += 1
            game.next(action)

            if prediction is not None:
                #tsv.visualize_game_state(game, ax1)
                #tsv.visualize_observation_grid(prediction.reshape(8, 7), 8, 7, ax2)
                #plt.draw()
                #fig.canvas.flush_events()

                #print(f"correctly predicted tiles: {sum(prediction == game.level.get_observation().flatten())}")
                errors_per_tick.append(errors_per_tick[-1] + 56 - sum(prediction == game._tile_map.get_observation().flatten()))

            """
            if previous_state.level.playerX != game._tile_map.playerX or \
                    previous_state.level.playerY != game._tile_map.playerY:
                pass
                #print(f"player moved from ({previous_state.level.playerX},{previous_state.level.playerY}) to "
                #      f"({game.level.playerX},{game.level.playerY})")
            for x in range(game.get_width()):
                for y in range(game.get_height()):
                    if previous_state.level.get_cell(x, y) != game._tile_map.get_cell(x, y):
                        #print(f"({x},{y}) changed")
                        pass
            """

            fm.add_transition(previous_state, action, game)
            fm.fit()

            previous_state = game.deep_copy()

        if visualize_result:
            #tsv.visualize_game_state(game, ax1)
            #plt.draw()
            #fig.canvas.flush_events()

            all_sprites_list = pygame.sprite.Group()
            tilemap = game.get_tile_map()
            character = pygame.sprite.Group()
            for x in range(game.get_width()):
                for y in range(game.get_height()):
                    if tilemap[x, y] == "o" or tilemap[x, y] == "u" or tilemap[x, y] == "A":
                        all_sprites_list.add(SokobanSprite(".", x, y))
                    if tilemap[x, y] == "u":
                        all_sprites_list.add(SokobanSprite(tilemap[x, y], x, y))
                        character.add(SokobanSprite("A", x, y))
                    elif tilemap[x, y] == "A":
                        character.add(SokobanSprite("A", x, y))
                    else:
                        all_sprites_list.add(SokobanSprite(tilemap[x, y], x, y))

            all_sprites_list.draw(surf)
            character.draw(surf)
            pygame.display.update()
            obs = np.transpose(pygame.surfarray.array3d(surf).astype(np.uint8), (1, 0, 2))
            ax1.imshow(obs)
            plt.draw()
            fig.canvas.flush_events()
            clock.tick(60)

        if tick == 1000:
            carryOn = False
        else:
            print(tick)


    pygame.quit()

    import matplotlib.pyplot as plt

    plt.plot(range(len(errors_per_tick)), errors_per_tick)
    plt.show()

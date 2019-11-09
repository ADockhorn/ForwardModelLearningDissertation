from abstractclasses.AbstractVisualizer import AbstractGameStateVisualizer
from abstractclasses.AbstractGameState import GridGameState
from abstractclasses.AbstractNeighborhoodPattern import AbstractNeighborhoodPattern
import matplotlib.pyplot as plt
import matplotlib.image as mp_img
import numpy as np


class TileMapVisualizer(AbstractGameStateVisualizer):

    def __init__(self, tile_dict=None, tile_size=None):
        super().__init__()
        if tile_dict is not None:
            self.set_tile_dict(tile_dict)
        else:
            self.tile_dict = None

        if tile_size is None:
            self.tile_width = self.tile_dict[1].shape[0]
            self.tile_height = self.tile_dict[1].shape[1]
        else:
            self.tile_width = tile_size
            self.tile_height = tile_size

    def set_tile_dict(self, tile_dict):
        self.tile_dict = {tile_key: [TileMapVisualizer.read_tile(image_path) for image_path in image_paths]
                          for (tile_key, image_paths) in tile_dict.items()}

    @staticmethod
    def read_tile(path):
        tile = mp_img.imread(path)
        if len(tile.shape) == 2:
            tile = np.stack([tile, tile, tile, np.ones(tile.shape)], axis=2)
        return tile

    def visualize_game_state(self, game_state: GridGameState, axis=None):
        tile_map = game_state.get_tile_map()
        map_w = game_state.get_width()
        map_h = game_state.get_height()

        self.visualize_observation_grid(tile_map, map_w, map_h, axis)

    def visualize_observation_grid(self, observation, map_w, map_h, axis=None, tile_dict=None):
        if tile_dict is not None:
            self.set_tile_dict(tile_dict)

        if axis is None:
            _, axis = plt.subplots(1, 1)
        axis.cla()
        axis.axis('off')

        for x in range(map_w):
            for y in range(map_h):
                for img in self.tile_dict.get(observation[x, y], []):
                    axis.imshow(img, extent=(x*self.tile_height + -0.5, (x+1)*self.tile_height - 0.5,
                                             (map_h*self.tile_height)-((y+1)*self.tile_height + -0.5),
                                             (map_h*self.tile_height)-(y*self.tile_height - 0.5)))
        axis.set_xlim(-0.5, map_w*self.tile_width-0.5)
        axis.set_ylim(0.5, map_h*self.tile_height+0.5)
        return axis

    def visualize_patterns_of_position_list(self, game_state: GridGameState,
                                            pattern_extractor: AbstractNeighborhoodPattern,
                                            position_list):
        raise NotImplementedError

    def visualize_all_pattern(self, game_state: GridGameState,
                              pattern_extractor: AbstractNeighborhoodPattern):

        fig, ax = plt.subplots(game_state.get_height(), game_state.get_width())

        plot_positions = [(x, y) for x in range(game_state.get_width()) for y in range(game_state.get_height())]
        results = pattern_extractor.get_patterns_for_position_list(game_state.get_tile_map(), plot_positions)
        for i, (x, y) in enumerate(plot_positions):
            pattern_to_plot = np.array([' ' for _ in range(pattern_extractor.get_width() *
                                                           pattern_extractor.get_height())],
                                       dtype=results.dtype).reshape(pattern_extractor.get_width(),
                                                                    pattern_extractor.get_height())
            pattern_to_plot[pattern_extractor.get_mask()] = results[i, :]
            self.visualize_observation_grid(pattern_to_plot,
                                            pattern_extractor.get_width(),
                                            pattern_extractor.get_height(),
                                            ax[y, x])
        return fig, ax


if __name__ == "__main__":
    from games.Sokoban import Sokoban, SokobanConstants

    tsv = TileMapVisualizer(SokobanConstants.images, 24)
    game = Sokoban()

    _, [ax1, ax2, ax3, ax4, ax5, ax6] = plt.subplots(1, 6)
    tsv.visualize_game_state(game, ax1)

    game.next(SokobanConstants.UP)
    tsv.visualize_game_state(game, ax2)

    game.next(SokobanConstants.UP)
    tsv.visualize_game_state(game, ax3)

    game.next(SokobanConstants.DOWN)
    tsv.visualize_game_state(game, ax4)

    game.next(SokobanConstants.RIGHT)
    tsv.visualize_game_state(game, ax5)

    game.next(SokobanConstants.RIGHT)
    tsv.visualize_game_state(game, ax6)

    plt.show()


    tsv = TileMapVisualizer(SokobanConstants.images, 24)
    game = Sokoban()

    _, [ax1, ax2] = plt.subplots(1, 2)

    game.next(SokobanConstants.UP)
    tsv.visualize_game_state(game, ax1)

    game.next(SokobanConstants.UP)
    tsv.visualize_game_state(game, ax2)

    plt.show()


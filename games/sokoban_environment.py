from games.Sokoban import Sokoban, SokobanConstants
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from games.TileMapVisualizer import TileMapVisualizer
import matplotlib.pyplot as plt
from abstractclasses.AbstractNeighborhoodPattern import CrossNeighborhoodPattern, SquareNeighborhoodPattern
from models.localforwardmodel import LocalForwardModel
from models.modelcontainer import ModelContainer
import random
from typing import Tuple
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC


class SokobanEnvironment:

    def __init__(self, level=-1):
        self.game = Sokoban(level)
        #self.fig, self.ax = plt.subplots(1, 1)
        self.tsv = TileMapVisualizer(SokobanConstants.images, 24)

    def step(self, action) -> Tuple[np.ndarray, int, bool, None]:
        self.game.next(action)
        return self.game.get_tile_map(), self.game.get_score(), self.game.is_terminal(), None

    def reset(self, level=-1):
        self.game = Sokoban(level)
        return

    def render(self):
        #self.tsv.visualize_game_state(self.game, self.ax)
        #plt.draw()
        #self.fig.canvas.flush_events()
        pass

    def close(self):
        #plt.close(self.fig)
        pass

    def get_actions(self):
        return self.game.get_actions()


def update_prediction_plot(states, predicted_states, actions, ax):
    for idx, state in enumerate(states):
        tsv.visualize_observation_grid(state, state.shape[0], state.shape[1], ax[0, idx])
        if idx == 0:
            ax[0, idx].set_title("current_state")
        else:
            ax[0, idx].set_title(f"{SokobanConstants.ACTION_DESCRIPTION[actions[idx-1]]}")

    tsv.visualize_observation_grid(states[0], states[0].shape[0], states[0].shape[1], ax[1, 0])

    for idx, predicted in enumerate(predicted_states):
        tsv.visualize_observation_grid(predicted, predicted.shape[0], predicted.shape[1], ax[1, idx])
    ax[1, 0].set_ylabel("predicted_states")

    plt.draw()
    fig.canvas.flush_events()
    pass


if __name__ == "__main__":
    env = SokobanEnvironment()

    previous_observation = None
    prediction = None
    prediction_stats = [0]
    accumulated_error = [0]

    classifier_list = list()
    classifier_list.append(DecisionTreeClassifier())
    classifier_list.append(AdaBoostClassifier(
         DecisionTreeClassifier(),
         n_estimators=5,
         learning_rate=1))
    classifier_list.append(SVC())

    pattern_extractor_list = list()
    pattern_extractor_list.append(CrossNeighborhoodPattern(2))
    pattern_extractor_list.append(SquareNeighborhoodPattern(2))

    possible_inputs = np.array(['x', '.', '*', 'o', 'A', 'u', 'w', '+', '0', '1', '2', '3', '4'])
    # forward_model = ModelContainer(classifier_list, pattern_extractor_list, possible_inputs)
    forward_model = LocalForwardModel(classifier_list[0], pattern_extractor_list[0], possible_inputs)

    action_list = np.random.choice(np.array(env.get_actions()), 1000)
    predict_future_steps = 3
    fig, ax = plt.subplots(2, predict_future_steps+1)
    plt.draw()
    plt.show(block=False)
    tsv = TileMapVisualizer(SokobanConstants.images, 24)

    observation = env.game.get_tile_map()
    states = []
    state_predictions = [None]

    for i, current_action in enumerate(action_list):
        states.append(observation)
        update_prediction_plot(states[max(i-predict_future_steps, 0):(i+1)], [],
                               action_list[max(i-predict_future_steps,0):(i+1)], ax)

        if forward_model.is_trained() and previous_observation is not None:
            #predictions = forward_model.predict_n_steps(previous_observation, action_list[i:i+predict_future_steps])
            #for plot_idx, prediction in enumerate(predictions):
            #    tsv.visualize_observation_grid(prediction, previous_observation.shape[0], previous_observation.shape[1], ax[1, 1+plot_idx])
            #    ax[1, 1+plot_idx].set_title(f"{SokobanConstants.ACTION_DESCRIPTION[action_list[i+plot_idx]]}")
            pass
        else:
            state_predictions.append(None)

        observation, reward, done, info = env.step(current_action)
        #env.render()

        if previous_observation is None:
            print(f"tick {i}")
        else:
            #if prediction is not None:
            #    prediction_stats.append(np.sum(observation.flatten() == prediction))
            #    accumulated_error.append(accumulated_error[-1] + len(prediction) - prediction_stats[-1])
            #    print(f"tick {i}, predicted_correctly: {prediction_stats[-1]}")

            forward_model.add_transition(previous_observation, current_action, observation)
            forward_model.fit()

        previous_observation = observation
        input('wait for key...')

    #fig, [ax1, ax2] = plt.subplots(1, 2)
    #ax1.plot(prediction_stats)
    #ax2.plot(accumulated_error)
    #plt.show()




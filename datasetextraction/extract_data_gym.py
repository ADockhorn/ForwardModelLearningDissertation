import gym
import numpy as np
import os
from PIL import Image


DIR_NAME = 'record'
MAX_FRAMES = 2000  # max length of Mario
MAX_TRIALS = 100


def _process_frame(frame):
    obs = np.array(Image.fromarray(frame).resize((64, 64)))
    return obs


def record_game(game_name, output):

    if not os.path.exists(DIR_NAME):
        os.makedirs(DIR_NAME)
    if not os.path.exists(DIR_NAME + f"/{game_name}"):
        os.makedirs(DIR_NAME + f"/{game_name}")

    record_files = [int(name.split("_")[3].split(".")[0]) for name in os.listdir(f'./record/{game_name}')
                    if os.path.isfile(f"./record/{game_name}/{name}") and name.startswith(f"record_{game_name}_{output}")]
    file_id = 0 if len(record_files) == 0 else max(record_files)+1

    for trial in range(MAX_TRIALS):
        previousObservation = None

        env = gym.make(f'{game_name}-{output}')
        env.reset()
        X_down_sampled = []
        X_original = []
        actions = []
        rewards = []

        for frame in range(MAX_FRAMES):
            action = env.action_space.sample()
            obs, reward, done, _ = env.step(action)

            if previousObservation is not None:
                X_down_sampled.append(_process_frame(previousObservation))
                X_original.append(previousObservation)
                if len(actions) == 0:
                    actions.append(np.array([0]))
                    rewards.append(np.array([0]))
                else:
                    actions.append(action)
                    rewards.append(reward)

            #if previousObservation is not None:
            #    fm.add_transition(previousObservation, action, None)
            previousObservation = obs

            env.render()

            if done:
                break

        print(f"finished {trial+1}/{MAX_TRIALS} trials")
        X_down_sampled = np.array(X_down_sampled)
        X_original = np.array(X_original)
        actions = np.array(actions)
        env.close()

        np.savez_compressed(f"./{DIR_NAME}/{game_name}/record_{game_name}_{output}_{file_id}.npz",
                            obs_downsampled=X_down_sampled, actions=actions, obs_original=X_original, rewards=rewards)
        file_id += 1
        print(f"store file for X={X_down_sampled.shape}; X={X_original.shape}; y={actions.shape}")


if __name__ == "__main__":
    game_names = ["Pong", "Qbert", "MontezumaRevenge", "MsPacman", "Phoenix", "SpaceInvaders", "Assault", "Boxing", "Breakout", "Freeway"]
    outputs = ["v0", "v0", "v0", "v0", "v0", "v0", "v0", "v0", "v0", "v0"]
    for game_name, output in zip(game_names, outputs):
        record_game(game_name, output)

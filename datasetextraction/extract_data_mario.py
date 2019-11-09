from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT, RIGHT_ONLY
import numpy as np
from abstractclasses.AbstractNeighborhoodPattern import CrossNeighborhoodPattern
from models.localforwardmodel import LocalForwardModel
import os
from PIL import Image
import matplotlib.pyplot as plt


def _process_frame(frame):
    obs = np.array(Image.fromarray(frame).resize((64, 64)))
    return obs


MAX_FRAMES = 2000  # max length of Mario
MAX_TRIALS = 3

render_mode = False  # for debugging.

DIR_NAME = 'record'
output = "v2"
if not os.path.exists(DIR_NAME):
    os.makedirs(DIR_NAME)

if not os.path.exists(DIR_NAME+"/Mario"):
    os.makedirs(DIR_NAME+"/Mario")

record_files = [int(name.split("_")[2].split(".")[0]) for name in os.listdir('./record/Mario')
                if os.path.isfile("./record/Mario/"+name) and name.startswith("record_mario_")]
file_id = 0 if len(record_files) == 0 else max(record_files)+1


worlds = [1, 2, 3, 4, 5, 6, 7, 8]
levels = [1, 2, 3, 4]
combinations = [(world, level) for world in worlds for level in levels]

for levelind, (world, level) in enumerate(combinations):
    for trial in range(MAX_TRIALS):
        actions = []
        previousObservation = None

        env = gym_super_mario_bros.make(f'SuperMarioBros-{world}-{level}-{output}')
        env = JoypadSpace(env, RIGHT_ONLY)
        env.reset()
        X_downsampled = []
        X_original = []
        y = []
        rewards = []

        for frame in range(MAX_FRAMES):
            action = env.action_space.sample()
            #action = actions[frame%len(actions)]#
            obs, reward, done, _ = env.step(action)

            if previousObservation is not None:
                X_downsampled.append(_process_frame(previousObservation))
                X_original.append(previousObservation)
                if len(y) == 0:
                    y.append(0)
                    rewards.append(0)
                else:
                    y.append(action)
                    rewards.append(reward)


            #if previousObservation is not None:
            #    fm.add_transition(previousObservation, action, None)
            previousObservation = obs
            if render_mode:
                env.render()

            if done:
                break

        print(f"finished {trial+1}/{MAX_TRIALS} trials")
        X_downsampled = np.array(X_downsampled)
        X_original = np.array(X_original)
        y = np.array(y)
        rewards = np.array(rewards)
        env.close()

        np.savez_compressed(f"./{DIR_NAME}/Mario/record_mario_{world}_{level}_{output}_{trial}.npz",
                            obs_downsampled=X_downsampled, actions=y, obs_original=X_original, rewards=rewards)
        print(f"store file for X={X_downsampled.shape}; X={X_original.shape}; "
              f"y={y.shape}, rewards={rewards.shape}")
    print(f"finished {levelind + 1}/{len(combinations)} levels")

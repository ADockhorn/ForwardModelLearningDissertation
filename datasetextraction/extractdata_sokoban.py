import numpy as np
import random
import os
from abstractclasses.AbstractNeighborhoodPattern import CrossNeighborhoodPattern
from models.localforwardmodel import LocalForwardModel

MAX_FRAMES = 100  # max length of carracing
MAX_TRIALS = 100

render_mode = False # for debugging.

DIR_NAME = 'record'
if not os.path.exists(DIR_NAME):
    os.makedirs(DIR_NAME)

record_files = [int(name.split("_")[2].split(".")[0]) for name in os.listdir('./record') if os.path.isfile("./record/"+name)  and name.startswith("record_sokoban_")]
file_id = 0 if len(record_files) == 0 else max(record_files)+1

from games.sokoban_environment import SokobanEnvironment

fm = LocalForwardModel(None, CrossNeighborhoodPattern(3), np.array(['x', '.', '*', 'o', 'A', 'u', 'w', '+',
                                                                    '0', '1', '2', '3', '4']))

for trial in range(MAX_TRIALS):
    env = SokobanEnvironment(random.randint(1, 20))
    actions = []
    previousObservation = None

    for frame in range(MAX_FRAMES):
        action = random.choice(env.get_actions())
        obs, _, done, _ = env.step(action)
        if previousObservation is not None:
            fm.add_transition(obs, action, previousObservation)
        previousObservation = obs

        if done:
            break
    env.close()
    print(f"finished {trial}/{MAX_TRIALS} trials")


    np.savez_compressed(DIR_NAME+"/record_sokoban_"+str(file_id)+".npz", obs=fm.get_data_set()[:, :-2],
                        action=fm.get_data_set()[:, -2], result=fm.get_data_set()[:, -1])
    print(f"store file for obs={fm.get_data_set()[:, :-2].shape}; "
          f"action={fm.get_data_set()[:, -2].shape};"
          f"result={fm.get_data_set()[:, -1].shape}")
    file_id += 1



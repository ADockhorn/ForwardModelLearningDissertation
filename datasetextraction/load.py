import numpy as np
import os


record_files = [int(name.split("_")[1].split(".")[0]) for name in os.listdir('./record') if os.path.isfile("./record/"+name) and name.startswith("record_")]

if len(record_files) != 0:
    loaded = np.load(f'./record/record_{max(record_files)}.npz')
    print(loaded['obs'].shape)
    print(loaded['action'].shape)
    print(loaded['result'].shape)


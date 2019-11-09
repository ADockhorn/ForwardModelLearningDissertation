import time
from gym.envs.box2d.car_racing import *
from pyglet.window import key
import matplotlib.pyplot as plt
from scipy.misc import imresize as resize
import os




def _process_frame(frame):
  obs = frame[0:84, :, :].astype(np.float)/255.0
  obs = resize(obs, (64, 64))
  obs = ((1.0 - obs) * 255).round().astype(np.uint8)
  return obs


def start_playing(n_episodes, max_ticks, start_ticks=30):
    DIR_NAME = 'record'
    if not os.path.exists(DIR_NAME):
        os.makedirs(DIR_NAME)

    record_files = [int(name.split("_")[2].split(".")[0]) for name in os.listdir('./record') if
                    os.path.isfile("./record/" + name) and name.startswith("record_carracing_")]
    file_id = 0 if len(record_files) == 0 else max(record_files) + 1

    a = np.array([0.0, 0.0, 0.0])

    def key_press(k, mod):
        global restart
        if k == 0xff0d: restart = True
        if k == key.LEFT:  a[0] = -1.0
        if k == key.RIGHT: a[0] = +1.0
        if k == key.UP:    a[1] = +1.0
        if k == key.DOWN:  a[2] = +0.8

    def key_release(k, mod):
        if k == key.LEFT and a[0] == -1.0: a[0] = 0
        if k == key.RIGHT and a[0] == +1.0: a[0] = 0
        if k == key.UP:    a[1] = 0
        if k == key.DOWN:  a[2] = 0

    env = CarRacing()
    env.render()
    env.viewer.window.on_key_press = key_press
    env.viewer.window.on_key_release = key_release

    for episode in range(n_episodes):
        prev_observation = env.reset()
        X = None
        y = None

        ticks = 0
        while ticks < max_ticks+start_ticks:
            action = a
            observation, reward, done, info = env.step(action)
            if ticks > start_ticks:
                if X is None:
                    X = _process_frame(prev_observation)
                    y = np.array([0., 0., 0.])
                else:
                    X = np.vstack((X, _process_frame(prev_observation)))
                    y = np.vstack((y, action))

            env.render()

            prev_observation = observation

            if done:
                break
            ticks += 1
        time.sleep(2)

        np.savez_compressed(DIR_NAME + "/record_carracing_" + str(file_id) + ".npz", obs=X, action=y)
        print(f"store file for obs={X.shape}; "
              f"action={y.shape}")
        file_id += 1


if __name__ == "__main__":
    start_playing(2, 100)

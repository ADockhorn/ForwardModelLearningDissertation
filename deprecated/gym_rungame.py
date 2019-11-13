import gym
import matplotlib.pyplot as plt
from models.forwardmodel import ForwardModel
import numpy as np

plt.ion()


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])


def run_game(game, forwardmodel=None):
    env = gym.make(game)
    observation = env.reset()

    observations = []

    if forwardmodel is not None:
        f, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(10,5))
        #plt.axis([-50, 50, 0, 10000])
        plt.ion()
        ax1.axis('off'), ax1.set_title("observation")
        ax2.axis('off'), ax2.set_title("grayscale observation")
        ax3.axis('off'), ax3.set_title("predicted observation")
        plt.show()

        im_color = ax1.imshow(observation)
        im_gray = ax2.imshow(rgb2gray(observation), cmap=plt.get_cmap("gray"))
        im_pred = ax3.imshow(rgb2gray(observation)*0, cmap=plt.get_cmap("gray"))
        plt.draw()

    for _ in range(1000):

        action = env.action_space.sample()
        if forwardmodel is not None and len(observations) > 0:
            #forwardmodel.fit(np.array(observations))
            #predicted_observation = forwardmodel.predict(observation)
            pass

        observation, reward, done, info = env.step(action)
        extended_observation = np.append(observation.flatten(), action)
        observations.append(extended_observation)

        if forwardmodel is not None:
            im_color.set_data(observation)
            im_gray.set_data(rgb2gray(observation))
            plt.draw()
            plt.pause(0.001)

        else:
            env.render('human')

    plt.show()
    env.close()


if __name__ == "__main__":
    from sklearn.neighbors import NearestNeighbors
    fm = ForwardModel(NearestNeighbors(n_neighbors=2, algorithm='ball_tree'))

    run_game("Pong-v0", 1)
    # run_game("Pong-v0", fm)

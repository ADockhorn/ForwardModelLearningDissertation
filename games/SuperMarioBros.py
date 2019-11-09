from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT


if __name__ == "__main__":
    #env = gym_super_mario_bros.make('SuperMarioBros-v0')  #whole game
    env = gym_super_mario_bros.make('SuperMarioBros-1-1-v3')  #SuperMarioBros-<world>-<stage>-v<version>  single stage

    env = JoypadSpace(env, SIMPLE_MOVEMENT)

    done = True
    for step in range(5000):
        if done:
            state = env.reset()
        state, reward, done, info = env.step(env.action_space.sample())
        env.render()

    env.close()
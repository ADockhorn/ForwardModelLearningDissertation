import gym
import gym_gvgai
import matplotlib.pyplot as plt
import numpy as np
from abstractclasses.AbstractGrid import AbstractGrid
from typing import Dict, Tuple, List
import logging
import copy
import logging
from sklearn.tree import DecisionTreeClassifier
from abstractclasses.AbstractNeighborhoodPattern import CrossNeighborhoodPattern, SquareNeighborhoodPattern
from models.localforwardmodel import LocalForwardModel
import random
import time
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC
from games.TileMapVisualizer import TileMapVisualizer
from games.GVGAIConstants import GVGAIConstants
from games.gvgai_environment import GVGAIEnvironment


if __name__ == "__main__":
    game = "painter"
    level = 0
    version = 0

    env = GVGAIEnvironment(game, level, version)
    done = False
    while done:


import time
import math
import random
from abstractclasses.AbstractForwardModelAgent import AbstractForwardModelAgent
from models.objectgamestate import ObjectGameState
from copy import deepcopy


class TreeNode:

    def __init__(self, state, parent):
        self.state = state
        self.parent = parent
        self.numVisits = 0
        self.totalReward = 0
        self.reward = 0
        self.isTerminal = False
        self.isFullyExpanded = self.isTerminal
        self.children = {}


class MCTSObjectAgent(AbstractForwardModelAgent):

    def __init__(self,
                 forward_model=None, score_model=None,
                 iterationLimit=50,
                 explorationConstant=1, #1 / math.sqrt(2),
                 rollout_depth=10,
                 discount=0.95):
        super().__init__(forward_model, score_model)
        self.searchLimit = iterationLimit
        self.explorationConstant = explorationConstant
        self.rollout_depth = rollout_depth
        self.actions = None
        self.discount = discount

    def get_agent_name(self) -> str:
        return "LFM-MCTS"

    def re_initialize(self):
        return

    def get_next_action(self, state, actions):
        #print(state)

        self.actions = actions
        state = ObjectGameState(state.origObservationGrid, state.observationGrid.shape[2],
                                state.observationGrid.shape[1])

        self.root = TreeNode(state, None)

        for i in range(self.searchLimit):
            self.executeRound()

        #print()
        #for child in self.root.children.values():
        #    print(child.totalReward, child.numVisits, self.root.numVisits, child.numVisits,
        #          child.totalReward / child.numVisits)

        bestChild = self.get_best_child(self.root, 0)
        #print(self.get_action(self.root, bestChild))
        return self.get_action(self.root, bestChild)

    def executeRound(self):
        node = self.selectNode(self.root)
        reward = self.randomPolicy(deepcopy(node.state), self.rollout_depth)
        self.backpropogate(node, reward)

    def selectNode(self, node):
        while not node.isTerminal:
            if node.isFullyExpanded:
                node = self.get_best_child(node, self.explorationConstant)
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        actions = self.actions
        for action in actions:
            if action not in node.children.keys():
                new_state, discounted_return = self._forward_model.predict(node.state, action)

                newNode = TreeNode(new_state, node)
                newNode.reward = discounted_return
                node.children[action] = newNode
                if len(actions) == len(node.children):
                    node.isFullyExpanded = True
                return newNode

    def backpropogate(self, node, reward):
        while node is not None:
            node.numVisits += 1
            reward += node.reward
            node.totalReward += reward
            node = node.parent

    def get_best_child(self, node, explorationValue):
        bestValue = float("-inf")
        bestNodes = []
        for child in node.children.values():
            nodeValue = child.totalReward / child.numVisits + explorationValue * math.sqrt(
                2 * math.log(node.numVisits) / child.numVisits)
            #print(nodeValue, child.totalReward / child.numVisits, explorationValue * math.sqrt(
            #    2 * math.log(node.numVisits) / child.numVisits))
            if nodeValue > bestValue:
                bestValue = nodeValue
                bestNodes = [child]
            elif nodeValue == bestValue:
                bestNodes.append(child)
        return random.choice(bestNodes)

    def get_action(self, root, bestChild):
        for action, node in root.children.items():
            if node is bestChild:
                return action

    def randomPolicy(self, state, remaining_depth):
        action = random.choice(self.actions)
        state, discounted_return = self._forward_model.predict(state, action)
        if remaining_depth == 0:
            return discounted_return
        else:
            return discounted_return + self.randomPolicy(state, remaining_depth - 1) * self.discount

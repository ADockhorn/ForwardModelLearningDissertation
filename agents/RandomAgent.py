import random
from abstractclasses.AbstractForwardModelAgent import AbstractForwardModelAgent


class RandomAgent(AbstractForwardModelAgent):

    def __init__(self, forward_model=None, score_model=None):
        super().__init__(forward_model, score_model)

    def get_next_action(self, state, actions):
        return random.choice(actions)

    def get_agent_name(self) -> str:
        return "Random Agent"

    def re_initialize(self):
        return None


if __name__ == "__main__":

    agent = RandomAgent()
    action = agent.get_next_action(None, [1, 2, 3, 4])

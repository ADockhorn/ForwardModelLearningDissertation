import numpy as np
import logging
import math
import random

from abstractclasses.AbstractForwardModelAgent import AbstractForwardModelAgent
from models.objectgamestate import ObjectGameState
from copy import deepcopy


class BFSObjectAgent(AbstractForwardModelAgent):

    def __init__(self, expansions, discount_factor=1.0, forward_model=None, score_model=None):
        super().__init__(forward_model, score_model)

        self._expansions = expansions
        self._discount_factor = discount_factor
        self.visited_states = dict()
        self._exploration_penalty = 0.1

    def re_initialize(self):
        self.visited_states = dict()

    def get_next_action(self, state, actions):
        """
        candidates = []
        to_expand = [[[], 0, ObjectGameState(state.origObservationGrid, state.observationGrid.shape[2], state.observationGrid.shape[1])]]
        for i in range(self._expansions):
            if len(to_expand) == 0:
                break
            new_candidates = self.expand(to_expand.pop(0), actions)
            for new_candidate in new_candidates:
                to_expand.append(new_candidate)
                candidates.append(new_candidate)
        """
        """
        state = ObjectGameState(state.origObservationGrid, state.observationGrid.shape[2], state.observationGrid.shape[1])
        state_id = state.string
        if state_id in self.visited_states:
            self.visited_states[state_id] += 1
        else:
            self.visited_states[state_id] = 1
        """

        unique_candidates = []
        to_expand = [[[], 0, state]]
        for i in range(self._expansions):
            if len(to_expand) == 0:
                break

            new_candidates = self.expand(to_expand.pop(0), actions)
            for new_candidate in new_candidates:
                for candidate in unique_candidates:
                    # if score and state is the same, don't add this to the search
                    if new_candidate[1] == candidate[1] and new_candidate[2].string == candidate[2].string:
                        break
                else:
                    unique_candidates.append(new_candidate)
                    to_expand.append(new_candidate)

        best_score = max(unique_candidates, key=lambda x: x[1])
        best_candidates = [x for x in unique_candidates if x[1] == best_score[1]]
        logging.info('Best score in evaluations: %.2f' % best_score[1])

        # The next best action is the first action from the solution space
        return random.choice(best_candidates)[0][0]

    def expand(self, expandable, actions):

        action_seq, score, state = expandable
        discount = math.pow(self._discount_factor, len(action_seq))

        expanded = []
        random.shuffle(actions)
        for action in actions:
            new_state = deepcopy(state)
            new_state, pred_score = self._forward_model.predict(new_state, action)
            discounted_return = score + pred_score[0] * discount
            #discounted_return -= self.visited_states.get(new_state.string, 0) * self._exploration_penalty * discount
            expanded.append([action_seq + [action], round(discounted_return, 2), new_state])

        return expanded

    def get_agent_name(self) -> str:
        return "BFS Agent"

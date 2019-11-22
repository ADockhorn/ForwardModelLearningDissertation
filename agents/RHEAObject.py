import numpy as np
import logging
import math
import random
from copy import deepcopy

from abstractclasses.AbstractForwardModelAgent import AbstractForwardModelAgent
from models.objectgamestate import ObjectGameState


class RHEAObjectAgent(AbstractForwardModelAgent):

    def __init__(self, rollout_actions_length, mutation_probability, num_evaluations,
                 flip_at_least_one=True, discount_factor=1.0, ignore_frames=0, forward_model=None, score_model=None):
        super().__init__(forward_model, score_model)

        self._rollout_actions_length = rollout_actions_length
        self._flip_at_least_one = flip_at_least_one
        self._mutation_probability = mutation_probability
        self._num_evaluations = num_evaluations
        self._ignore_frames = ignore_frames
        self._solution = None

        self._discount_factors = []
        for i in range(self._rollout_actions_length):
            self._discount_factors.append(math.pow(discount_factor, i))

    def re_initialize(self):
        pass

    def get_next_action(self, sso, actions):
        """
        Get the next best action by evaluating a bunch of mutated solutions
        """
        solution = self._random_solution(actions)

        candidate_solutions = self._mutate(solution, actions, self._mutation_probability)

        mutated_scores = self.evaluate_rollouts(sso, candidate_solutions)
        best_idx = int(np.argmax(mutated_scores, axis=0))

        best_score_in_evaluations = mutated_scores[best_idx]

        self._solution = candidate_solutions[best_idx]

        logging.info('Best score in evaluations: %.2f' % best_score_in_evaluations)

        # The next best action is the first action from the solution space
        return self._solution[0]

    def get_agent_name(self) -> str:
        return "RHEA Agent"

    def _random_solution(self, actions):
        """
        Create a random set fo actions
        """
        return np.array([random.choice(actions) for _ in range(self._rollout_actions_length)])

    def _mutate(self, solution, actions, mutation_probability):
        """
        Mutate the solution
        """

        candidate_solutions = []
        # Solution here is 2D of rollout_actions x batch_size
        for b in range(self._num_evaluations):
            # Create a set of indexes in the solution that we are going to mutate
            mutation_indexes = set()
            solution_length = len(solution)
            if self._flip_at_least_one:
                mutation_indexes.add(np.random.randint(solution_length))

            mutation_indexes = mutation_indexes.union(
                set(np.where(np.random.random([solution_length]) < mutation_probability)[0]))

            # Create the number of mutations that is the same as the number of mutation indexes
            num_mutations = len(mutation_indexes)
            mutations = [random.choice(actions) for _ in range(num_mutations)]

            # Replace values in the solutions with mutated values
            new_solution = np.copy(solution)
            new_solution[list(mutation_indexes)] = mutations
            candidate_solutions.append(new_solution)

        return np.stack(candidate_solutions)

    def evaluate_rollouts(self, state, candidate_solutions):
        scores = []
        state = ObjectGameState(state.origObservationGrid, state.observationGrid.shape[2], state.observationGrid.shape[1])

        for solution in candidate_solutions:
            scores.append(self.evaluate_rollout(deepcopy(state), solution))

        return scores

    def evaluate_rollout(self, state, action_sequence):
        discounted_return = 0
        new_state = state
        for idx, action in enumerate(action_sequence):
            new_state, pred_score = self._forward_model.predict(new_state, action)
            discounted_return += pred_score * self._discount_factors[idx]

        return discounted_return

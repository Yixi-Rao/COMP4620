import unittest

from vi import ValueIteration
from student_example1 import hard_instance

class Test(unittest.TestCase):

    def test(self):
        domain = hard_instance()
        eps = 0.5

        # verify the parameters of the state machine
        self.assertEqual(len(domain.get_observation_space().get_elements()), 6, msg="Needs 6 states")
        for state in domain.get_observation_space().get_elements(): 
            for action in domain.get_applicable_actions(state).get_elements(): 
                cost = domain.get_transition_value(state, action).cost
                self.assertGreaterEqual(cost, 0, "Cost needs to be between 0 and 1")
                self.assertGreaterEqual(1, cost, "Cost needs to be between 0 and 1")

        for state in domain.get_observation_space().get_elements(): 
            for action in domain.get_applicable_actions(state).get_elements(): 
                for _, prob in domain.get_next_state_distribution(state, action).get_values():
                    self.assertGreaterEqual(prob, 0.1, "Probability of a transition should be at least 0.1")

        # verify the number of iterations
        vi = ValueIteration(domain, gamma=1, initial_value=0)
        vi.backup(epsilon=eps, max_iteration=10000) # Notice that the value of 0.5 is very large!
        self.assertGreater(vi.nb_iterations(), 1000, msg="Number of iterations too small")
        


def main():
    unittest.main()

if __name__ == "__main__":
    main()

import unittest

from domain import RLEnvironment
from cricket import cricket_team_3, CricketAction
from qlearning import QLearning
from q import LastValueQ

class Test(unittest.TestCase):

    def test(self):
        domain: RLEnvironment = cricket_team_3()
        gamma = .9
        q = LastValueQ(default=0)
        qlearning: QLearning = QLearning(domain=domain, epsilon=.1, gamma=gamma, q=q)

        # There is only one state after the first action.  We will revolve around this state.
        domain.reset()
        initial_state = domain.current_state()
        domain.execute(domain.applicable_actions()[0])
        state_of_interest = domain.current_state()

        q.learn(state_of_interest, CricketAction.STOP, 1)
        q.learn(state_of_interest, CricketAction.RUN, 1)
        q.learn(state_of_interest, CricketAction.BACKOFF, 1)

        qlearning.reset()
        qlearning.execute_one_action()
        self.assertEqual(domain.current_state(), state_of_interest)

        # Remark: this test only verifies the long term reward.  Should also verify the reward of the current action.
        for i in range(1000):
            q.learn(state_of_interest, CricketAction.BACKOFF, i+2)
            qlearning.reset()
            qlearning.execute_one_action()
            self.assertEqual(q.value(initial_state, CricketAction.STOP), gamma * q.value(state_of_interest, CricketAction.BACKOFF))

def main():
    unittest.main()

if __name__ == "__main__":
    main()

# eof
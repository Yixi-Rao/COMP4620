import unittest

from domain import RLEnvironment
from cricket import cricket_team_3, CricketAction
from sarsa import Sarsa
from q import LastValueQ

class Test(unittest.TestCase):

    def test(self):
        domain: RLEnvironment = cricket_team_3()
        gamma = .9
        q = LastValueQ(default=0)
        epsilon = .1
        sarsa = Sarsa(domain=domain, epsilon=epsilon, gamma=gamma, q=q)

        # There is only one state after the first action.  We will revolve around this state.
        domain.reset()
        initial_state = domain.current_state()
        domain.execute(domain.applicable_actions()[0])
        state_of_interest = domain.current_state()

        q.learn(state_of_interest, CricketAction.STOP, 1)
        q.learn(state_of_interest, CricketAction.RUN, 2)
        q.learn(state_of_interest, CricketAction.BACKOFF, 3)

        sarsa.reset()
        sarsa.execute_one_action()
        self.assertEqual(domain.current_state(), state_of_interest)

        # Remark: this test only verifies the long term reward.  Should also verify the reward of the current action.
        nb_stop = 0
        nb_run = 0
        nb_backoff = 0
        NB_RUNS = 1000
        for i in range(NB_RUNS):
            q.learn(state_of_interest, CricketAction.BACKOFF, i+20)
            sarsa.reset()
            sarsa.execute_one_action()
            if q.value(initial_state, CricketAction.STOP) == gamma * q.value(state_of_interest, CricketAction.STOP):
                nb_stop += 1
            if q.value(initial_state, CricketAction.STOP) == gamma * q.value(state_of_interest, CricketAction.RUN):
                nb_run += 1
            if q.value(initial_state, CricketAction.STOP) == gamma * q.value(state_of_interest, CricketAction.BACKOFF):
                nb_backoff += 1
            
        message: str = 'Suspicious number of actions.  This could be a random outcome.  Try again, and if this test often fails, your implementation is probably incorrect.'
        self.assertLess(nb_stop, NB_RUNS * epsilon * 2, msg=message)
        self.assertLess(nb_run, NB_RUNS * epsilon * 2, msg=message)
        self.assertLess(nb_backoff, NB_RUNS * (1-(epsilon/2)), msg=message)

def main():
    unittest.main()

if __name__ == "__main__":
    main()

# eof
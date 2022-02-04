import unittest

from domain import RLEnvironment

from cricket import cricket_team_2, CricketAction
from q import LastValueQ, epsilon_greedy_action

class Test(unittest.TestCase):

    def test(self):
        domain: RLEnvironment = cricket_team_2()

        lv: LastValueQ = LastValueQ(default=0)

        domain.reset()
        domain.execute(domain.applicable_actions()[0])
        state = domain.current_state()

        # state = CricketState(nb_runs_=0, ball_distance_=2, batter1_adv_=1, batter2_adv_=5)
        run = CricketAction.RUN
        stop = CricketAction.STOP
        backoff = CricketAction.BACKOFF

        lv.learn(state=state, action=run, reward=1)
        lv.learn(state=state, action=stop, reward=2)
        lv.learn(state=state, action=backoff, reward=3) # backoff is optimal

        epsilon = .1
        # using epsilon = .1 and 1000 tests.
        # on average, the optimal decision should be taken 1000 * ((1-eps) + eps / NB_ACTIONS)
        # that's about 933, and 33 times for each other action
        counting = { run:0 , stop:0 , backoff:0 }
        for _i in range(1000): 
            action = epsilon_greedy_action(q=lv, env=domain, epsilon=epsilon)
            counting[action] += 1

        message: str = 'Suspicious number of actions.  This could be a random outcome.  Try again, and if this test often fails, your implementation is probably incorrect.'

        self.assertLess(counting[run], 60, msg=message)
        self.assertLess(15, counting[run], msg=message)

        self.assertLess(counting[stop], 60, msg=message)
        self.assertLess(15, counting[stop], msg=message)

        self.assertLess(counting[backoff], 960, msg=message)
        self.assertLess(915, counting[backoff], msg=message)

def main():
    unittest.main()

if __name__ == "__main__":
    main()

# eof
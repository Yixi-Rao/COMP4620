import unittest

from domain import RLEnvironment

from cricket import cricket_team_2, CricketAction
from q import LastValueQ, greedy_action

class Test(unittest.TestCase):

    def test(self):
        domain: RLEnvironment = cricket_team_2()

        lv: LastValueQ = LastValueQ(default=0)

        domain.reset()

        # state = CricketState(nb_runs_=0, ball_distance_=2, batter1_adv_=1, batter2_adv_=5)
        run = CricketAction.RUN
        stop = CricketAction.STOP
        backoff = CricketAction.BACKOFF

        lv = LastValueQ(default=0)

        # create 3 tests where run, stop, and backoff are the optimal action
        while len(domain.applicable_actions()) == 1: # we want the three actions to be applicable
            action = domain.applicable_actions()[0]
            domain.execute(action)

        lv.learn(state=domain.current_state(), action=run, reward=10)
        lv.learn(state=domain.current_state(), action=stop, reward=0)
        lv.learn(state=domain.current_state(), action=backoff, reward=0)
        self.assertEqual(greedy_action(q=lv, env=domain), run)

        lv.learn(state=domain.current_state(), action=run, reward=0)
        lv.learn(state=domain.current_state(), action=stop, reward=10)
        lv.learn(state=domain.current_state(), action=backoff, reward=0)
        self.assertEqual(greedy_action(q=lv, env=domain), stop)

        lv.learn(state=domain.current_state(), action=run, reward=0)
        lv.learn(state=domain.current_state(), action=stop, reward=0)
        lv.learn(state=domain.current_state(), action=backoff, reward=10)
        self.assertEqual(greedy_action(q=lv, env=domain), backoff)

def main():
    unittest.main()

if __name__ == "__main__":
    main()

# eof
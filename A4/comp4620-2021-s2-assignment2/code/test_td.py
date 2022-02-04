import unittest

from domain import RLEnvironment
from cricket import cricket_team_2, CricketState, CricketAction
from q import TemporalDifference

class Test(unittest.TestCase):

    def test(self):

        domain: RLEnvironment = cricket_team_2()
        gamma: float = 0.99
        # The next states are not actually possible.  Ideally, this test should be improved.
        state1 = CricketState(nb_runs_=0, ball_distance_=2, batter1_adv_=1, batter2_adv_=5)
        action1 = CricketAction.RUN
        state2 = CricketState(nb_runs_=0, ball_distance_=2, batter1_adv_=2, batter2_adv_=5)
        action2 = CricketAction.STOP

        ave = TemporalDifference(alpha=.1,default=10)

        self.assertAlmostEqual(ave.value(state1, action1), 10)

        ave.learn(state=state1, action=action1, reward=1)
        self.assertAlmostEqual(ave.value(state1, action1), 9.1)
        self.assertAlmostEqual(ave.value(state2, action2), 10)

        ave.learn(state=state1, action=action1, reward=7)
        self.assertAlmostEqual(ave.value(state1, action1), 8.89)
        self.assertAlmostEqual(ave.value(state2, action2), 10)

        ave.learn(state=state1, action=action2, reward=0)
        self.assertAlmostEqual(ave.value(state1, action1), 8.89)
        self.assertAlmostEqual(ave.value(state2, action2), 10)
        self.assertAlmostEqual(ave.value(state1, action2), 9)

def main():
    unittest.main()

if __name__ == "__main__":
    main()

# eof
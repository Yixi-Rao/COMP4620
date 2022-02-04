import unittest

class Test(unittest.TestCase):

    def test(self):
        import example1
        mdp = example1.example_1()

        state0 = mdp.get_state('0')
        state1 = mdp.get_state('1')
        state2 = mdp.get_state('2')
        state3 = mdp.get_state('3')
        action0 = mdp.get_action('hunt')
        action1 = mdp.get_action('nohunt')

        import MDP

        pol = MDP.ExplicitPolicy(mdp)

        pol.set_action(state0, action0)
        pol.set_action(state1, action1)
        pol.set_action(state2, action0)
        pol.set_action(state3, action1)

        import algos

        v = algos.compute_v_of_policy(mdp, pol, gamma=.9, stopping_threshold=.001)

        self.assertAlmostEqual(v.value(state0), 64.8, msg='Bounds may be imprecise', delta=.1)
        self.assertAlmostEqual(v.value(state1), 70.3, msg='Bounds may be imprecise', delta=.1)
        self.assertAlmostEqual(v.value(state2), 93.4, msg='Bounds may be imprecise', delta=.1)
        self.assertAlmostEqual(v.value(state3), 94, msg='Bounds may be imprecise', delta=.1)
   

def main():
    unittest.main()

if __name__ == "__main__":
    main()

# eof
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

        import algos

        q = algos.ExplicitActionValueFunction()

        q.set_value(state0, action0, 1)
        q.set_value(state0, action1, 10)
        q.set_value(state1, action0, 8)
        q.set_value(state1, action1, 6)
        q.set_value(state2, action0, 7)
        q.set_value(state2, action1, 7)
        q.set_value(state3, action0, 4)
        q.set_value(state3, action1, 0)

        import MDP

        pol = MDP.ExplicitPolicy(mdp)
        pol.set_action(state0, action0)
        pol.set_action(state1, action0)
        pol.set_action(state2, action1)
        pol.set_action(state3, action1)

        v = algos.compute_v_from_q_and_policy(mdp, pol, q)
        
        self.assertEqual(v.value(state0), 1)
        self.assertEqual(v.value(state1), 8)
        self.assertEqual(v.value(state2), 7)
        self.assertEqual(v.value(state3), 0)
   

def main():
    unittest.main()

if __name__ == "__main__":
    main()

# eof
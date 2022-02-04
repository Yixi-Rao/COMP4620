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
        q.set_value(state0, action0, 5)
        q.set_value(state0, action1, 9)
        q.set_value(state1, action0, 8)
        q.set_value(state1, action1, 6)
        q.set_value(state2, action0, 9)
        q.set_value(state2, action1, 7)
        q.set_value(state3, action0, 8)
        q.set_value(state3, action1, 8)

        # a,v = algos.greedy_action(mdp, q, state0)
        pol, v = algos.greedy_policy(mdp, q)
        self.assertEqual(pol.action(state0), action1)
        self.assertEqual(pol.action(state1), action0)
        self.assertEqual(pol.action(state2), action0)
        self.assertEqual(v.value(state3), 8)
   

def main():
    unittest.main()

if __name__ == "__main__":
    main()

# eof
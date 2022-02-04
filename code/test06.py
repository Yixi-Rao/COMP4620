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

        v = algos.ExplicitStateValueFunction()
        v.set_value(state0, 2)
        v.set_value(state1, 4)
        v.set_value(state2, 6)
        v.set_value(state3, 8)
        q = algos.compute_q_from_v(mdp, v, .9)

        self.assertAlmostEqual(q.value(state0, action0), 6.06)
        self.assertAlmostEqual(q.value(state0, action1), 4.8)
        self.assertAlmostEqual(q.value(state1, action0), 16.68)
        self.assertAlmostEqual(q.value(state1, action1), 13.8)
        self.assertAlmostEqual(q.value(state2, action0), 17.48)
        self.assertAlmostEqual(q.value(state2, action1), 14.6)
        self.assertAlmostEqual(q.value(state3, action0), 17.02)
        self.assertAlmostEqual(q.value(state3, action1), 15.4)
   

def main():
    unittest.main()

if __name__ == "__main__":
    main()

# eof
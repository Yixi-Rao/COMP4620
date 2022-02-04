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
        v.set_value(state1, 6)
        v.set_value(state2, 22)
        v.set_value(state3, 20)

        pol, vprime = algos.bellman_backup(mdp, v, .9)

        self.assertEqual(pol.action(state0), action0)
        self.assertEqual(pol.action(state1), action0)
        self.assertEqual(pol.action(state2), action0)
        self.assertEqual(pol.action(state3), action1)
        
        self.assertAlmostEqual(vprime.value(state0), 7.32)
        self.assertAlmostEqual(vprime.value(state1), 27.12)
        self.assertAlmostEqual(vprime.value(state2), 28.1)
        self.assertAlmostEqual(vprime.value(state3), 29.8)
   

def main():
    unittest.main()

if __name__ == "__main__":
    main()

# eof
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
        
        pol, v = algos.value_iteration(mdp, gamma=.9, epsilon=.01)
        
        self.assertAlmostEqual(v.value(state0),99.0,delta=0.1)
        self.assertAlmostEqual(v.value(state1),110,delta=0.1)
        self.assertAlmostEqual(v.value(state2),110,delta=0.1)
        self.assertAlmostEqual(v.value(state3),109,delta=0.1)

        self.assertEqual(pol.action(state0),action0)
        self.assertEqual(pol.action(state1),action0)
        self.assertEqual(pol.action(state2),action1)
        self.assertEqual(pol.action(state3),action1)
   

def main():
    unittest.main()

if __name__ == "__main__":
    main()

# eof
import unittest

class Test(unittest.TestCase):

    def test(self):
        import example1
        mdp = example1.example_1()

        state0 = mdp.get_state('0')
        state1 = mdp.get_state('1')
        state2 = mdp.get_state('2')
        state3 = mdp.get_state('3')
        action = mdp.get_action('hunt')

        count = {state0: 0, state1: 0, state2: 0, state3: 0}
        total_reward = 0

        import algos
        for i in range(1000):
            state, rew = algos.simulate_one_step(mdp, state1, action)
            count[state] = count[state] + 1
            total_reward += rew

        self.assertEqual(total_reward, 1000*12)
        self.assertLessEqual(count[state0], 50 + 1000*.1, msg='Probable error (rerun)')
        self.assertLessEqual(count[state1], 50 + 1000*.2, msg='Probable error (rerun)')
        self.assertLessEqual(count[state2], 50 + 1000*.7, msg='Probable error (rerun)')
        self.assertLessEqual(count[state3], 0)
    

def main():
    unittest.main()

if __name__ == "__main__":
    main()
  

# eof
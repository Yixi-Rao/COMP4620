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
        pol.set_action(state0,action0)
        pol.set_action(state1,action0)
        pol.set_action(state2,action0)
        pol.set_action(state3,action1)

        
        
        import algos
        hist = algos.simulate(mdp, pol, 100000)

        cum_reward = 0
        count = {state0: 0, state1: 0, state2: 0, state3: 0}
        for i in range(hist.length()):
            count[hist.state(i)] += 1
            cum_reward += hist.reward(i)

        # At this stage, we have a Markov process, which can be solved analytical.  
        # The values below are generally satisfied, but unlikely runs can happen that will return different values.
        self.assertLessEqual(cum_reward, 1070000, msg='Probable error (rerun)')
        self.assertGreaterEqual(cum_reward, 1060000, msg='Probable error (rerun)')
        self.assertGreaterEqual(count[state0], 1000, msg='Probable error (rerun)')
        self.assertLessEqual(count[state3], 38000, msg='Probable error (rerun)')
        print(count)
        

def main():
    unittest.main()

if __name__ == "__main__":
    main()

# eof
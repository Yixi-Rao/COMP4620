'''
  An example of an MDP modelled implicitly.
  Compared to the state machine of example1.py, 
  the successor states are not computed when the MDP is constructed 
  but when the method next_states() is called.
'''

from typing import List, Tuple

from MDP import Action, State, MDP

class Example2(MDP):
    hunt_ = 'hunt'
    nohunt_ = 'nohunt'

    def states(self) -> List[State]:
        return [0,1,2,3]

    def actions(self) -> List[Action]:
        return [self.hunt_, self.nohunt_]

    def applicable_actions(self, s: State) -> List[Action]:
        return self.actions() # all actions are always applicable

    def next_states(self, s: State, a: Action) -> List[Tuple[State,float,float]]:
        reward = (3-s) + (10 if s>0 else 0) # the reward is always the same in this example
        
        if a == self.nohunt_:
            next_state = max(0,s-1) # consume one if possible
            proba = 1
            return [ (next_state,proba,reward) ] # only one successor

        # a == self.hunt_

        # 2 to 3 successors
        proba_successor = {} # using a map because there are several ways to reach the same state

        # first state: not gaining food (and consume 1)
        s1 = max(0,s-1)
        proba_successor[s1] = .1

        # second state: gain 2 food (and consume 1)
        s2 = min(3,s+1)
        proba_successor[s2] = .7

        # third state: gain 1 food (and consume 0)
        s3 = s
        if not s in proba_successor:
            proba_successor[s] = 0
        proba_successor[s] = proba_successor[s] + .2

        return [ (next,proba,reward) for (next,proba) in proba_successor.items() ]
        '''
          Returns the outcome of performing action a in state s.  
          Defined as a list of elements [s',prob,rew] 
          where s' is the next state, 
          prob is the probability of reaching this state, 
          and rew is the reward.
        '''
        pass
    
    def initial_state(self) -> State:
        return 1

def example_2() -> MDP:
    return Example2()

# eof
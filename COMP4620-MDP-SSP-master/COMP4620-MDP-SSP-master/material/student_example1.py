from vi import ValueIteration
from statemachine import StateMachine, SMTransition

def hard_instance() -> StateMachine: 
    '''
  Creates an MDP that is as hard as possible for VI to find a good approximation. 
  The MDP should be built on top of the StateMachine framework available in the file statemachine.py
  The restrictions are as follows: 
  1. The state machine contains six states, named s1 to s6.  
     The initial state is s1.  
     Only one action, a1, is available in s6; 
     this action costs 0 and loops on state s6.
  2. The cost of any action is always in the interval [0,1].
  3. The probability of a transition from one state to another 
     is either 0 or at least 0.1.
    '''
    # DONE
    transition_functions = [SMTransition("s6","a1",0,[("s6",1)]),
                            SMTransition("s1", "a2", 1, [("s2", 0.8),("s5",0.2)]),
                            SMTransition("s2", "a3", 1, [("s3", 1)]),
                            SMTransition("s3", "a4", 1, [("s4", 1)]),
                            SMTransition("s4", "a5", 1, [("s2", 1)]),
                            SMTransition("s5", "a6", 1, [("s6", 1)]),
                            # SMTransition("s2", "a2", 1, [("s2", 1)]),
                            # SMTransition("s3", "a3", 1, [("s3", 1)]),
                            # SMTransition("s4", "a4", 1, [("s4", 1)]),
                            # SMTransition("s5", "a5", 1, [("s5", 1)]),
                            # SMTransition("s1", "a6", 1, [("s2", 0.2),("s3",0.2),("s4",0.2),("s5",0.2),("s6",0.2)])
                            ]

    return StateMachine(
        transition_functions, "s1"
    )


if __name__ == '__main__':
    domain = hard_instance()
    vi = ValueIteration(domain, gamma=1)
    vi.backup(epsilon = 0.5) # Notice that the value of 0.5 is very large!
    print("Number of iterations: {}".format(vi.nb_iterations()))

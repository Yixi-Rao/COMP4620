from typing import Dict, Tuple, Optional

from MDP import Action, State, MDP, Policy
from algos import ExplicitStateValueFunction, StateValueFunction, value_iteration

class NDPolicy:
    def __init__(self, copy: Optional = None): 
        '''
          If copy is not empty, this policy is a copy of the specified policy
        '''
        if copy == None:
            self._actions = {}
        else:
            self._actions = {
                s:set(acts) for s,acts in copy._actions.items()
            }

    def add(self, s, a):
        if not s in self._actions:
            self._actions[s] = set()
        self._actions[s].add(a)

    def add_nondet_policy(self, ndpol):
        for s,acts in ndpol.items():
            if not s in self._actions:
                self._actions[s] = set()
            for a in acts:
                self._actions[s].add(a)
    
    def add_det_policy(self, mdp, pol: Policy):
        for s in mdp.states():
            self.add(s, pol.action(s))

    def actions(self, s):
        return self._actions[s]

def compute_policy_value(mdp: MDP, ndpol: NDPolicy, gamma: float, epsilon: float, max_iteration: int) -> StateValueFunction:
    current_svalue = ExplicitStateValueFunction()
    #! compute_v_of_policy
    while max_iteration > 0: 
        #! compute_q_from_v
        Q_s_a = {}
        for s in mdp.states():
            for a in mdp.applicable_actions(s):
                value = 0
                for next_s, prob, rew in mdp.next_states(s,a):
                    value += prob * (rew + (gamma * current_svalue.value(next_s)))
                Q_s_a[(s, a)] = value
        #! compute_v_from_q_and_policy
        new_svalue = ExplicitStateValueFunction()
        for s in mdp.states():
            Min_act = min([(Q_s_a[(s, a)], a) for a in ndpol.actions(s)])[1]
            new_svalue.set_value(s, Q_s_a[(s, Min_act)])
        #! state_value_difference
        diff = max([abs(current_svalue.value(s) - new_svalue.value(s)) for s in mdp.states()])
        if diff < epsilon:
            current_svalue = new_svalue
            break
        current_svalue = new_svalue
        max_iteration = max_iteration - 1
        
    return current_svalue    

def policy_size(pol:NDPolicy):
    return sum([len(a_set) for a_set in pol._actions.values()])
        
def getOptimal(mdp, VI_V, applicable_acts, Π, startindex, subopt_epsilon, epsilon, gamma, max_iteration):
    '''using the search algorithm from the paper:
        M. M. Fard and J. Pineau. MDPs with non-deterministic policies. In 21st Advances in Neural Information Processing Systems (NeurIPS-08), pages 1065–1072, 2008.
    '''
    Π0 = NDPolicy(Π)
    # We make use of the fact that if a policy is not -optimal, neither is any other policy that includes it, and thus we can cut the search tree at this point.
    for i in range(startindex, len(applicable_acts)):
        state, act = applicable_acts[i]
        if act not in Π.actions(state):
            Π_new = NDPolicy(Π)
            Π_new.add(state, act)
            ND_V = compute_policy_value(mdp, Π_new, epsilon=epsilon, gamma=gamma, max_iteration=max_iteration)
            if ND_V.value(state) >= (1 - subopt_epsilon) * VI_V.value(state):
                new_pol = getOptimal(mdp, VI_V, applicable_acts, Π_new, startindex + 1, subopt_epsilon, epsilon, gamma, max_iteration)
                if policy_size(new_pol) > policy_size(Π0):
                    Π0 = new_pol
    return Π0

def compute_non_augmentable_policy(mdp: MDP, gamma: float, epsilon: float, subopt_epsilon: float, max_iteration: int) -> NDPolicy:
    '''using the search algorithm from the paper:
        M. M. Fard and J. Pineau. MDPs with non-deterministic policies. In 21st Advances in Neural Information Processing Systems (NeurIPS-08), pages 1065–1072, 2008.
    '''
    # start by computing the conservative policy
    Optimalpol, VI_V = value_iteration(mdp=mdp, gamma=gamma, epsilon=epsilon)
    NDpol            = NDPolicy()
    NDpol.add_det_policy(mdp=mdp, pol=Optimalpol)
    
    applicable_acts = []
    for state in mdp.states():
        for act in mdp.applicable_actions(state):
            applicable_acts.append((state, act))
    # We then augment it until we arrive at a non-augmentable policy
    return getOptimal(mdp, VI_V, applicable_acts, NDpol, 0, subopt_epsilon, epsilon, gamma, max_iteration)
                

'''
  TODO: Explain here why the non-deterministic policy 
  represented on the figure is not conservative epsilon-optimal 
  according to the definition of Fard and Pineau 
  (between 200 and 500 characters):

  In order to be conservative epsilon-optimal, 
  the non-deterministic policy should be such that all policies 
  that can be derived from this policy have a value of 44.5 or more.  
  However, the policy that moves from 0 to 1 and from 1 to 0 
  has a negative value (it only includes costs).
'''

# eof
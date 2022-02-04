'''
  This file contains the algorithms that you need to implement.  

  In this file, the object used to represent the value of each state 
  is a dictionary State -> float.
  Similarly, the object used to represent the Q value (of each pair state/action)
  is a dictionary (State,Action) -> float.
  A (Markov, deterministic) policy is a dictionary State -> Action.
'''

from typing import Dict, Tuple, Optional

from random import random

from MDP import Action, MDP, State, Policy, ExplicitPolicy, History

class StateValueFunction:
    '''
        The interface for a (state) value function.
    '''
    def value(self, s: State) -> float:
        print(f'{type(self).__name__} value function not implemented')

class ExplicitStateValueFunction(StateValueFunction):
    '''
      A value function explicitly represented as a dictionary with default value of 0.
    '''
    def __init__(self):
        self._explicit_value = {}

    def set_value(self, s: State, v: float): 
        self._explicit_value[s] = v

    def value(self, s: State): 
        if not s in self._explicit_value:
            self.set_value(s,0)
        return self._explicit_value[s]

def state_value_difference(mdp: MDP, v1: StateValueFunction, v2: StateValueFunction) -> float:
    '''
      Returns the absolute max difference between the two specified state value function.  
      This methods is particularly useful in contexts 
      in which one computes the state value function until convergence: 
      at each iteration, we compute the difference between the current value function and the previous one, 
      and we stop when that difference is below a given threshold.  
      Notice however that this here method computes the value of the difference, 
      whilst we only care about whether this difference is above the threshold;
      in practice, we would probably send the threshold as a parameter and stop as soon as the threshold is reached.
    '''
    return max([ abs(v1.value(s) - v2.value(s)) for s in mdp.states() ])

class ActionValueFunction:
    '''
        The interface for an action (in a state) value function.
    '''
    def value(self, s: State, a: Action) -> float:
        print(f'{type(self).__name__} value function not implemented')

class ExplicitActionValueFunction(ActionValueFunction):
    '''
      An action value function explicitly represented as a dictionary with default value of 0.
    '''
    def __init__(self):
        self._explicit_value = {}

    def set_value(self, s: State, a: Action, v: float): 
        self._explicit_value[(s,a)] = v

    def value(self, s: State, a: Action): 
        if not (s,a) in self._explicit_value:
            self.set_value((s,a),0)
        return self._explicit_value[s,a]

def simulate_one_step(mdp: MDP, state: State, act: Action) -> Tuple[State,float]:
    '''
      TODO: IMPLEMENT
    '''
    pass

def simulate(mdp: MDP, pol: Policy, nbsteps: int) -> History:
    '''
      TODO: IMPLEMENT
    '''

def greedy_action(mdp: MDP, q: ActionValueFunction, s: State) -> Tuple[Action,float]:
    '''
      TODO: IMPLEMENT
    '''
    pass

def greedy_policy(mdp: MDP, q: ActionValueFunction) -> Tuple[Policy,StateValueFunction]:
    '''
      TODO: IMPLEMENT
    '''
    pass

def one_step_lookahead(mdp: MDP, v: StateValueFunction, gamma: float, s: State, a: Action
  ) -> float:
    '''
      TODO: IMPLEMENT
    '''
    pass

def compute_q_from_v(mdp: MDP, v: StateValueFunction, gamma: float) -> ActionValueFunction:
    '''
      TODO: IMPLEMENT
    '''
    pass

def compute_v_from_q_and_policy(mdp: MDP, pol: Policy, q: ActionValueFunction) -> StateValueFunction:
    '''
      TODO: IMPLEMENT
    '''
    pass

def bellman_backup(mdp: MDP, v: StateValueFunction, gamma: float) -> Tuple[Policy,StateValueFunction]:
    '''
      TODO: IMPLEMENT
    '''
    pass

def compute_v_of_policy(mdp: MDP, \
    pol: Policy, \
    gamma: float, \
    stopping_threshold: float, \
    starting_value: Optional[StateValueFunction] = None) -> StateValueFunction:
    '''
      TODO: IMPLEMENT
    '''
    pass

def is_policy_nearly_greedy(mdp: MDP, pol: Policy, epsilon: float, q: ActionValueFunction):
    '''
      TODO: IMPLEMENT
    '''
    pass

def policy_iteration(mdp: MDP, gamma: float, epsilon: float, stopping_threshold: float, starting_pi: Optional[Policy] = None) -> Policy:
    '''
      TODO: IMPLEMENT
    '''
    pass

def value_iteration(mdp: MDP, gamma: float, epsilon: float) -> Tuple[Policy, StateValueFunction]:
    '''
      TODO: IMPLEMENT
    '''
    pass

# eof
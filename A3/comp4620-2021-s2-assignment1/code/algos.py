'''
  This file contains the algorithms that you need to implement.  

  In this file, the object used to represent the value of each state 
  is a dictionary State -> float.
  Similarly, the object used to represent the Q value (of each pair state/action)
  is a dictionary (State,Action) -> float.
  A (Markov, deterministic) policy is a dictionary State -> Action.
'''

from typing import Dict, Tuple, Optional, Set, List, FrozenSet

from random import random

from MDP import Action, MDP, State, Policy, ExplicitPolicy, History

#NOTE State Value Function: 可空定义，有set_value(s, v) 和 value(s)函数
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
    def __init__(self, mdp: Optional[MDP] = None, value_function: Optional[StateValueFunction] = None):
        self._explicit_value = {}
        if (not mdp is None) and (not value_function is None):
            for state in mdp.states():
                self._explicit_value[state] = value_function.value(state)

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

#NOTE Action Value Function: 代表在s中执行a的value为多少。有set_value(s, a, v) 和 value(s, a)函数
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
            self.set_value((s,a), 0)
        return self._explicit_value[s,a]

#!------------------------------------------------------------------------------------------------------
#NOTE (s , a) -> (s,' r)...
def simulate_one_step(mdp: MDP, state: State, act: Action) -> Tuple[State,float]:
    r = random()
    for next_state, prob, reward in mdp.next_states(state, act):
        r -= prob
        if r <= 0:
            return next_state, reward
    print(f'Error with probability function {state} {act}')

#NOTE 从初始state开始，执行Policy上的指示，不停调用simulate_one_step来构建history
def simulate(mdp: MDP, pol: Policy, nbsteps: int) -> History:
    h = History(mdp)
    for _ in range(nbsteps):
        current_state = h.last_state()
        act = pol.action(current_state)
        next_state, rew = simulate_one_step(mdp, current_state, act)
        h.add(act, next_state, rew)
    return h

#NOTE 给Action Value Function，贪婪算法决定当前state的action。返回action与action value
def greedy_action(mdp: MDP, q: ActionValueFunction, s: State) -> Tuple[Action,float]:
    '''
      Computes the greedy action in the specified state given the specified action value function.
      The method returns both the action and the value associated with this action in this state.
    '''
    best_action = None
    best_val = None
    for a in mdp.applicable_actions(s):
        val = q.value(s,a)
        if best_val == None or best_val < val:
            best_action = a
            best_val    = val
    return best_action, best_val

#NOTE 给Action Value Function，对每一个state调用greedy_action得到policy。返回policy与State Value Function
def greedy_policy(mdp: MDP, q: ActionValueFunction) -> Tuple[Policy,StateValueFunction]:
    '''
      Computes the greedy policy associated with the specified action value function.  
      It also returns the associated state value function.
    '''
    result_pol = ExplicitPolicy(mdp)
    result_val = ExplicitStateValueFunction()
    
    for s in mdp.states():
        action, val = greedy_action(mdp, q, s)
        result_pol.set_action(s, action)
        result_val.set_value(s, val)
        
    return result_pol, result_val

#!------------------------------------------------------------------------------------------------------
#NOTE 对于(s,a)，计算 for all s' - Sum[P(s,a,s') * (r + gamma * V(s'))]
def one_step_lookahead(mdp: MDP, v: StateValueFunction, gamma: float, s: State, a: Action) -> float:
    '''
      Computes the one-step lookahead value for the specified pair state/action, given the specified state value function.
      The one-step lookahead is calculated by looking at all the possible states that can be reached from executing the action, 
      and adding their expected outcomes.
    '''
    value = 0
    for next_s, prob, rew in mdp.next_states(s,a):
        value += prob * (rew + (gamma * v.value(next_s)))
    return value

#NOTE 给定state value function。计算action value function
def compute_q_from_v(mdp: MDP, v: StateValueFunction, gamma: float) -> ActionValueFunction:
    '''
      Computes the action value function as a one-step lookahead value of the specified state value function.
    '''
    result = ExplicitActionValueFunction()
    for s in mdp.states():
        for a in mdp.applicable_actions(s):
            result.set_value(s, a, one_step_lookahead(mdp, v, gamma, s, a))
    return result

#NOTE 给定action value function和policy。policy给出action，action value function给出action的值
def compute_v_from_q_and_policy(mdp: MDP, pol: Policy, q: ActionValueFunction) -> StateValueFunction:
    '''
      Computes the state value function as a one-step lookahead value of the specified action value function 
      for the given policy.
    '''
    result = ExplicitStateValueFunction()
    for s in mdp.states():
        result.set_value(s, q.value(s, pol.action(s)))
    return result

#!------------------------------------------------------------------------------------------------------
#NOTE 给定一个State Value Function，根据 “贪婪算法”   给出的action来更新 “一次” 那个State Value Function
NB_BACKUPS = 0
def bellman_backup(mdp: MDP, v: StateValueFunction, gamma: float) -> Tuple[Policy,StateValueFunction]:
    '''
      Performs the Bellman backup for the specified state value function.
      Remember that the Bellamn backup is a greedy one-step lookahead of the existing state value function.
      This method also returns the current policy.
    '''
    global NB_BACKUPS
    q = compute_q_from_v(mdp, v, gamma)
    NB_BACKUPS += 1
    return greedy_policy(mdp, q)

#NOTE 给定一个State Value Function，根据 “特定policy” 给出的action来更新 “迭代n次” 那个State Value Function
def compute_v_of_policy(mdp: MDP, \
    pol: Policy, \
    gamma: float, \
    stopping_threshold: float, \
    starting_value: Optional[StateValueFunction] = None) -> StateValueFunction:
    '''
      Computes iteratively the value of each state for the specified policy with the specified discount factor gamma.
      The algorithm iteratively performs a backup until the backup change is below the specified stopping threshold.
      The user can specify a starting state value function; starting with a good value function can decrease the number of required iterations.
      (The result could also be computed as a system of linear equations.)
    '''
    current_svalue: StateValueFunction = ExplicitStateValueFunction() if starting_value == None else starting_value
    while True: # could bound the number of iterations
        qvalue     = compute_q_from_v(mdp, current_svalue, gamma)
        new_svalue = compute_v_from_q_and_policy(mdp, pol, qvalue)
        diff       = state_value_difference(mdp, current_svalue, new_svalue)
        if diff < stopping_threshold:
            return new_svalue
        current_svalue = new_svalue

#!------------------------------------------------------------------------------------------------------
#NOTE 对于那个policy，测试它是否在每一个state上选择的action的value都近似==贪婪算法的选择的值
def is_policy_nearly_greedy(mdp: MDP, pol: Policy, epsilon: float, q: ActionValueFunction):
    '''
      Indicates whether the specified policy is nearly greedy for the action value function, 
      i.e., whether the action it selects in each state has a value 
      that is at most epsilon away from the value of the state with maximal value.
    '''
    for s in mdp.states():
        a      = pol.action(s)
        avalue = q.value(s,a)
        _, greedy_avalue = greedy_action(mdp, q, s)
        if avalue + epsilon < greedy_avalue:
            return False
    return True

def policy_iteration(mdp: MDP, gamma: float, epsilon: float, stopping_threshold: float, starting_pi: Optional[Policy] = None) -> Policy:
    '''
      Performs the policy iteration algorithm.
      epsilon is used to determine when a policy is nearly optimal (cf. subroutine is_policy_nearly_greedy).
      stopping_threshold is used to determine when the value of a policy is precise enough (cf. policy compute_v_of_policy).
    '''
    pol = ExplicitPolicy(mdp) if starting_pi == None else starting_pi 
    while True:
        vs = compute_v_of_policy(mdp, pol, gamma, stopping_threshold)
        qs = compute_q_from_v(mdp, vs, gamma)
        if is_policy_nearly_greedy(mdp, pol, epsilon, qs):
            return pol
        pol, vs = greedy_policy(mdp, qs)

#NOTE 不断的执行bellman backup，效果等于compute_v_of_policy。
def value_iteration(mdp: MDP, gamma: float, epsilon: float) -> Tuple[Policy, StateValueFunction]:
    '''
      Performs the value iteration algorithm.
    '''
    vs = ExplicitStateValueFunction()
    while True:
        pol, newvs = bellman_backup(mdp, vs, gamma)
        diff = state_value_difference(mdp, vs, newvs)
        if diff < epsilon:
            return pol, newvs
        vs = newvs



# eof
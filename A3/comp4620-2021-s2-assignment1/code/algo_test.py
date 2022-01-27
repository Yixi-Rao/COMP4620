from typing import Dict, Tuple, Optional, Set, List, FrozenSet
from algos import ExplicitStateValueFunction, StateValueFunction, ActionValueFunction, ExplicitActionValueFunction

from random import random

from MDP import Action, MDP, State, Policy, ExplicitPolicy, History

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

# NOTE 给Action Value Function，贪婪算法决定当前state的action。返回action与action value
def greedy_action(mdp: MDP, q: ActionValueFunction, s: State) -> Tuple[Action, float]:
    '''
      Computes the greedy action in the specified state given the specified action value function.
      The method returns both the action and the value associated with this action in this state.
    '''
    best_action = None
    best_val = None
    for a in mdp.applicable_actions(s):
        val = q.value(s, a)
        if best_val == None or best_val < val:
            best_action = a
            best_val = val
    return best_action, best_val

# NOTE 给Action Value Function，对每一个state调用greedy_action得到policy。返回policy与State Value Function
def greedy_policy(mdp: MDP, q: ActionValueFunction) -> Tuple[Policy, StateValueFunction]:
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

# NOTE 给定state value function。计算action value function
def compute_q_from_v(mdp: MDP, v: StateValueFunction, gamma: float) -> ActionValueFunction:
    '''
      Computes the action value function as a one-step lookahead value of the specified state value function.
    '''
    result = ExplicitActionValueFunction()
    for s in mdp.states():
        for a in mdp.applicable_actions(s):
            result.set_value(s, a, one_step_lookahead(mdp, v, gamma, s, a))
    return result


# NOTE 给定一个State Value Function，根据 “贪婪算法”   给出的action来更新 “一次” 那个State Value Function
NB_BACKUPS = 0
def bellman_backup(mdp: MDP, v: StateValueFunction, gamma: float) -> Tuple[Policy, StateValueFunction]:
    '''
      Performs the Bellman backup for the specified state value function.
      Remember that the Bellamn backup is a greedy one-step lookahead of the existing state value function.
      This method also returns the current policy.
    '''
    global NB_BACKUPS
    q = compute_q_from_v(mdp, v, gamma)
    NB_BACKUPS += 1
    return greedy_policy(mdp, q)

# NOTE 不断的执行bellman backup，效果等于compute_v_of_policy。
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

def value_iteration1(mdp: MDP, gamma: float, epsilon: float) -> Tuple[Policy, StateValueFunction]:
    '''
      Performs the value iteration algorithm.
    '''
    vs = ExplicitStateValueFunction()
    while True:
        #! q = compute_q_from_v(mdp, vs, gamma)
        q = ExplicitActionValueFunction()
        for s in mdp.states():
            for a in mdp.applicable_actions(s):
                q.set_value(s, a, one_step_lookahead(mdp, vs, gamma, s, a))

        #! pol, newvs = greedy_policy(mdp, q)
        result_val = ExplicitStateValueFunction()
        for s in mdp.states():
            _, val = greedy_action(mdp, q, s)
            result_val.set_value(s, val)
            
        newvs = result_val
    
        diff = max([abs(vs.value(s) - newvs.value(s)) for s in mdp.states()])

        if diff < epsilon:
            return newvs
        vs = newvs

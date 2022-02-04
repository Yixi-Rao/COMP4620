from __future__ import annotations # Really?
from typing import Dict, List, Optional, Tuple
from interface import Action, Assignment1Domain, State

from policy import Policy

class ValueFunction: 
    '''
    This class implements a value function, 
    i.e., a mapping from states to floats.
    Given a value function V, the value of state s can be accessed and modified via:
      V[s]
    '''
    _domain: Assignment1Domain
    _values: Dict[State,float]
    _default_value: float

    def __init__(self, domain: Assignment1Domain, default_value: Optional[float] = 0): 
        self._domain = domain
        self._values = {  }
        self._default_value = default_value

    def __getitem__(self, state: State) -> float: 
        '''
        Defines accessor V[s]
        '''
        if state in self._values:
            return self._values[state]
        return self._default_value

    def __setitem__(self, state: State, value: float) -> None:
        '''
        Defines getter V[s]
        '''
        self._values[state] = value

    def q_value(self, state: State, action: Action, gamma: float) -> float:
        '''
        Returns the Q value of the specified action in the specified state, 
        using the current value function, with the specified discount factor gamma.
        '''
        # DONE
        sum_value = 0
        distribution = self._domain.get_next_state_distribution(state,action).get_values()
        for (next_state, probability) in distribution:
            sum_value += probability * (self._domain.get_transition_value(state,action,next_state).cost + gamma * self.__getitem__(next_state))


        return sum_value
    
    def compute_single_policy_backup(self, policy: Policy, gamma: float) -> Tuple[ValueFunction, float]:
        '''
        Performs a policy backup on the current value function 
        and using the specified policy.  
        This method does not modify the current value function; 
        instead it returns a new value function, 
        together with the error associated with the backup operation.
        '''
        # DONE
        new_value_function = ValueFunction(self._domain)
        error = 0
        for state in self._domain.get_observation_space().get_elements():
            if self._domain.is_terminal(state):
                new_value_function._values[state] = 0
            else:
                action = policy.__getitem__(state)
                # distribution = self._domain.get_next_state_distribution(state,action).get_values()
                new_value_function._values[state] = self.q_value(state,action,gamma)
                if error < abs(self.q_value(state,action,gamma) - self.__getitem__(state)):
                    error = abs(self.q_value(state,action,gamma) - self.__getitem__(state))


        return new_value_function, error

    def compute_bellmann_backup(self, gamma: float) -> Tuple[ValueFunction, float]:
        '''
        Performs a Bellmann Backup of the current value function 
        with the specified discount factor.
        This method does not modify the current value function; 
        instead it returns a new value function, 
        together with the Bellmann error.
        '''
        # DONE
        new_value_function = ValueFunction(self._domain)
        error = 0
        for state in self._domain.get_observation_space().get_elements():
            if self._domain.is_terminal(state):
                new_value_function.__setitem__(state,0)
            else:
                actions = self._domain.get_applicable_actions(state).get_elements()
                backup_value_candidates = [self.q_value(state,action,gamma) for action in actions]
                new_value_function._values[state] = min(backup_value_candidates)
            error = max(error, abs(new_value_function.__getitem__(state) - self.__getitem__(state)))

        return new_value_function, error

    def greedy_action(self, state: State, gamma: float) -> Tuple[Action,float]:
        '''
        Computes the greedy action that should be performed in the specified state 
        according to the current value function.
        This method also returns the Q value of the greedy action.
        '''
        # DONE
        actions = self._domain.get_applicable_actions(state).get_elements()
        greedy_values = [(action, self.q_value(state,action,gamma)) for action in actions]
        greedy_values_sorted = sorted(greedy_values,key= lambda x:x[1])
        return greedy_values_sorted[0]

    def greedy_policy(self, gamma: float) -> Policy:
        '''
        Computes the greedy policy of this value function.
        '''
        pol = Policy(self._domain)
        for state in self._domain.get_observation_space().get_elements():
            pol[state] = self.greedy_action(state, gamma)[0]
        return pol


    def print(self) -> None: 
        '''
        Prints out this value.
        '''
        print("+++++++")
        print("Values:")
        for state, value in self._values.items():
            print("State {} -> {}".format(state, value))


def compute_value_function_of_policy(pol: Policy, gamma: float, epsilon: Optional[float] = 0.01) -> ValueFunction:
    '''
    Computes an approximated value function of the specified policy (V_{pi})
    by running the iterative algorithm described in the lecture.
    '''
    # DONE
    value_function = ValueFunction(pol.get_domain())
    while value_function.compute_single_policy_backup(pol,gamma)[1] != 0:
        value_function = value_function.compute_single_policy_backup(pol,gamma)[0]
    return value_function

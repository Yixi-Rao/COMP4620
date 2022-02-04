from enum import Enum
from typing import Optional, Dict, Tuple
import sys

from interface import Assignment1Domain, State, Action
from skdecide import MDPDomain, TransitionValue, DiscreteDistribution, Space, EnumerableSpace
from skdecide.builders.solver import DeterministicPolicies

from value import ValueFunction
from policy import Policy

class ValueIteration:
    '''
    ValueIteration is the class that is used to perform the Value Iteration algorithm.
    It contains the domain, the current value function, and other misc information.
    Importantly, _max_value indicates the maximum value 
    that one can expect to associate with a state: 
    if the state is and stays above that value, 
    it is assumed that its value is not changing anymore.
    '''
    _domain: Assignment1Domain
    _values: ValueFunction
    _max_value: float
    _gamma: float
    _nb_iterations: int

    def __init__(self, domain: Assignment1Domain, max_value: Optional[float] = 1000, gamma: Optional[float] = 0.9, initial_value: Optional[float] = 0):
        self._domain = domain
        self._values = ValueFunction(domain, default_value=initial_value)
        self._max_value = max_value
        self._gamma = gamma
        self._nb_iterations = 0

    def value(self, state: State) -> float:
        '''
        Returns the current value of the specified state.
        '''
        return self._values[state]

    def single_backup(self) -> float:
        '''
        Performs a single Bellmann backup as implemented in value.py, 
        and returns the Bellmann error associated with this backup.
        '''
        self._values, error = self._values.compute_bellmann_backup(self._gamma)
        self._nb_iterations += 1
        return error

    def backup(self, epsilon: float = 0.01, max_iteration: Optional[int] = None) -> None:
        '''
        Performs the Value Iteration algorithm
        until the error is below the epsilon threshold, 
        or until the number of iterations is above the specified value.
        '''
        # DONE
        if max_iteration is not None:
            while self.single_backup() > epsilon:
                if self._nb_iterations > max_iteration:
                    return
        else:
            while True:
                if self.single_backup() < epsilon:
                    return
        return

    def policy(self) -> Policy: 
        '''
        Returns the greedy policy for the current value function.
        '''
        return self._values.greedy_policy(self._gamma)

    def nb_iterations(self): 
        '''
        Indicates how many iterations have been executed so far.
        '''
        return self._nb_iterations

if __name__ == '__main__':
    import example1
    domain = example1.example_1()

    vi = ValueIteration(domain)

    print()
    vi._values.print()
    print()
    vi.policy().print()

    error = vi.single_backup()

    print()
    print("Error: {}".format(error))
    vi._values.print()
    print()
    vi.policy().print()

    error = vi.single_backup()

    print()
    print("Error: {}".format(error))
    vi._values.print()
    print()
    vi.policy().print()

    vi.backup(0.001)
    
    print()
    vi._values.print()
    print()
    vi.policy().print()

'''
+++++++
Values:

+++++++
Policy:
State NoFork -> DoNothing
State Fork1 -> DoNothing
State Fork2 -> DoNothing
State Fork12 -> Eat

Error: 30.0
+++++++
Values:
State NoFork -> 0.0
State Fork1 -> 0.0
State Fork2 -> 0.0
State Fork12 -> -30.0

+++++++
Policy:
State NoFork -> DoNothing
State Fork1 -> Pick2
State Fork2 -> Pick1
State Fork12 -> Eat

Error: 19.3
+++++++
Values:
State NoFork -> 0.0
State Fork1 -> -4.3
State Fork2 -> -19.3
State Fork12 -> -30.0

+++++++
Policy:
State NoFork -> DoNothing
State Fork1 -> Pick2
State Fork2 -> Pick1
State Fork12 -> Eat

+++++++
Values:
State NoFork -> -1.7040500184222633
State Fork1 -> -7.449732944847336
State Fork2 -> -21.211200834755594
State Fork12 -> -31.53275627167941

+++++++
Policy:
State NoFork -> Pick1
State Fork1 -> Pick2
State Fork2 -> Pick1
State Fork12 -> Eat

'''
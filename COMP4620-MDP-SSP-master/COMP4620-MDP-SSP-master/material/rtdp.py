from typing import Dict, Optional, Tuple
from interface import Assignment1Domain, State, Action
from random import random
from value import ValueFunction
from policy import Policy

def take_one_random_step(domain: Assignment1Domain, state: State, action: Action) -> State:
    '''
      Simulates the execution of the specified action in the specified state.
    '''
    rand = random()
    for nextstate, prob in domain.get_next_state_distribution(state, action).get_values():
        if prob > rand: 
            return nextstate
        rand -= prob
    raise Exception("Could not find next state.  Is the probability distribution correct?  (State {}, Action {})".format(state, action))

class Simulation:
    '''
      Simulation is the class that represents a trial.
      It consists of a domain, 
      a value function (that can be used to choose the next action), 
      the current state, 
      and some misc information.
    '''
    _domain: Assignment1Domain
    _values: ValueFunction
    _gamma: float
    _current_state: State
    _max_depth: int
    _current_depth: int

    def __init__(self, domain: Assignment1Domain, values: ValueFunction, gamma: float, max_depth: int, initial_state: Optional[State] = None):
        self._domain = domain
        self._values = values
        self._gamma = gamma
        self._current_state = self._domain.get_initial_state() if initial_state == None else initial_state
        self._max_depth = max_depth
        self._current_depth = 0

    def one_step_simulate_and_update(self) -> None:
        '''
          Performs a single step of the simulation: 
          * update the value of the current state
          * choose the next action
          * simulate the next action
          * update the number of steps
        '''
        # DONE
        (action, value) = self._values.greedy_action(self._current_state,self._gamma)
        self._values.__setitem__(self._current_state,value)
        self._current_depth+=1
        # distribution = self._domain.get_next_state_distribution(self._current_state,action)
        self._current_state = take_one_random_step(self._domain,self._current_state,action)
        return
        
    def run_simulation(self) -> None:
        '''
          Runs the complete simulation.
        '''
        while self._current_depth < self._max_depth: 
            self.one_step_simulate_and_update()

class RTDP: 
    '''
    RTDP is the class that is used to perform the Real-Time Dynamic Programming algorithm.
    It contains the domain and the current value function.
    '''
    _domain: Assignment1Domain
    _values: Dict[State, float]
    _gamma: float

    def __init__(self, domain: Assignment1Domain, gamma: float, h: Optional[int] = None):
        self._domain = domain
        # Here is one way to compute a safe heuristic: 
        # take the smallest cost and divide it by (1 - gamma)
        if h == None:
            smallest = min( [ domain.get_transition_value(state, action, next_state).cost \
                for state in domain.get_observation_space().get_elements() \
                for action in domain.get_applicable_actions(state).get_elements() \
                for (next_state,_) in domain._get_next_state_distribution(state,action).get_values() \
                ] )
            h = smallest / (1 - gamma) # gamma should not be 1!
        self._values = ValueFunction(domain, default_value=h)
        self._gamma = gamma

    def run_simulation(self, depth: int) -> None:
        '''
          Runs a single simulation up to specified depth.
        '''
        sim: Simulation = Simulation(self._domain, self._values, self._gamma, depth)
        sim.run_simulation()

    def run_n_simulations(self, n: int, depth: int) -> None:
        '''
          Runs the specified number of simulations.
        '''
        for _k in range(n): 
            self.run_simulation(depth)

    def policy(self) -> Policy: 
        return self._values.greedy_policy(self._gamma)


if __name__ == '__main__':
    import example1
    domain = example1.example_1()

    rtdp = RTDP(domain, 0.9)

    policy = rtdp.policy()
    policy.print()

    rtdp.run_n_simulations(5, 10)

    policy = rtdp.policy()
    policy.print()

    rtdp.run_n_simulations(50, 100)

    policy = rtdp.policy()
    policy.print()
'''
+++++++
Policy:
State NoFork -> DoNothing
State Fork1 -> DoNothing
State Fork2 -> DoNothing
State Fork12 -> Eat
+++++++
Policy:
State NoFork -> Pick1
State Fork1 -> Pick2
State Fork2 -> Pick1
State Fork12 -> DoNothing
+++++++
Policy:
State NoFork -> Pick1
State Fork1 -> Pick2
State Fork2 -> Pick1
State Fork12 -> Eat
'''
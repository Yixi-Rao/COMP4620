from enum import Enum
from typing import Optional, Dict
import sys

from skdecide import MDPDomain, TransitionValue, DiscreteDistribution, Space, EnumerableSpace
from skdecide.builders.solver import DeterministicPolicies

class State:
    pass

# Example of Action type (adapt to your needs)
class Action:
    pass


class Assignment1Domain(MDPDomain):
    def _get_transition_value(self, state: State, action: Action, next_state: Optional[State] = None) -> TransitionValue:
        raise NotImplementedError
    
    def _get_next_state_distribution(self, state: State, action: Action) -> DiscreteDistribution[State]:
        raise NotImplementedError
    
    def _is_terminal(self, state: State) -> bool:
        return False
    
    def _get_applicable_actions_from(self, state: State) -> EnumerableSpace[Action]:
        raise NotImplementedError
    
    def _get_action_space_(self) -> EnumerableSpace[Action]:
        raise NotImplementedError
    
    def _get_initial_state_(self) -> State:
        raise NotImplementedError
    
    def _get_observation_space_(self) -> EnumerableSpace[State]:
        raise NotImplementedError


# eof
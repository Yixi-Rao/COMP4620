from typing import Dict, Tuple, List, Optional
from dataclasses import dataclass
from interface import Assignment1Domain, State, Action
from skdecide import DiscreteDistribution, TransitionValue
from skdecide.hub.space.gym import ListSpace

class SMState(State):
    _name: str

    def __init__(self, name: str):
        self._name = name

    def __repr__(self):
        return self._name

    def name(self) -> str: 
        return self._name


class SMAction(Action):
    _name: str

    def __init__(self, name: str):
        self._name = name

    def __repr__(self):
        return self._name

    def name(self) -> str: 
        return self._name

@dataclass
class SMTransition(): 
    origin: str
    action: str
    cost: float
    prob_distribution: List[Tuple[str, float]]

class StateMachine(Assignment1Domain):

    _name_to_state: Dict[str, SMState]
    _name_to_action: Dict[str, SMAction]
    _initial_state: SMState
    _state_to_action_to_output: Dict[State, Dict[Action, Tuple[int,DiscreteDistribution]]]

    def __init__(self, \
            transition_function: List[SMTransition], \
            initial_state: str):
        self._name_to_state = {}
        self._name_to_action = {}
        self._state_to_action_to_output = {}

        trans: SMTransition
        for trans in transition_function:
            origin = self.state(trans.origin)
            action = self.action(trans.action)
            distrib = DiscreteDistribution(
                [ (self.state(target_name), prob) for (target_name,prob) in trans.prob_distribution]
            )
            self._state_to_action_to_output[origin][action] = (trans.cost, distrib)

        self._initial_state = self.state(initial_state)

    def state(self, name: str) -> SMState:
        if name in self._name_to_state:
            return self._name_to_state[name]
        state = SMState(name)
        self._name_to_state[name] = state
        self._state_to_action_to_output[state] = {}
        return state

    def action(self, name: str) -> SMAction:
        if name in self._name_to_action:
            return self._name_to_action[name]
        action = SMAction(name)
        self._name_to_action[name] = action
        return action

    def  _get_transition_value(self, state: SMState, action: SMAction, next_state: Optional[SMState] = None) -> TransitionValue:
        (value,_distrib) = self._state_to_action_to_output[state][action]
        return TransitionValue(cost=value)
    
    def _get_next_state_distribution(self, state: SMState, action: SMAction) -> DiscreteDistribution[State]:
        (_value,distrib) = self._state_to_action_to_output[state][action]
        return distrib
    
    def _is_terminal(self, state: State) -> bool:
        return False
    
    def _get_applicable_actions_from(self, state: State) -> ListSpace[Action]:
        return ListSpace(self._state_to_action_to_output[state].keys())
    
    def _get_action_space_(self) -> ListSpace[Action]:
        return self._name_to_action.values()
    
    def _get_initial_state_(self) -> State:
        return self._initial_state
    
    def _get_observation_space_(self) -> ListSpace[State]:
        return ListSpace(self._name_to_state.values())


# eof

from __future__ import annotations # Really?
from typing import Dict, List, Optional
from interface import Action, Assignment1Domain, State

class Policy:
    '''
    This class implements a policy, 
    i.e., a mapping from states to actions.
    Given a policy pol, the value of state s can be accessed and modified via:
      pol[s]
    '''
    _domain: Assignment1Domain
    _actions: Dict[State, Action]

    def __init__(self, domain: Assignment1Domain, default_action: Optional[Action] = None): 
        self._domain = domain
        self._actions = {}
        for state in domain.get_observation_space().get_elements():
            actions = domain.get_applicable_actions(state).get_elements()
            if default_action != None and default_action in actions: 
                self._actions[state] = default_action
            else: 
                self._actions[state] = actions[0]

    def __getitem__(self, state: State) -> Action: 
        '''
        Defines accessor pol[s]
        '''
        return self._actions[state]

    def __setitem__(self, state: State, action: Action) -> None:
        '''
        Defines getter pol[s]
        '''
        self._actions[state] = action

    def get_domain(self) -> Assignment1Domain: 
        return self._domain

    def __eq__(self, other: Policy) -> bool: 
        return self._actions == other._actions


    def print(self) -> None: 
        print("+++++++")
        print("Policy:")
        for state, action in self._actions.items():
            print("State {} -> {}".format(state, action))



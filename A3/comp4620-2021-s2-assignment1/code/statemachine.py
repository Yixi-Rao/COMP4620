from dataclasses import dataclass
from typing import Dict, List, Tuple

from MDP import Action, MDP, State, Policy

'''
  The State Machine MDP.
'''

class SMState(State):
    def __init__(self, name: str):
        self._name = name

    def __repr__(self):
        return self._name

    def name(self) -> str: 
        return self._name

class SMAction(Action):
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
    prob_distribution: List[Tuple[str, float, float]]

class SMMDP(MDP):
    def __init__(self, 
      transitions: List[SMTransition], 
      initial_state: str):
        self._states      = {} # string -> State
        self._actions     = {} # string -> Action
        self._transitions = {} # State -> Action -> list of State * float * float
        trans: SMTransition = None
        for trans in transitions: 
            origin: State = self.get_state(trans.origin)
            action: Action = self.get_action(trans.action)
            outcome = []
            for succname, prob, rew in trans.prob_distribution:
                succ: State = self.get_state(succname)
                outcome.append( (succ, prob, rew) )
            self._transitions[origin][action] = outcome

        self._initial_state = self.get_state(initial_state)
    
    def get_state(self, sname: str):
        '''
        Makes sure that the MDP knows about this state
        '''
        if not (sname in self._states):
            s = SMState(sname)
            self._states[sname] = s
            self._transitions[s] = {}
        return self._states[sname]
    
    def get_action(self, aname: str):
        '''
        Makes sure that the MDP knows about this action
        '''
        if not (aname in self._actions):
            a = SMAction(aname)
            self._actions[aname] = a
        return self._actions[aname]

    def states(self) -> List[State]:
        return [ s for (name,s) in self._states.items() ]

    def actions(self) -> List[Action]:
        return [ a for (name,a) in self._actions.items() ]

    def applicable_actions(self, s: State) -> List[Action]:
        return self._transitions[s].keys()

    def next_states(self, s: State, a: Action) -> List[Tuple[State,float,float]]:
        return self._transitions[s][a]
    
    def initial_state(self) -> State:
        return self._initial_state

    def print(self) -> None:
        print(f'{self.initial_state()}')
        for state in self.states():
            for action in self.applicable_actions(state):
                outcome = self.next_states(state, action)
                print(f'{state} {action} {outcome}')

def read_state_machine(file) -> SMMDP: 
    import re # pip install regex
    exp = re.compile('(\S+)\s+(\S+)\s+(.*)')
    exp2 = re.compile('\(\s*(\S+)\s*,\s*(\S+)\s*,\s*(\S+)\s*\)')
    with open(file,'r') as input:
        initial_state = input.readline().strip()
        transes = []
        for line in input.readlines():
            m = exp.match(line)
            orig = m.group(1)
            action = m.group(2)
            outcome = m.group(3)
            trans = SMTransition(orig, action, exp2.findall(outcome))
            transes.append(trans)
    return SMMDP(transes, initial_state)

def state_machine_from_mdp(mdp: MDP) -> Tuple[SMMDP,Dict[SMState,State],Dict[SMAction,Action]]:
    state_to_str = {}
    str_to_state = {}
    
    action_to_str = {}
    str_to_action = {}

    nbstates  = [0]
    nbactions = [0]

    transitions = []
    initial_str = None

    def get_state(state: State) -> str:
        if state in state_to_str:
            return state_to_str[state]
        result = f'state_{nbstates[0]}'
        nbstates[0] += 1
        state_to_str[state] = result
        str_to_state[result] = state
        return result

    def get_action(action: Action) -> str:
        if action in action_to_str:
            return action_to_str[action]
        result = f'act_{nbactions[0]}'
        nbactions[0] += 1
        action_to_str[action] = result
        str_to_action[result] = action
        return result

    str_initial = get_state(mdp.initial_state())
    
    open_set  = set()
    known = set()
    open_set.add(mdp.initial_state())
    known.add(mdp.initial_state())

    fo = open("foo.txt", "w")
    while open_set:
        state     = open_set.pop()
        fo.write("!state: "+str(state) + "\n")
        str_state = get_state(state)
        for act in mdp.applicable_actions(state):
            str_act = get_action(act)
            fo.write("---!action: "+str(act)+ "\n")

            # copy the successors in open/known
            for next_state, _prob, _rew in mdp.next_states(state, act):
                fo.write("---!next_state(" + str(_prob) + ") " + str(int(_rew)) + "$ : "+str(next_state)+ "\n")
                if not next_state in known:
                    
                    open_set.add(next_state)
                    known.add(next_state)
            
            trans = SMTransition( str_state, str_act, [ (get_state(next_state), prob, rew) for (next_state, prob, rew) in mdp.next_states(state, act)])
            transitions.append(trans)
        fo.write("\n")
    fo.close()
    smmdp = SMMDP(transitions, str_initial)
    return (
        smmdp, 
        { smmdp.get_state(str_state) : state for state, str_state in state_to_str.items() },
        { smmdp.get_action(str_act)  : act   for act,   str_act   in action_to_str.items() }
    )
    
    # Tuple[SMMDP,Dict[SMState,State],Dict[SMAction,Action]]:

class TranslatedPolicy(Policy):
    def __init__(self, pol, state_translater, action_translater):
        self.pol_               = pol
        self.state_translater_  = state_translater
        self.action_translater_ = action_translater

    def action(self, s: State) -> Action:
        act = self.pol_.action(self.state_translater_[s])
        return self.action_translater_[act]

# eof
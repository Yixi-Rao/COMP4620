# MDP.py
# Contains classes and methods to represent and manipulate MDPs, policies, and values.

from typing import List, Tuple, Optional

class State:
    pass

class Action: 
    pass

class MDP:
    '''
      This class is the basic interface for an MDP.
      Implementations of MDPs include SMMDP in file statemachine.py
    '''
    def states(self) -> List[State]:
        pass

    def actions(self) -> List[Action]:
        pass

    def applicable_actions(self, s: State) -> List[Action]:
        pass

    def next_states(self, s: State, a: Action) -> List[Tuple[State,float,float]]:
        '''
          Returns the outcome of performing action a in state s.  
          Defined as a list of elements [s',prob,rew] 
          where s' is the next state, 
          prob is the probability of reaching this state, 
          and rew is the reward.
        '''
        pass
    
    def initial_state(self) -> State:
        pass

class Policy:
    '''
        The interface for a deterministic Markov Policy
    '''
    def action(self, s: State) -> Action:
        print(f'{type(self).__name__} action function not implemented')

class ExplicitPolicy(Policy):
    '''
      A DM Policy explicitly represented as a dictionary with default action of the first applicable action.
    '''
    def __init__(self, mdp: MDP):
        self.mdp = mdp
        self._explicit_decision = {}

    def set_action(self, s: State, a: Action):
        self._explicit_decision[s] = a

    def action(self, s: State):
        if not s in self._explicit_decision:
            self.set_action(s, next(iter(self.mdp.applicable_actions(s)))) # takes the first action from the set of applicable actions
        return self._explicit_decision[s]

class History:
    def __init__(self, mdp: Optional[MDP] = None, init_state: Optional[State] = None, h: Optional = None):
        if not h is None:
            self.mdp_ = h.mdp_
            self.seq_ = h.seq_.copy()
            return
        self.mdp_ = mdp
        self.seq_ = [ init_state ] if not init_state is None else [ mdp.initial_state() ]
    
    def __repr__(self):
        strings = []
        for o in self.seq_:
            strings.append(str(o))
        return ' '.join(strings)

    def pretty_repr(self) -> List[str]:
        strings = []
        for i in range(self.length()):
            strings.append( str(self.state(i)) + '\taction: ' + str(self.action(i)) + '\treward: ' + str(self.reward(i)))
        strings.append(str(self.state(self.length())))
        return strings

    def add(self, act: Action, state: State, rew: float) -> None:
        self.seq_.append(act)
        self.seq_.append(rew)
        self.seq_.append(state)

    def state(self, i) -> State:
        '''
          From 0 to length() inclusive
        '''
        return self.seq_[i*3]

    def action(self, i) -> Action:
        '''
          From 0 to length()-1 inclusive
        '''
        return self.seq_[1 + (i*3)]

    def reward(self, i) -> float:
        '''
          From 0 to length()-1 inclusive
        '''
        return self.seq_[2 + (i*3)]

    def length(self) -> int:
        return len(self.seq_) // 3

    def last_state(self) -> State:
        return self.state(self.length())

# eof
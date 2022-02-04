from random import random, choice
from typing import Optional

from MDP import Action, State
from domain import RLEnvironment

class Q:
    '''
      A Q class is a class that represents an estimate of a pair state/action.
      Different implementations are proposed below
    '''

    def __init__(self):
        pass

    def value(self, state: State, action: Action) -> float:
        '''
          The value associated with the specified pair state/action.  
          Not implemented in this class.
        '''
        pass

    def learn(self, state: State, action: Action, reward: float) -> None:
        '''
          Tells this Q that the last execution of action in state 
          led to the specified (long-term) reward.
        '''
        pass

class LastValueQ(Q):
    '''
      An example implementation of a Q.  
      The value of a pair state is the value of the last execution of that state pair, 
      and 0 if it has never been applied.
    '''
    def __init__(self, default: Optional[float] = 0):
        self.default_ = default
        self.values_ = {}

    def value(self, state: State, action: Action) -> float:
        if (state,action) in self.values_:
            return self.values_[state,action]
        return self.default_

    def learn(self, state: State, action: Action, reward: float) -> None:
        self.values_[state,action] = reward

class Average(Q):
    '''
      An implementation of Q where the value of a pair state/action is the average 
      of the value received so far (default, if there is no value).
    '''
    def __init__(self, default: Optional[float] = 0):
        self.default_ = default
        self.values_ = {}
        self.counts_ = {}

    def value(self, state: State, action: Action) -> float:
        if (state,action) in self.values_:
            return self.values_[state,action]
        return self.default_

    def learn(self, state: State, action: Action, reward: float) -> None:
        if self.counts_.get((state, action)) == None:
            self.counts_[(state, action)] = 1
            self.values_[state, action] = reward
        else:
            self.counts_[(state, action)] = self.counts_[(state, action)] + 1
            Est = self.value(state, action)
            self.values_[state, action] = (Est + reward) / self.counts_[(state, action)]
        

class TemporalDifference(Q):
    '''
      An implementation of Q where the value of a pair state/action is updated 
      using temporal difference (default value is 0).
    '''
    def __init__(self, alpha: float, default: Optional[float] = 0):
        self.alpha_   = alpha
        self.default_ = default
        self.values_  = {}

    def value(self, state: State, action: Action) -> float:
        if (state, action) in self.values_:
            return self.values_[state, action]
        return self.default_

    def learn(self, state: State, action: Action, reward: float) -> None:
        Est = self.value(state, action)
        self.values_[state, action] = Est + self.alpha_ * (reward - Est)
    
'''
  Generic methods for Q
'''


def greedy_action(q: Q, env: RLEnvironment) -> Action:
    '''
      Computes the greedy action, according to q, 
      for the current state in the environment.
    '''
    cur_state   = env.current_state()
    app_actions = env.applicable_actions()
    
    return app_actions[max([(q.value(cur_state, a), i) for i, a in enumerate(app_actions)])[1]]

def epsilon_greedy_action(q: Q, env: RLEnvironment, epsilon: float) -> Action:
    '''
      Computes the greedy action, according to q, 
      for the current state in the environment.
    '''
    if random() < epsilon:
        app_actions = env.applicable_actions()
        return choice(app_actions) 
    else:
        return greedy_action(q, env)

# eof
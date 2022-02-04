from typing import Optional

from domain import RLEnvironment
from q import Q, TemporalDifference, epsilon_greedy_action, greedy_action

class QLearning:
    '''
      An implementation of Q learning.
    '''
    def __init__(self, domain: RLEnvironment, epsilon: float, gamma: float, q: Optional[Q] = TemporalDifference(alpha=.01)):
        self.domain_ = domain
        self.ε       = epsilon
        self.γ       = gamma
        self.q_      = q
        
        self.domain_.reset()
        self.cur_s_ = self.domain_.current_state()

    def reset(self):
        '''
          Resets the domain to its initial state
        '''
        self.domain_.reset()
        self.cur_s_ = self.domain_.current_state()

    def execute_one_action(self):
        '''
          Executes one action according to the QLearning strategy, and updates the Q value function.
        '''
        cur_a  = epsilon_greedy_action(self.q_, self.domain_, self.ε)
        Tout   = self.domain_.execute(cur_a)
        r      = Tout.reward
        next_s = Tout.state
        next_a = greedy_action(self.q_, self.domain_)
        
        self.q_.learn(self.cur_s_, cur_a,
                      r + self.γ * self.q_.value(next_s, next_a))
        
        self.cur_s_ = next_s

# eof
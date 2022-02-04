from typing import Optional

from domain import RLEnvironment
from q import Q, TemporalDifference, epsilon_greedy_action

class Sarsa:
    '''
      An implementation of SARSA.
    '''

    def __init__(self, domain: RLEnvironment, epsilon: float, gamma: float, q: Optional[Q] = TemporalDifference(alpha=.01)):
        self.domain_ = domain
        self.ε       = epsilon
        self.γ       = gamma
        self.q_      = q
        
        self.domain_.reset()
        self.cur_s_ = self.domain_.current_state()
        self.cur_a_ = epsilon_greedy_action(self.q_, self.domain_, self.ε)

    def reset(self):
        '''
          Resets the domain to its initial state
        '''
        self.domain_.reset()
        self.cur_s_ = self.domain_.current_state()
        self.cur_a_ = epsilon_greedy_action(self.q_, self.domain_, self.ε)
        

    def execute_one_action(self):
        '''
          Executes one action according to the SARSA strategy, and updates the Q value function.
        '''
        Tout   = self.domain_.execute(self.cur_a_)
        r      = Tout.reward
        next_s = Tout.state
        next_a = epsilon_greedy_action(self.q_, self.domain_, self.ε)
        
        self.q_.learn(self.cur_s_, self.cur_a_, r + self.γ * self.q_.value(next_s, next_a))
        # if isinstance(self.q_, TemporalDifference):
        #     self.q_.learn(self.cur_s_, self.cur_a_, r + self.γ * self.q_.value(next_s, next_a))
        # else:
        #     self.q_.learn(self.cur_s_, self.cur_a_, r)
        
        self.cur_s_ = next_s
        self.cur_a_ = next_a

# eof
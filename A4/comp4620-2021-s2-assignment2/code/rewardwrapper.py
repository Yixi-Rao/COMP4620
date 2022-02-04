from typing import List

from domain import Action, State, RLEnvironment, TransitionOutcome

class RewardWrapper(RLEnvironment):
    '''
      A reward wrapper is a wrapper for a RL domain 
      that keeps track of how much reward was collected during execution
    '''
    _domain: RLEnvironment # the wrapped domain
    _rewards: List[float]

    def __init__(self, domain: RLEnvironment):
        self.domain_ = domain
        self.rewards_ = []

    def reset(self) -> State:
        return self.domain_.reset()
    
    def applicable_actions(self) -> List[Action]:
        return self.domain_.applicable_actions()

    def execute(self, action: Action) -> TransitionOutcome:
        result = self.domain_.execute(action)
        self.rewards_.append(result.reward)
        return result
    
    def current_state(self) -> State:
        return self.domain_.current_state()

    def get_reward_summary(self, gamma: float) -> List[float]:
        '''
          Returns the *weighted* rewards accumulated so far.
          If rewards is the array of rewards gathered and result is the output of this method, 
          then result[i] = rewards[i] + gamma * rewards[i+1] + gamma^2 * rewards[i+2] + ...
          where rewards[j] = 0 for all j > len(rewards).
          Notice that the very last values of results should be ignored (because rewards[i+k] == 0 for small k).
        '''
        result: List[int] = []

        if len(self.rewards_) != 0:
            result.append(self.rewards_[-1])
        for i in range(len(self.rewards_)-1,-1,-1): # iterate from the last element
            result.append(self.rewards_[i] + gamma * result[-1])

        result.reverse()
        return result

#eof
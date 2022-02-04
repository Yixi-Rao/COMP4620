from typing import Tuple, TypeVar, Generic, List
from dataclasses import dataclass

from random import random
from MDP import Action, State, MDP

@dataclass(unsafe_hash=True)
class TransitionOutcome:
    '''
      The outcome of a transition defined as a pair: state, reward
    '''
    state: State
    reward: float

T = TypeVar('T')

class DiscreteDistribution(Generic[T]):
    '''
      A probability distribution over a finite set of elements of type T.
      This distribution is meant to be immutable.
    '''
    def __init__(self, distribution: List[Tuple[T,float]]):
        '''
          A list of elements T with their probability.  
          The sum of probabilities should add up to 1.
        '''
        self.distrib_ = distribution

    def sample(self) -> T:
        '''
          Returns an element from this probability distribution drawn at random.
        '''
        r = random()
        for t,prob in self.distrib_:
            if r <= prob:
                return t
            r = r - prob
        print('Warning: probability distribution does not add up to 1.  Returning None.')
        return None

class RLEnvironment:
    '''
      A Reinforcement Learning Environment is a black box 
      that an agent can interact with.  
      It has a current state.  
      The agent can reset the state back to initial, 
      query the applicable actions, and execute one of these actions 
      (which modifies the state and returns a reward).
    '''

    def reset(self) -> State:
        '''
          Sends the environment back to the initial state, 
          and returns this state.
        '''
        pass
    
    def applicable_actions(self) -> List[Action]:
        '''
          Returns the list of actions appicable in the current state.
        '''
        pass

    def execute(self, action: Action) -> TransitionOutcome:
        '''
          Execute the specified action, and returns the new state alongside the reward.
        '''
        pass
    
    def current_state(self) -> State:
      '''
        Returns the current state.
      '''
      pass



class RL_MDP(RLEnvironment):
    '''
      An RL MDP is an RL Environment that sits on top of an MDP, 
      i.e., a mathematical representation of a system.  
      Not every RLEnvironment is built from an MDP object.  
      For instance, an RLEnvironment could be connected to the real world.
    '''

    def __init__(self, mdp: MDP):
        self.mdp_ = mdp
        self.reset()

    def reset(self) -> State:
        self.current_state_ = self.mdp_._initial_state()
    
    def applicable_actions(self) -> List[Action]:
        return self.mdp_.applicable_actions(self.current_state_)

    def execute(self, action: Action) -> TransitionOutcome:
        next_state_prob_rew = self.mdp_.next_states(self.current_state_, action)
        # chooses the random effect: select the pair (state,rew) all probas so far add up to more than the randomly selected value
        r = random()
        for state, prob, rew in next_state_prob_rew:
            if prob >= r:
                self.current_state_ = state
                return TransitionOutcome(state=self.current_state_, reward=rew)
            r -= prob
        print('Warning: probability distribution does not add up to 1.  Returning None.')
        return None
    
    def current_state(self) -> State:
        return self.current_state_
    
# eof
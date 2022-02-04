from dataclasses import dataclass
from enum import Enum
from typing import List

from domain import Action, State, RLEnvironment, DiscreteDistribution, TransitionOutcome

'''
  This file implements a domain that is a parody of a cricket game in which we have to decide
  whether the batters should run, stop, or move back (I did not find technical terms for the decisions)
  depending on the distance of the ball.
'''

MAX_NB_RUNS = 5 # the max number of points that the players can make
MAX_BALL_DISTANCE = 20 # how far from the wicket the ball can be
ADVANCEMENT_FOR_RUN = 5 # how much both batters should advance to add a run

REWARD_FOR_LOSING = -10

@dataclass(unsafe_hash=True)
class CricketState(State):
    '''
      The state of a cricket game.  Should be immutable.
      No notion of tiredness here.
    '''
    nb_runs_: int # how many points the batters are currently making
    ball_distance_: int # how far from the wicket the ball currently is (when this value is zero, the batters should have 0 advancement!)
    batter1_adv_: int # how far the first player has advanced from the wicket
    batter2_adv_: int


class CricketAction(Enum):
    '''
      Simplifications:
      * both players do the same action (for instance, it is not the case that player 1 runs while player 2 backs off)
      * players know what the other player is doing
    '''
    STOP = 0
    RUN = 1
    BACKOFF = 2


class CricketDomain(RLEnvironment):
    '''
        The cricket domain is parametrised by the following variables, 
        which means that there can be many different variations of the domain.
    '''
    first_batter_speed_: DiscreteDistribution[int] # the probability that the first player will advance by k steps when running (we assume they always backoff by one)
    second_batter_speed_: DiscreteDistribution[int]
    ball_speed_: DiscreteDistribution[int] # how fast the ball travels back to the wicket
    batting_strength_: DiscreteDistribution[int] # same for both players.  No strategy here in choosing the non-stricking batter
    initial_state_: CricketState

    def __init__(self
        , first_batter_speed:DiscreteDistribution[int]
        , second_batter_speed: DiscreteDistribution[int]
        , ball_speed: DiscreteDistribution[int]
        , batting_strength: DiscreteDistribution[int]
        ):
        self.first_batter_speed_ = first_batter_speed
        self.second_batter_speed_ = second_batter_speed
        self.ball_speed_ = ball_speed
        self.batting_strength_ = batting_strength
        self.initial_state_ = CricketState(nb_runs_=0, ball_distance_=0, batter1_adv_=0, batter2_adv_=0)
        self.reset()

    def reset(self):
        self.current_state_ = self.initial_state_

    def applicable_actions(self) -> List[Action]:
        if self.current_state_ == self.initial_state_:
            # In initial state, the ball is being thrown, so the players have to wait.
            return [CricketAction.STOP]
        return [CricketAction.STOP, CricketAction.RUN, CricketAction.BACKOFF]

    def execute(self, action: Action) -> TransitionOutcome:
        state = self.current_state_
        if state == self.initial_state_:
            # Throwing the ball
            new_state = CricketState(nb_runs_=0, batter1_adv_=0, batter2_adv_=0, ball_distance_=self.batting_strength_.sample())
            self.current_state_ = new_state
            return TransitionOutcome(state=new_state,reward=0)

        new_nb_runs = state.nb_runs_
        new_batter1_adv: int = state.batter1_adv_
        new_batter2_adv: int = state.batter2_adv_
        if action == CricketAction.BACKOFF:
            if new_batter1_adv > 0:
                new_batter1_adv -= 1
            if new_batter2_adv > 0:
                new_batter2_adv -= 1
        if action == CricketAction.RUN:
            new_batter1_adv += self.first_batter_speed_.sample()
            if new_batter1_adv > ADVANCEMENT_FOR_RUN: # stops after reaching max
                new_batter1_adv = ADVANCEMENT_FOR_RUN
            new_batter2_adv += self.second_batter_speed_.sample()
            if new_batter2_adv > ADVANCEMENT_FOR_RUN:
                new_batter2_adv = ADVANCEMENT_FOR_RUN
            if new_batter1_adv == ADVANCEMENT_FOR_RUN and new_batter2_adv == ADVANCEMENT_FOR_RUN: 
                # Resets the advancement.  The batters will be able to go for another run afterwards
                new_batter1_adv = 0
                new_batter2_adv = 0
                new_nb_runs += 1
                if new_nb_runs > MAX_NB_RUNS: # they ran for nothing
                    new_nb_runs = MAX_NB_RUNS

        new_ball_distance: int = state.ball_distance_ - self.ball_speed_.sample()

        reward = 0
        if new_ball_distance <= 0: # end of the delivery (will reset the state)
            if new_batter1_adv > 0 or new_batter2_adv > 0: # dismissal!
                reward = REWARD_FOR_LOSING
            else: # otherwise, points are scored
                reward = new_nb_runs
            new_nb_runs = 0
            new_ball_distance = 0
            new_batter1_adv = 0
            new_batter2_adv = 0

        new_state = CricketState(nb_runs_=new_nb_runs,batter1_adv_=new_batter1_adv,batter2_adv_=new_batter2_adv,ball_distance_=new_ball_distance)
        self.current_state_ = new_state
        return TransitionOutcome(state=new_state,reward=reward)
    
    def states(self) -> List[State]:
        return [
            CricketState(nb_runs_=r, batter1_adv_=b1, batter2_adv_=b2, ball_distance_=b)
            for r in range(MAX_NB_RUNS+1) for b1 in range(ADVANCEMENT_FOR_RUN+1) for b2 in range(ADVANCEMENT_FOR_RUN+1) for b in range(MAX_BALL_DISTANCE+1)
        ]

    def current_state(self) -> State:
        return self.current_state_

def cricket_team_1() -> CricketDomain:
    return CricketDomain(
        first_batter_speed=DiscreteDistribution([(1,0.5),(2,.5)])
        , second_batter_speed=DiscreteDistribution([(1,0.5),(2,.5)])
        , ball_speed=DiscreteDistribution([(1,.7),(2,.3)])
        , batting_strength=DiscreteDistribution([(12,.1),(13,.4),(14,.4),(15,.1)])
    )

def cricket_team_2() -> CricketDomain:
    return CricketDomain(
        first_batter_speed=DiscreteDistribution([(1,0.5),(2,.5)])
        , second_batter_speed=DiscreteDistribution([(1,0.5),(2,.5)])
        , ball_speed=DiscreteDistribution([(1,.6),(2,.3),(3,.1)])
        , batting_strength=DiscreteDistribution([(12,.1),(13,.4),(14,.4),(15,.1)])
    )

def cricket_team_3() -> CricketDomain:
    return CricketDomain(
        first_batter_speed=DiscreteDistribution([(1,1)])
        , second_batter_speed=DiscreteDistribution([(1,1)])
        , ball_speed=DiscreteDistribution([(1,1)])
        , batting_strength=DiscreteDistribution([(12,1)])
    )

# eof
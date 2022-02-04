from dataclasses import dataclass
from enum import Enum
from typing import List

from domain import Action, State, RLEnvironment, DiscreteDistribution, TransitionOutcome

'''
  An extension to the CricketGame in which cheating is possible.
  Explanations about most variables are in cricket.py
'''

MAX_NB_RUNS = 5
MAX_BALL_DISTANCE = 20
ADVANCEMENT_FOR_RUN = 5

REWARD_FOR_LOSING = -10
REWARD_FOR_CHEATING = -100

@dataclass(unsafe_hash=True)
class CheatingCricketState(State):
    '''
      The state of a cricket game.  Should be immutable.
      No notion of tiredness here.
    '''
    nb_runs_: int
    ball_distance_: int
    batter1_adv_: int
    batter2_adv_: int
    cheats_: bool # true if cheating during this delivery
    scoring_: bool # true after the ball came back to the wicket but before scoring (hiding must be performed now)


class CheatingCricketAction(Enum):
    STOP = 0
    RUN = 1
    BACKOFF = 2
    CHEAT = 3
    DO_NOT_CHEAT = 4
    HIDE = 5
    DO_NOT_HIDE = 6


class CheatingCricketDomain(RLEnvironment):
    first_batter_speed_: DiscreteDistribution[int]
    second_batter_speed_: DiscreteDistribution[int]
    ball_speed_: DiscreteDistribution[int]
    batting_strength_: DiscreteDistribution[int]
    initial_state_: CheatingCricketState

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
        self.initial_state_ = CheatingCricketState(nb_runs_=0, ball_distance_=0, 
          batter1_adv_=0, batter2_adv_=0, cheats_ = False, scoring_ = False)
        self.reset()

    def reset(self):
        self.current_state_ = self.initial_state_

    def applicable_actions(self) -> List[Action]:
        if self.current_state_ == self.initial_state_:
            # must decide if going to cheat
            return [CheatingCricketAction.CHEAT, CheatingCricketAction.DO_NOT_CHEAT]
        if self.current_state_.scoring_:
            # must decide if going to hide
            return [CheatingCricketAction.HIDE, CheatingCricketAction.DO_NOT_HIDE]
        return [CheatingCricketAction.STOP, CheatingCricketAction.RUN, CheatingCricketAction.BACKOFF]

    def execute(self, action: Action) -> TransitionOutcome:
        state = self.current_state_
        if state == self.initial_state_:
            # Throwing the ball
            cheats = (action == CheatingCricketAction.CHEAT)
            next_state = CheatingCricketState(nb_runs_=0, batter1_adv_=0, batter2_adv_=0, 
                ball_distance_=self.batting_strength_.sample(), cheats_=cheats, scoring_=False)
            self.current_state_ = next_state
            return TransitionOutcome(state=next_state,reward=0)

        if state.scoring_:
            reward: int
            if state.cheats_ and action != CheatingCricketAction.HIDE:
                reward = REWARD_FOR_CHEATING # Huge penalty
            elif state.batter1_adv_ == 0 and state.batter2_adv_ == 0:
                if state.cheats_:
                    reward = state.nb_runs_ * 2 # successful cheat
                else:
                    reward = state.nb_runs_
            else:
                reward = REWARD_FOR_LOSING
            self.current_state_ = self.initial_state_
            return TransitionOutcome(state=self.initial_state_, reward=reward)

        new_nb_runs = state.nb_runs_
        new_batter1_adv: int = state.batter1_adv_
        new_batter2_adv: int = state.batter2_adv_
        if action == CheatingCricketAction.BACKOFF:
            if new_batter1_adv > 0:
                new_batter1_adv -= 1
            if new_batter2_adv > 0:
                new_batter2_adv -= 1
        if action == CheatingCricketAction.RUN:
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
        scoring = (new_ball_distance <= 0)

        new_state = CheatingCricketState(nb_runs_=new_nb_runs,batter1_adv_=new_batter1_adv,
            batter2_adv_=new_batter2_adv,ball_distance_=new_ball_distance,
            cheats_=state.cheats_,scoring_=scoring)
        self.current_state_ = new_state
        return TransitionOutcome(state=new_state,reward=0)
    
    def states(self) -> List[State]:
        return [
            CheatingCricketState(nb_runs_=r, batter1_adv_=b1, batter2_adv_=b2, ball_distance_=b,cheats_=c,scoring_=s)
            for r in range(MAX_NB_RUNS+1) 
            for b1 in range(ADVANCEMENT_FOR_RUN+1) for b2 in range(ADVANCEMENT_FOR_RUN+1) 
            for b in range(MAX_BALL_DISTANCE+1)
            for c in [True,False] for s in [True,False] if (not s or b == 0) # cannot score if b != 0
        ]

    def current_state(self) -> State:
        return self.current_state_

def cheating_cricket_team_1() -> CheatingCricketDomain:
    return CheatingCricketDomain(
        first_batter_speed=DiscreteDistribution([(1,0.5),(2,.5)])
        , second_batter_speed=DiscreteDistribution([(1,0.5),(2,.5)])
        , ball_speed=DiscreteDistribution([(1,.7),(2,.3)])
        , batting_strength=DiscreteDistribution([(12,.1),(13,.4),(14,.4),(15,.1)])
    )

def cheating_cricket_team_2() -> CheatingCricketDomain:
    return CheatingCricketDomain(
        first_batter_speed=DiscreteDistribution([(1,0.5),(2,.5)])
        , second_batter_speed=DiscreteDistribution([(1,0.5),(2,.5)])
        , ball_speed=DiscreteDistribution([(1,.6),(2,.3),(3,.1)])
        , batting_strength=DiscreteDistribution([(12,.1),(13,.4),(14,.4),(15,.1)])
    )

def cheating_cricket_team_3() -> CheatingCricketDomain:
    return CheatingCricketDomain(
        first_batter_speed=DiscreteDistribution([(1,1)])
        , second_batter_speed=DiscreteDistribution([(1,1)])
        , ball_speed=DiscreteDistribution([(1,1)])
        , batting_strength=DiscreteDistribution([(12,1)])
    )

# eof

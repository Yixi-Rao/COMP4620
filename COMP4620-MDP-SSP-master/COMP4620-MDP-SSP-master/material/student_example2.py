from enum import Enum
from typing import NamedTuple, Optional, List, Tuple
from interface import Assignment1Domain, State, Action
from skdecide import DiscreteDistribution, TransitionValue
from skdecide.hub.space.gym import ListSpace

from vi import ValueIteration

max_queue: int = 6
tau_1: float = .3
tau_2: float = .2
prob_orange_pass = .5

class TrafficLightAction(Enum): 
    '''
      The list of applicable actions.
    '''
    SWITCH = 0
    DO_NOT_SWITCH = 1

class SingleLightState(Enum): 
    '''
      The list of possible states of a single light.  
      The next 6 states match the first element of each state in Figure 1.
    '''
    GREEN = 0, 
    GREEN_SWITCH_INITIATED = 1,
    EARLY_ORANGE = 2, 
    LATE_ORANGE = 3,
    RECENT_RED = 4,
    RED = 5, 

    def next_state(self, other, act) :
        '''
          Computes the next Single Light State
          given the current Single Light State (self)
          and the specified action.
          This method returns one Single Light State, and not a distribution 
          because the next Single Light State is deterministically determined.
        '''
        if self == SingleLightState.GREEN: 
            if act == TrafficLightAction.DO_NOT_SWITCH:
                return SingleLightState.GREEN
            return SingleLightState.GREEN_SWITCH_INITIATED

        if self == SingleLightState.GREEN_SWITCH_INITIATED: 
            return SingleLightState.EARLY_ORANGE

        if self == SingleLightState.EARLY_ORANGE:
            return SingleLightState.LATE_ORANGE

        if self == SingleLightState.LATE_ORANGE:
            return SingleLightState.RECENT_RED

        if self == SingleLightState.RECENT_RED: 
            return SingleLightState.RED

        # At this point, the state is RED.  It becomes GREEN iff other is RECENT_RED
        if other == SingleLightState.RECENT_RED:
            return SingleLightState.GREEN
        return SingleLightState.RED

    def next_cars_queueing(self, current_cars: int, tau: float) -> List[Tuple[int, float]]:
        '''
          Computes the number of cars queueing in the next state 
          given 1) that self is the next Single Light State
          2) the specified number of cars currently waiting, 
          and 3) the rate of cars coming.
          The outcome is a list of numbers and their probability distribution.
          For instance, if the light is red, the number of cars is 2, and tau is .3, 
          the outcome of this method will be: 
            [(3,.3), (2,.7)]
          because there is 30% chance that the number of vehicles will increase by 1
          and 70% chance that this number will not increase.
        '''
        if current_cars == 0 and (self == SingleLightState.GREEN or self == SingleLightState.GREEN_SWITCH_INITIATED or self == SingleLightState.EARLY_ORANGE):
            return [(0,1)]

        if self == SingleLightState.GREEN or self == SingleLightState.GREEN_SWITCH_INITIATED or self == SingleLightState.EARLY_ORANGE:
            # one car passes, a new one arrives with probability tau
            return [(current_cars-1, 1-tau), (current_cars, tau)]

        if self == SingleLightState.RED or self == SingleLightState.RECENT_RED:
            # increases by one if possible with probability tau
            if current_cars == max_queue:
                return [(max_queue, 1)]
            return [(current_cars, 1-tau), (current_cars+1, tau)]

        # at this point, self == SingleLightState.LATE_ORANGE:

        if current_cars == 0:
            prob_plus_one = tau * (1 - prob_orange_pass)
            return [ (0, 1 - prob_plus_one), (1, prob_plus_one)]

        if current_cars == max_queue:
            prob_minus_1 = prob_orange_pass * (1-tau)
            return [
                (current_cars-1, prob_minus_1),
                (current_cars, 1 - prob_minus_1),
            ]

        prob_minus_1 = prob_orange_pass * (1-tau)
        prob_plus_1 = (1-prob_orange_pass) * tau
        prob_stays = 1 - prob_minus_1 - prob_plus_1
        return [
            (current_cars-1, prob_minus_1),
            (current_cars+1, prob_plus_1),
            (current_cars,   prob_stays),
        ]
    

class TrafficLightState(NamedTuple):
    '''
      A state of the MDP, defined as the states of the two lights 
      and the number of vehicles queueing on each direction.
    '''
    cars_queueing_north: int
    cars_queueing_east: int
    north_light: SingleLightState
    east_light: SingleLightState

    def __eq__(self, other): 
        if self.cars_queueing_north != other.cars_queueing_north:
            return False
        if self.cars_queueing_east != other.cars_queueing_east:
            return False
        if self.north_light != other.north_light:
            return False
        if self.east_light != other.east_light:
            return False
        return True

class TrafficLightDomain(Assignment1Domain):
    '''
      The MDP
    '''
    _states: List[TrafficLightState]

    def __init__(self):
        self._states = None # The set of states is computed the first time _get_observation_space_ is called

    def  _get_transition_value(self, state: TrafficLightState, action: TrafficLightAction, next_state: Optional[TrafficLightState] = None) -> TransitionValue:
        '''
          Returns the value of the transition
        '''
        # DONE
        if next_state is not None:
            return TransitionValue(cost=next_state.cars_queueing_east+state.cars_queueing_north,
                                   reward=-(next_state.cars_queueing_east+state.cars_queueing_north))
        else:
            return TransitionValue(cost=0)

    def _get_next_state_distribution(self, state: TrafficLightState, action: TrafficLightAction) -> DiscreteDistribution[TrafficLightState]:
        '''
          Returns the list of states 
          that applying the specified action in the specified state can lead to, 
          together with their respective probabilities.
        '''
        # TODO
        ans = []

        tau_north = tau_1
        tau_east = tau_2

        east_light = state.east_light.next_state(state.north_light,action)
        north_light = state.north_light.next_state(state.east_light,action)

        north_distribution = state.north_light.next_cars_queueing(state.cars_queueing_north,tau_north)
        east_distribution = state.east_light.next_cars_queueing(state.cars_queueing_east,tau_east)

        for (north_int, prob_north) in north_distribution:
            for (east_int, prob_east) in east_distribution:
                traffic_light_state = TrafficLightState(north_int,east_int,north_light,east_light)
                traffic_light_state_prob = prob_north*prob_east
                ans.append((traffic_light_state,traffic_light_state_prob))
                if north_int == 3 and east_int == 2:
                    print(prob_north)
                    print(prob_east)
        return DiscreteDistribution(ans)
    
    def _is_terminal(self, state: TrafficLightState) -> bool:
        '''
        No terminal state.
        '''
        return False
    
    def _get_applicable_actions_from(self, state: TrafficLightState) -> ListSpace[TrafficLightAction]:
        '''
          Returns the list of actions applicable in the specified state.
        '''
        # DONE
        result = []
        north_light = state.north_light
        east_light = state.east_light
        if north_light == SingleLightState.RED and east_light == SingleLightState.GREEN:
            result.append(TrafficLightAction.DO_NOT_SWITCH)
            result.append(TrafficLightAction.SWITCH)
        elif north_light == SingleLightState.GREEN and east_light == SingleLightState.RED:
            result.append(TrafficLightAction.DO_NOT_SWITCH)
            result.append(TrafficLightAction.SWITCH)
        else:
            result.append(TrafficLightAction.DO_NOT_SWITCH)
        return ListSpace(result)
    
    def _get_action_space_(self) -> ListSpace[TrafficLightAction]:
        '''
          Returns the list of actions.
        '''
        return ListSpace([TrafficLightAction.SWITCH , TrafficLightAction.DO_NOT_SWITCH])
    
    def _get_initial_state_(self) -> State:
        '''
          Returns the initial state
        '''
        return TrafficLightState(cars_queueing_north=0, \
            cars_queueing_east=0, \
            north_light=SingleLightState.GREEN, \
            east_light=SingleLightState.RED
        )
    
    def _get_observation_space_(self) -> ListSpace[TrafficLightState]:
        '''
          Returns the list of states.  
          It can be a superset.
        '''
        if self._states == None:
            # TODO
            self._states = [
            ]

        return ListSpace(self._states)

if __name__ == '__main__':
    tl = TrafficLightDomain()

    vi = ValueIteration(tl, max_value = 1000, gamma = 0.9, initial_value=0)
    vi.backup()
    interesting_state = TrafficLightState(cars_queueing_north=2, \
            cars_queueing_east=3, \
            north_light=SingleLightState.GREEN, \
            east_light=SingleLightState.RED
        )
    action = vi.policy()[interesting_state]
    print("Action in initial state: {}".format(action))


'''
  QUESTIONS: 

* Explain the optimal action in the interesting state of the __main__ as calculated by VI.

* In some countries, the traffic lights are optimised in order to reduce the number of times cars cross the light when it is orange.  Explain how you would modify the model to mimic this behaviour.
'''

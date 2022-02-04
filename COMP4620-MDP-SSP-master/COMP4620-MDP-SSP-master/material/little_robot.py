# This models the little robot problem
from enum import Enum
from typing import NamedTuple, Optional, Dict, List, Dict, Set, Tuple
from interface import Assignment1Domain, State, Action
from skdecide.hub.space.gym import ListSpace
from skdecide import DiscreteDistribution, TransitionValue

from value import ValueFunction

class GridState(State):
    _x: int
    _y: int

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    def __eq__(self, other):
        if other == None: return False
        return self._x == other._x and self._y == other._y

    def __hash__(self):
        sum = self._y + self._x
        m = int((sum * (sum + 1)) / 2)
        return m + self._y

    def __repr__(self):
        return "({},{})".format(self._x,self._y)

class StateDelta():
    _dx: int
    _dy: int

    def __init__(self, dx: int, dy: int):
        self._dx = dx
        self._dy = dy
        
    def dx(self): 
        return self._dx

    def dy(self): 
        return self._dy


class GridAction(Action):
    _cost: float
    _deltas: List[Tuple[StateDelta,float]]
    _name: str

    def __init__(self, cost: float, deltas: List[Tuple[StateDelta,float]], name: str):
        self._cost = cost
        self._deltas = deltas
        self._name = name

    def __repr__(self):
        return self._name


class GridDomain(Assignment1Domain):
    _minX: int # inclusive
    _maxX: int # inclusive
    _minY: int # inclusive
    _maxY: int # inclusive
    _init: GridState

    _actions: List[GridAction]

    _stay_actions: Set[GridAction]
    _terminals: Dict[GridState, GridAction]
    
    _obstacles: Set[GridState]

    def __init__(self
    , minX: Optional[int] = 0, maxX: Optional[int] = 4
    , minY: Optional[int] = 0, maxY: Optional[int] = 4 
    , init: Optional[GridState] = GridState(0,2)
    , actions: Optional[List[GridAction]] = []
    , terminals: Optional[Dict[GridState,float]] = {}
    , obstacles: Optional[List[GridState]] = []
    ):
        self._minX = minX
        self._maxX = maxX
        self._minY = minY
        self._maxY = maxY
        self._init = init
        self._actions = actions
        self._terminals = terminals
        self._stay_actions = set()
        for state in terminals:
            cost = terminals[state]
            gaction = GridAction(cost, [(StateDelta(0,0),1)], "stay_" + state.__repr__())
            self._stay_actions.add(gaction)
            self._terminals[state] = gaction
        self._obstacles = set(obstacles)



    def next_state(self, state: GridState, delta: StateDelta):
        new_state = GridState(state._x + delta.dx() , state._y + delta.dy() )
        if new_state._x < self._minX: return None
        if new_state._y < self._minY: return None
        if new_state._x > self._maxX: return None
        if new_state._y > self._maxY: return None
        if new_state in self._obstacles: return None
        return new_state

    def action(self, name: str) -> GridAction:
        action: GridAction
        for action in self._actions:
            if action._name == name:
                return action


    def _get_transition_value(self, state: GridState, action: GridAction, next_state: Optional[GridState] = None) -> TransitionValue:
        return TransitionValue(cost=action._cost)
    
    def _get_next_state_distribution(self, state: GridState, action: GridAction) -> DiscreteDistribution[State]:
        unnormalised = [ (self.next_state(state, delta), prob) for (delta,prob) in action._deltas ]
        factor = sum( [ prob for (next_state,prob) in unnormalised if next_state != None] )
        if factor == 0:
            raise ValueError("Action {} not applicable in state {}".format(action, state))
        result = DiscreteDistribution(
            [ (next_state, prob / factor) for (next_state, prob) in unnormalised if next_state != None ]
        )
        return result
    
    def _is_terminal(self, state: GridState) -> bool:
        return state in self._terminals
    
    def _get_applicable_actions_from(self, state: GridState) -> ListSpace[GridAction]:
        actions = [
            action for action in self._actions if 
            any( self.next_state(state, delta) != None for (delta,_prob) in action._deltas)
        ]
        if state in self._terminals:
            actions.append(self._terminals[state])
        return ListSpace(actions)

    def _get_action_space_(self) -> ListSpace[Action]:
        actions = self._actions.copy()
        for action in self._stay_actions:
            actions.append(action)
        return ListSpace(actions)
    
    def _get_initial_state_(self) -> State:
        return self._init
    
    def _get_observation_space_(self) -> ListSpace[State]:
        return ListSpace(
            [
                GridState(x,y) for x in range(self._minX, self._maxX+1)
                for y in range(self._minY, self._maxY+1)
                if GridState(x,y) not in self._obstacles
            ]
        )

    def string_row(self, vi: ValueFunction
        , y: int
        , digits1: int = 2
        , digits2: int = 5
        , action_space: int = 0
    ) -> str:
        result: str = "|"
        for x in range(self._minX,self._maxX+1): 
            state = GridState(x,y)
#            print(state)
            if state not in self._obstacles:
                val = vi.value(GridState(x,y))
                val_string = ("{:" + str(digits1) + "." + str(digits2) + "f}").format(val)
            else:
                val_string = " " * (digits1 + digits2)
            val_string = val_string + " " * (action_space +1)
            result = result + " " + val_string + " |"
        return result


    def print_table_complete(self, vi: ValueFunction
        , digits1: int = 2
        , digits2: int = 8
        , action_space: int = 0
    ) -> None:
        sepline = "+"
        for _x in range(self._minX,self._maxX+1):
            sepline = sepline + ("-" * (3+digits1+digits2)) + \
                ( "" if (action_space == 0) else "-" * (1+action_space) ) + \
                "+"
        print(sepline)
        for y in range(self._maxY,self._minY-1,-1):
            print(self.string_row(vi, y, digits1=digits1, digits2=digits2, action_space=action_space))
            print(sepline)
        
def default_robot() -> GridDomain:
    up: GridAction = GridAction(1, [(StateDelta(0,1),1)], "up")
    down: GridAction = GridAction(1, [(StateDelta(0,-1),1)], "down")
    left: GridAction = GridAction(1, [(StateDelta(-1,0),1)], "left")
    #right_lean: GridAction = GridAction(1, [(StateDelta(1,0),.5) , (StateDelta(1,-1),.45), (StateDelta(-1,0),.05)], "right")
    right_lean: GridAction = GridAction(1, [(StateDelta(1,0),.5) , (StateDelta(1,-1),.5)], "right")
    little_robot = GridDomain(minX=0, maxX=4, minY = 0, maxY = 4, init=GridState(x=0,y=2), 
      actions=[ up, down, left, right_lean ], 
      terminals = {GridState(4,2): 0},
      obstacles = [GridState(2,2)]
    )
    return little_robot


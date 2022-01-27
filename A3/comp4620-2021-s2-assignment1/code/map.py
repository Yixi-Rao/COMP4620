import random
from typing import Dict, List, Tuple, Optional, Set
from MDP import Action, MDP, State


class MonsterType:
    def __init__(self, name: str, st: float, ma: float):
        self.name_ = name
        self.st_   = st
        self.ma_   = ma

    def __repr__(self):
        return self.name_

    def strength(self):
        return self.st_

    def magic(self):
        return self.ma_


class AdventurerType:
    def __init__(self, name, st: float, ma: float):
        self.name_ = name
        self.st_   = st
        self.ma_   = ma

    def __repr__(self):
        return self.name_

    def __hash__(self):
        # Assumes that there cannot be two different types with the same name
        return self.name_.__hash__()

    def __eq__(self, other):
        if not type(self) == type(other):
            return False
        return self.name_ == other.name_

    def strength(self):
        return self.st_

    def magic(self):
        return self.ma_

#NOTE monster and adventurer flight together
def probability_of_dying(m: MonsterType, a: AdventurerType) -> float:
    return min(1, max(0, m.strength() - a.strength()) + max(0, m.magic() - a.magic()))

#NOTE Map has dictionries of dangerous locations, dictionries of  inns, dictionries of  chest rooms and neighbours
class Map:
    def __init__(self):
        self.starting_location_   = None
        # three types of location
        self.dangerous_locations_ = {}
        self.inns_                = {}
        self.chest_rooms_         = {}
        # neighbours
        self.neighbours_          = {}

    def create_dangerous_location(self, name: str, monster: MonsterType):
        self.dangerous_locations_[name] = monster
        self.neighbours_[name] = set()

    def create_inn(self, name: str, for_hire: List[Tuple[int, AdventurerType]]):
        self.inns_[name] = for_hire
        self.neighbours_[name] = set()

    def create_chest_room(self, name: str, reward: int):
        self.chest_rooms_[name] = reward
        self.neighbours_[name] = set()

    def is_inn(self, locname: str) -> bool:
        return locname in self.inns_

    def for_hire(self, locname: str) -> List[Tuple[int, AdventurerType]]:
        return self.inns_[locname]

    def add_path(self, locname1, locname2):
        '''
          Adds a path between the two specified locations.
        '''
        self.neighbours_[locname1].add(locname2)
        self.neighbours_[locname2].add(locname1)

    def set_initial_location(self, locname: str) -> None:
        self.starting_location_ = locname

    def get_initial_location(self) -> str:
        return self.starting_location_

    def locations(self) -> Set[str]:
        return self.neighbours_.keys()

#NOTE all the adventurer information and cost. look up table
def collect_adventurer_types(map: Map) -> Set[Tuple[int, AdventurerType]]:
    result = set()
    for loc, offer in map.inns_.items():
        for cost, type in offer:
            result.add((cost, type))
    return result


PARTY_MAX_SIZE = 2

#NOTE party is list of adventurers
class Party:
    def __init__(self, party: Optional = None, add: Optional = None, rem: Optional = None):
        # first compute the adventurers as a list, then convert into a tuple
        # this is required to use hashcode functions
        advs = []
        if not party is None:
            for ad in party.adventurers_:
                advs.append(ad)
        if not add is None:
            advs.append(add)
        if not rem is None:
            del advs[rem]
        self.adventurers_ = tuple(advs)

    def __eq__(self, party) -> bool:
        return self.adventurers_ == party.adventurers_

    def __repr__(self) -> str:
        return str(self.adventurers_)

    def __hash__(self):
        return self.adventurers_.__hash__()

    def empty_party(self):
        return len(self.adventurers_) == 0

    def full(self):
        return self.size() == PARTY_MAX_SIZE

    def size(self):
        return len(self.adventurers_)

    def adventurer(self, i):
        return self.adventurers_[i]

#NOTE define the specific dungeon state: party, current_location, visited_places
class DungeonState(State):
    def __init__(self, 
                 state   : Optional      = None,
                 location: Optional[str] = None,
                 add     : Optional      = None,
                 rem     : Optional      = None
                 ):
        
        self.party_    = Party()  if state    is None     else Party(state.party_, add=add, rem=rem)
        self.location_ = location if location is not None else (state.location_ if state is not None else None)
        visited        = set()    if state    is None     else set(state.visited_places_)
        if not location is None:
            visited.add(location)
        self.visited_places_ = frozenset(visited)

    def __eq__(self, state) -> bool:
        if not self.party_ == state.party_:
            return False
        if not self.location_ == state.location_:
            return False
        if not self.visited_places_ == state.visited_places_:
            return False
        return True

    def __repr__(self) -> str:
        return f'<{self.party_},{self.location_},{self.visited_places_}>'

    def __hash__(self):
        v1 = self.party_.__hash__()
        v2 = self.location_.__hash__()
        v3 = self.visited_places_.__hash__()
        return v1 + v2 + v3
        # return self.party_.__hash__() + self.location_.__hash__() + self.visited_places_.__hash__()

#NOTE define the specific dungeon state 
class DungeonAction(Action):
    def next_states(self, state: DungeonState, map: Map) -> List[Tuple[DungeonState, float, float]]:
        pass


class HireAction(DungeonAction):
    def __init__(self, adventurer_type, price):
        self.adventurer_type_ = adventurer_type
        self.price_ = price

    def __repr__(self) -> str:
        return f'Hire {self.adventurer_type_.name_} for {self.price_}'

    def __hash__(self) -> int:
        return self.adventurer_type_.__hash__() + self.price_

    def __eq__(self, act) -> bool:
        if not type(self) == type(act):
            return False
        return (self.adventurer_type_ == act.adventurer_type_) and (self.price_ == act.price_)

    def next_states(self, state: DungeonState, map: Map) -> List[Tuple[DungeonState, float, float]]:
        new_state = DungeonState(state=state, add=self.adventurer_type_)
        return [(new_state, 1.0, -self.price_)]


class MoveAction(DungeonAction):
    def __init__(self, locname, index: int):
        self.locname_ = locname
        self.index_ = index

    def __eq__(self, act):
        if not type(self) == type(act):
            return False
        return self.locname_ == act.locname_ and self.index_ == act.index_

    def __repr__(self) -> str:
        return f'Move {self.locname_} {self.index_}'

    def __hash__(self):
        return self.locname_.__hash__() + self.index_

    def next_states(self, state: DungeonState, map: Map) -> List[Tuple[DungeonState, float, float]]:
        # if the new place is already visited, just move
        if self.locname_ in state.visited_places_:
            new_state = DungeonState(state=state, location=self.locname_)
            prob      = 1.0
            reward    = 0
            return [(new_state, prob, reward)]

        # if the new place is not dangerous, just move and collect the reward if any
        if not (self.locname_ in map.dangerous_locations_):
            new_state = DungeonState(state=state, location=self.locname_)
            prob      = 1.0
            reward    = 0 if not self.locname_ in map.chest_rooms_ else map.chest_rooms_[self.locname_]
            return [(new_state, prob, reward)]

        # visiting a dangerous location
        dying_prob    = probability_of_dying(map.dangerous_locations_[self.locname_], state.party_.adventurer(self.index_))
        success_state = DungeonState(state=state, location=self.locname_)
        fail_state    = DungeonState(state=state, rem=self.index_)
        # fail_state.remove_adventurer(self.index_)

        result = []
        if dying_prob > 0:
            result.append((fail_state, dying_prob, 0))
        if dying_prob < 1:
            result.append((success_state, 1-dying_prob, 0))
        return result


class NoAction(DungeonAction):
    def __eq__(self, act):
        if not type(self) == type(act):
            return False
        return True

    def __repr__(self) -> str:
        return 'No Action'

    def __hash__(self):
        return self.__repr__().__hash__()

    def next_states(self, state: DungeonState, map: Map) -> List[Tuple[DungeonState, float, float]]:
        return [(state, 1.0, 0)]

#NOTE all reachable states from the start states
def reachable_states(mdp: MDP, start: Optional[State] = None) -> List[State]:
    result = set()
    open = set()

    if start is None:
        start = mdp.initial_state()
    result.add(start)
    open.add(start)

    while open:
        state = open.pop()
        for act in mdp.applicable_actions(state):
            for next_state, prob, rew in mdp.next_states(state, act):
                if next_state in result:
                    continue
                result.add(next_state)
                open.add(next_state)

    return list(result)

#NOTE Dungeon MDP (map and reachable_states=connect states)
class DungeonMDP(MDP):
    def __init__(self, map: Map):
        self.map_ = map
        self.reachable_states_ = None

    def states(self) -> List[State]:
        if self.reachable_states_ == None:
            self.reachable_states_ = reachable_states(self)
        return self.reachable_states_

    def actions(self) -> List[Action]:
        result = [NoAction()]
        
        for i in range(PARTY_MAX_SIZE):
            for loc in self.map_.locations():
                act = MoveAction(loc, i)
                result.append(act)
                
        for cost, type in collect_adventurer_types(self.map_):
            act = HireAction(type, cost)
            result.append(act)
            
        return result

    def applicable_actions(self, s: State) -> List[Action]:
        result  = [NoAction()]
        locname = s.location_
        party   = s.party_

        # hire a companion
        if self.map_.is_inn(locname) and not party.full():
            for price, adtype in self.map_.for_hire(locname):
                act = HireAction(adtype, price)
                result.append(act)

        # move to a new location
        for index in range(party.size()):
            for loc in self.map_.neighbours_[locname]:
                act = MoveAction(loc, index)
                result.append(act)

        # can also move to visited room if there is noone in the party
        if party.empty_party():
            for loc in self.map_.neighbours_[locname]:
                if loc in s.visited_places_:
                    act = MoveAction(loc, 0)
                    result.append(act)

        return result

    def next_states(self, s: State, a: Action) -> List[Tuple[State, float, float]]:
        return a.next_states(s, self.map_)

    def initial_state(self) -> DungeonState:
        return DungeonState(location=self.map_.get_initial_location())

# end of class


def basic_map() -> Map:
    # adventurers
    peon    = AdventurerType('peon', st=0, ma=0)
    wizard  = AdventurerType('wizard', st=.1, ma=1.0)
    soldier = AdventurerType('soldier', st=.5, ma=.0)
    # monsters
    goblin   = MonsterType('goblin', st=.3, ma=.0)
    fimir    = MonsterType('fimir', st=.7, ma=.1)
    sorcerer = MonsterType('sorcerer', st=.2, ma=1.4)
    # map
    map = Map()
    map.create_inn('start', for_hire=[(10, peon), (100, soldier)])
    map.set_initial_location('start')
    map.create_inn('market', for_hire=[(8, peon), (50, soldier), (100, wizard)])
    map.create_dangerous_location('room1', fimir)
    map.create_dangerous_location('room2', goblin)
    map.create_dangerous_location('room3', sorcerer)
    map.create_dangerous_location('room4', goblin)
    map.create_chest_room('smallchest', 30)
    map.create_chest_room('largechest', 500)
    map.add_path('start', 'room1')
    map.add_path('start', 'room2')
    map.add_path('start', 'room4')
    map.add_path('market', 'room2')
    map.add_path('room1', 'room2')
    map.add_path('room1', 'room3')
    map.add_path('room1', 'room4')
    map.add_path('room3', 'largechest')
    map.add_path('room4', 'smallchest')

    return map

def basic_map2() -> Map:
    # adventurers
    peon    = AdventurerType('peon', st=0, ma=0)
    soldier = AdventurerType('soldier', st=.5, ma=.0)
    # monsters
    goblin   = MonsterType('goblin', st=.3, ma=.0)
    fimir    = MonsterType('fimir', st=.7, ma=.1)
    # map
    map = Map()
    map.create_inn('start', for_hire=[(10, peon), (100, soldier)])
    map.set_initial_location('start')
    map.create_dangerous_location('room1', fimir)
    map.create_dangerous_location('room2', goblin)

    map.add_path('start', 'room1')
    map.add_path('start', 'room2')

    map.add_path('room1', 'room2')

    return map


if __name__ == "__main__":

    map = basic_map()
    mdp = DungeonMDP(map)

    import statemachine

    smmdp, statedict, actiondict = statemachine.state_machine_from_mdp(mdp)
    reverse_statedict = {}
    for smstate, state in statedict.items():
        reverse_statedict[state] = smstate

    from algos import value_iteration
    smpol, svalue = value_iteration(smmdp, .99, .01)

    print('--')

    from algos import simulate
    pol = statemachine.TranslatedPolicy(smpol, reverse_statedict, actiondict)
    h = simulate(mdp, pol, 20)
    print(h)

# eof

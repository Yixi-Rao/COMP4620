import map
import modelling
import statemachine
from algos import value_iteration
from algos import simulate
import traceback


def probability_of_dying(m: map.MonsterType, a: map.AdventurerType) -> float:
    print("m strength ", m.strength())
    print("a strength ", a.strength())
    print("m magic ", m.magic())
    print("a magic ", a.magic())
    print(max(0, m.strength() - a.strength()))
    print(max(0, m.magic() - a.magic()))
    return min(1, max(0, m.strength() - a.strength()) + max(0, m.magic() - a.magic()))
m       = map.basic_map()
print(probability_of_dying(m.dangerous_locations_['room1'], m.for_hire('start')[0][1]))
# mdp     = map.DungeonMDP(m)
# new_mdp = modelling.forbid_two_actions(mdp, map.MoveAction(locname='room1',index=0))

# smmdp, statedict, actiondict = statemachine.state_machine_from_mdp(new_mdp)
# reverse_statedict = {}
# for smstate, state in statedict.items():
#     reverse_statedict[state] = smstate
    
# print('--')

# smpol, svalue = value_iteration(smmdp, .99, .01)
# pol = statemachine.TranslatedPolicy(smpol, reverse_statedict, actiondict)

# h = simulate(new_mdp, pol, 50)
# for line in h.pretty_repr():
#     print(line)




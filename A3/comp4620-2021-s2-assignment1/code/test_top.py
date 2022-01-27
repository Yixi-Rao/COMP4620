
from statemachine import SMMDP, SMTransition
from connectedcomp import compute_connected_components
from connectedcomp import CCGraph, ConnectedComponent

smmdp = SMMDP([
              SMTransition('1', 'a1', [['2', 1, 3]]),
              SMTransition('2', 'a1', [['3', .5, 5], ['4', .5, 10]]),
              SMTransition('2', 'a2', [['3', 1, 2]]),
              SMTransition('3', 'a1', [['1', .5, 5], ['6', .5, 8]]),
              SMTransition('3', 'a2', [['1', .9, 10], ['7', .1, 0]]),
              SMTransition('4', 'a1', [['5', 1, 1]]),
              SMTransition('4', 'a2', [['5', .9, 10], ['7', .05, 0], ['8', .05, 0]]),
              SMTransition('5', 'a1', [['6', 1, 1]]),
              SMTransition('6', 'a1', [['4', 1, 1]]),
              SMTransition('7', 'a1', [['8', 1, 0]]),
              SMTransition('8', 'a1', [['7', 1, 1]]),
              ], '1'
              )

compute_connected_components(smmdp)
# graph = CCGraph()
# scc3 = ConnectedComponent([smmdp.get_state('7'), smmdp.get_state('8')], set())
# scc2 = ConnectedComponent([smmdp.get_state('4'), smmdp.get_state('5'), smmdp.get_state('6')], {scc3})
# scc1 = ConnectedComponent([smmdp.get_state('1'), smmdp.get_state('2'), smmdp.get_state('3')], {scc2})
# graph.add_connected_component(scc1)
# print(graph.roots())
# graph.add_connected_component(scc2)
# print(graph.roots())
# graph.add_connected_component(scc3)
# print(graph.roots())
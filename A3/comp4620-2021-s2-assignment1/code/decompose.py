from map import basic_map, DungeonMDP
from connectedcomp import compute_reachables, create_cc_graph

if __name__ == "__main__":

    map = basic_map()
    mdp = DungeonMDP(map)

    import statemachine
    smmdp, statedict, actiondict = statemachine.state_machine_from_mdp(mdp)
    from connectedcomp import compute_connected_components
    ccgraph = compute_connected_components(smmdp)

    done_nodes = set(ccgraph.roots())
    todo = list(ccgraph.roots())
    while todo: 
        node = todo.pop()
        for child in node.children():
            if not child in done_nodes:
                done_nodes.add(child)
                todo.append(child)
        states = [ statedict[s] for s in node.states() ]
        print(states)

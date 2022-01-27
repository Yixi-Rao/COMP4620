from typing import Set, List
from algos import ExplicitStateValueFunction, StateValueFunction, ActionValueFunction, ExplicitActionValueFunction, one_step_lookahead, greedy_action, compute_q_from_v, greedy_policy
from MDP import State, MDP
from connectedcomp import CCGraph

def topological_vi(mdp: MDP, gamma: float, epsilon: float, graph: CCGraph) -> ExplicitStateValueFunction:
    root         = [scc for scc in graph.roots()][0]
    SCC_index    = graph.nb_components() - 1
    SCCToId_dict = {root : SCC_index}
    #! compute Id To SCC dictionary
    open_set     = set()
    open_set.add(root)
    
    while open_set:
        SCC = open_set.pop()
        for c_scc in SCC.children():
            open_set.add(c_scc)
            SCCToId_dict[c_scc] = SCCToId_dict[SCC] - 1
    
    IdToSCC_dict = {id : scc for scc, id in SCCToId_dict.items()}
    SCC_vs       = ExplicitStateValueFunction()
        
    for i in range(SCC_index + 1):
        SCC_i = IdToSCC_dict[i]
        #! value_iteration(mdp, gamma, epsilon)
        while True:
            #! q = compute_q_from_v(mdp, SCC_vs, gamma)
            q = ExplicitActionValueFunction()
            for s in SCC_i.states():
                for a in mdp.applicable_actions(s):
                    q.set_value(s, a, one_step_lookahead(mdp, SCC_vs, gamma, s, a))        
            #! greedy_policy(mdp, q)
            newvs = ExplicitStateValueFunction()
            for s in SCC_i.states():
                _, val = greedy_action(mdp, q, s)
                newvs.set_value(s, val)
            #! state_value_difference(mdp, SCC_vs, newvs)    
            diff = max([abs(SCC_vs.value(s) - newvs.value(s)) for s in SCC_i.states()])
            if diff < epsilon:
                for s in SCC_i.states():
                    SCC_vs.set_value(s, newvs.value(s))
                break
            
            for s in SCC_i.states():
                SCC_vs.set_value(s, newvs.value(s))
        
    return SCC_vs
        

# eof
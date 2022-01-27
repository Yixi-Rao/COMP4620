from typing import Any, List, FrozenSet, Set
from MDP import State, MDP

class ConnectedComponent:
    def __init__(self, states: List[State], children: Set[Any]) -> None:
        self.states_   = states
        self.children_ = children

    def states(self) -> List[State]:
        return self.states_

    def children(self) -> List[Any]:
        return self.children_
    
    def __repr__(self):
        return f'<{self.states_}->{self.children_}>'

class CCGraph:
    def __init__(self) -> None:
        self.roots_ = set() # all connected components can be reached from the roots

    def add_connected_component(self, cc: ConnectedComponent) -> None:
        self.roots_ = self.roots_.difference(cc.children())
        self.roots_.add(cc)

    def roots(self) -> Set[ConnectedComponent]:
        return self.roots_

    def print(self) -> None:
        todo = set()
        node_to_int = {}
        nb_nodes = 0
        for node in self.roots_:
            node_to_int[node] = nb_nodes
            nb_nodes += 1
            todo.add(node)
        
        while todo:
            node = todo.pop()
            for next in node.children():
                if not next in node_to_int:
                    node_to_int[next] = nb_nodes
                    nb_nodes += 1
                    todo.add(next)
            print(f'{node_to_int[node]} -> { [node_to_int[next] for next in node.children()] }')
            # print(node.states())

    def nb_components(self) -> int:
        open = set()
        closed = set()
        for cc in self.roots():
            open.add(cc)
            closed.add(cc)

        result = 0
        while open:
            cc = open.pop()
            result += 1
            for child in cc.children():
                if child in closed:
                    continue
                open.add(child)
                closed.add(child)

        return result


def firstDFS(state, visited, stack, graph):
    visited[state] = True
    
    for s in graph[state]:
        if visited[s] == False:
            firstDFS(s, visited, stack, graph)
    stack = stack.append(state)
    
def secondDFS(state, visited, graph):
    visited[state] = True
    SCC1 = [state]

    for s in graph[state]:
        if visited[s] == False:
            SCC2 = secondDFS(s, visited, graph)
            SCC1 = SCC1 + SCC2
    return SCC1

def compute_connected_components(mdp: MDP) -> CCGraph:
    '''using the Kosaraju's algorithm. the reference is https://www.geeksforgeeks.org/strongly-connected-components/
    '''
#!------------------------------------compute graph-------------------------------------------------------
    graph          = {} # default dictionary to store graph
    IdToState_dict = {}
    Id             = 0
    
    open_set = set()
    known    = set()
    open_set.add(mdp.initial_state())
    known.add(mdp.initial_state())
    
    while open_set:
        state = open_set.pop()
        IdToState_dict[Id] = state
        Id = Id + 1
        graph[state] = set()
        for act in mdp.applicable_actions(state):
            for next_state, _, _ in mdp.next_states(state, act):
                graph[state].add(next_state)
                if not next_state in known:
                    open_set.add(next_state)
                    known.add(next_state)
#!-----------------------------------Kosaraju's algorithm--------------------------------------------------------  
  #*--------------first DFS------------------------------
    stack   = []
    visited = {state : False for state in graph.keys()}
    
    for state, visit in visited.items():
        if visit == False:
            firstDFS(state, visited, stack, graph)
  #*--------------compute invert graph-----------------------------
    inv_graph = {v : [] for v in graph.keys()} 
    for v, us in graph.items():
        for u in us:
            inv_graph[u].append(v)
  #*--------------second DFS------------------------------        
    visited    = {state : False for state in graph.keys()}
    SCC_states = []
    
    while stack:
        state = stack.pop()
        if visited[state] == False:
            SCC_states.append(secondDFS(state, visited, inv_graph))
  #*---------------------------------------------- 
#!----------------bulid CC graph---------------------------------------------------------------------------  
    SCCG = CCGraph()
    SCCs = {frozenset(states) : ConnectedComponent(states, set()) for states in SCC_states}
    for i in range(len(SCC_states)):
        states = SCC_states[i]
        
        if i != len(SCC_states) - 1:
            next_scc = SCCs[frozenset(SCC_states[i + 1])]
            SCCs[frozenset(states)].children_ = {next_scc}
            
    for states in SCC_states[::-1]:
        SCCG.add_connected_component(SCCs[frozenset(states)])

    return SCCG


# eof
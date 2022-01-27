from typing import List, Tuple, Callable
from MDP import Action, State, MDP


def modify_action_reward(mdp: MDP, act: Action, delta: float) -> MDP:
    '''
        Returns an MDP equivalent to the specified MDP,
        except that the transitions associated with the specified action
        have a value modified by 'delta'.
    '''
    class mod_act_MDP(MDP):
        def __init__(self, mdp, mod, delta):
            self.ori_mdp_ = mdp
            self.mod_     = mod
            self.delta_   = delta

        def states(self) -> List[State]:
            return self.ori_mdp_.states()

        def actions(self) -> List[Action]:
            return self.ori_mdp_.actions()

        def applicable_actions(self, s: State) -> List[Action]:
            return self.ori_mdp_.applicable_actions(s)

        def next_states(self, s: State, a: Action) -> List[Tuple[State, float, float]]:
            new_states = self.ori_mdp_.next_states(s, a)
            if a == self.mod_:
                return [(si, pro, rew + self.delta_) for si, pro, rew in new_states]
            return new_states

        def initial_state(self) -> State:
            return self.ori_mdp_.initial_state()

    modified_mdp = mod_act_MDP(mdp, act, delta)
    return modified_mdp


def penalise_condition(mdp: MDP, condition: Callable[[State], bool], delta: float) -> MDP:
    '''
        Returns an MDP equivalent to the specified MDP, 
        except that the specified action is forbidden in states in which other actions are possible.
    '''
    class cond_act_MDP(MDP):
        def __init__(self, mdp, cond, delta):
            self.ori_mdp_ = mdp
            self.cond_    = cond
            self.delta_   = delta

        def states(self) -> List[State]:
            return self.ori_mdp_.states()

        def actions(self) -> List[Action]:
            return self.ori_mdp_.actions()

        def applicable_actions(self, s: State) -> List[Action]:
            return self.ori_mdp_.applicable_actions(s)

        def next_states(self, s: State, a: Action) -> List[Tuple[State, float, float]]:
            modified_states = []
            new_states      = self.ori_mdp_.next_states(s, a)
            for si, pro, rew in new_states:
                if(self.cond_(si)):
                    modified_states.append((si, pro, rew - delta))
                else:
                    modified_states.append((si, pro, rew))
            return modified_states

        def initial_state(self) -> State:
            return self.ori_mdp_.initial_state()

    modified_mdp = cond_act_MDP(mdp, condition, delta)
    return modified_mdp
    

def forbid_action(mdp: MDP, act: Action) -> MDP:
    '''
       Returns an MDP equivalent to the specified MDP, 
       except that the specified action is forbidden in states in which other actions are possible.
    '''
    class fbd_act_MDP(MDP):
        def __init__(self, mdp, fbd):
            self.ori_mdp_ = mdp
            self.fbd_     = fbd

        def states(self) -> List[State]:
            return self.ori_mdp_.states()

        def actions(self) -> List[Action]:
            return self.ori_mdp_.actions()

        def applicable_actions(self, s: State) -> List[Action]:
            result = self.ori_mdp_.applicable_actions(s)
            if len(result) != 1:
                new_result = [a for a in result if a != self.fbd_]
                return new_result
            else:
                return result

        def next_states(self, s: State, a: Action) -> List[Tuple[State, float, float]]:
            return self.ori_mdp_.next_states(s, a)

        def initial_state(self) -> State:
            return self.ori_mdp_.initial_state()

    modified_mdp = fbd_act_MDP(mdp, act)
    return modified_mdp


def forbid_two_actions(mdp: MDP, act: Action) -> MDP:
    '''
      Returns an MDP equivalent to the specified MDP, 
      except that the specified action can be applied only once.
    '''
    class counter_state(State):
        def __init__(self, state, inherit_act_used=None):
            self.ori_state_ = state
            self.act_used_  = frozenset(set()) if inherit_act_used==None else frozenset(inherit_act_used) # record whether the specific action is used
            # same as dangeon state
            self.party_          = self.ori_state_.party_
            self.location_       = self.ori_state_.location_
            self.visited_places_ = self.ori_state_.visited_places_
            
            self.debug_mode = False
        
        def update_act_used(self, act):
            before_set = {act for act in self.act_used_}
            before_set.add(act)
            self.act_used_  = frozenset(before_set)
        
        def __eq__(self, state) -> bool:
            if not self.party_ == state.party_:
                return False
            if not self.location_ == state.location_:
                return False
            if not self.visited_places_ == state.visited_places_:
                return False
            if not self.act_used_ == state.act_used_:
                return False
            return True
        
        def __repr__(self) -> str:
            if self.debug_mode:
                return f'<{self.party_},{self.location_},{self.visited_places_},{self.act_used_}>'
            return self.ori_state_.__repr__()
        
        def __hash__(self):
            v1 = self.party_.__hash__()
            v2 = self.location_.__hash__()
            v3 = self.visited_places_.__hash__()
            v4 = self.act_used_.__hash__()
            return v1 + v2 + v3 + v4
            
    class one_act_MDP(MDP):
        def __init__(self, mdp, act_1):
            self.ori_mdp_ = mdp
            self.act_1_   = act_1
        
        def states(self) -> List[State]:
            return self.ori_mdp_.states()

        def actions(self) -> List[Action]:
            return self.ori_mdp_.actions()

        def applicable_actions(self, s: State) -> List[Action]:
            '''if specific action is used then it will be removed from the return list
            '''
            result   = self.ori_mdp_.applicable_actions(s)  
            act_used = s.act_used_
        
            if self.act_1_ in act_used and self.act_1_ in result:
                result.remove(self.act_1_)
            
            return result

        def next_states(self, s: State, a: Action) -> List[Tuple[State, float, float]]:
            '''create new counter_state for the next_state to record the actions used
            '''
            new_states      = self.ori_mdp_.next_states(s, a)
            modified_states = []
            
            for si, pro, rew in new_states:
                inherit = set([a for a in s.act_used_])
                if a == self.act_1_:
                    inherit.add(a)
                si_counter_state = counter_state(si, inherit)
                
                modified_states.append((si_counter_state, pro, rew))
                
            return modified_states

        def initial_state(self) -> State:
            return counter_state(self.ori_mdp_.initial_state())

    modified_mdp = one_act_MDP(mdp, act)
    return modified_mdp


def one_action_between(mdp: MDP, a: Action, b: Action) -> MDP:
    '''
      Returns an MDP equivalent to the specified MDP,
      except that the first specified action can be applied multiple times 
      only if the second specified action is applied between its occurrences.
    '''
    class ActSeq_state(State):
        def __init__(self, state, inherit_act_used=None):
            self.ori_state_ = state
            self.acts_used_  = () if inherit_act_used == None else inherit_act_used #only have three possible values: 1. () 2.(a) 3.(a,b)
            
            self.party_          = self.ori_state_.party_
            self.location_       = self.ori_state_.location_
            self.visited_places_ = self.ori_state_.visited_places_
            
            self.debug_mode = False
        
        def __eq__(self, state) -> bool:
            if not self.party_ == state.party_:
                return False
            if not self.location_ == state.location_:
                return False
            if not self.visited_places_ == state.visited_places_:
                return False
            if not self.acts_used_ == state.acts_used_:
                return False
            return True
        
        def __repr__(self) -> str:
            if self.debug_mode:
                return f'<{self.party_},{self.location_},{self.visited_places_},{self.acts_used_}>'
            return self.ori_state_.__repr__()
    
        def __hash__(self):
            v1 = self.party_.__hash__()
            v2 = self.location_.__hash__()
            v3 = self.visited_places_.__hash__()
            v4 = self.acts_used_.__hash__()
            return v1 + v2 + v3 + v4
            
    class ActSeq_MDP(MDP):
        def __init__(self, mdp, act_a, act_b):
            self.ori_mdp_ = mdp
            self.act_a_   = act_a
            self.act_b_   = act_b
        
        def states(self) -> List[State]:
            return self.ori_mdp_.states()

        def actions(self) -> List[Action]:
            return self.ori_mdp_.actions()

        def applicable_actions(self, s: State) -> List[Action]:
            '''accroding to the used actions, to dicide the applicable actions. The pattern is:
                actseq = () -> return orignal result
                actseq = (a) -> a is removed in orignal result
                actseq = (a, b) -> return orignal result
            '''
            result = self.ori_mdp_.applicable_actions(s)  
            actseq = s.acts_used_
            
            if (self.act_a_ in result) and "a" in actseq:
                if self.check_valid(actseq):
                    return result
                else:
                    result.remove(self.act_a_)
            
            return result
        
        def check_valid(self, actseq) -> bool:
            '''check whether executing the action 'a' is valid or not based on actseq
            '''
            if actseq == ():
                return True
            elif actseq == tuple("a"):
                return False
            elif actseq == ("a", "b"):
                return True
            
        def next_states(self, s: State, a: Action) -> List[Tuple[State, float, float]]:
            '''create ActSeq_statefor the next_state, and update the action used for the next state, the pattern is:
                if using a:
                    actseq = () -> actseq = (a)
                    actseq = (a, b) -> actseq = ()
                if using b:
                    actseq = (a) -> actseq = (a, b)
            '''
            new_states      = self.ori_mdp_.next_states(s, a)
            modified_states = []
            
            for si, pro, rew in new_states:
                if   a == self.act_b_ and s.acts_used_ == tuple("a"):
                    si_ActSeq_state = ActSeq_state(si, ("a", "b"))
                    
                elif a == self.act_a_ and s.acts_used_ == ("a", "b"):
                    si_ActSeq_state = ActSeq_state(si, ())
                    
                elif a == self.act_a_ and s.acts_used_ == tuple():
                    si_ActSeq_state = ActSeq_state(si, tuple("a"))
                    
                else:
                    si_ActSeq_state = ActSeq_state(si, s.acts_used_)
                    
                modified_states.append((si_ActSeq_state, pro, rew))
                
            return modified_states

        def initial_state(self) -> State:
            return ActSeq_state(self.ori_mdp_.initial_state())

    modified_mdp = ActSeq_MDP(mdp, a, b)
    return modified_mdp

# eof

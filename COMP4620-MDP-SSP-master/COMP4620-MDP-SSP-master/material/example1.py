from statemachine import StateMachine, SMTransition


def example_1() -> StateMachine: 
    '''
    Generates a StateMachine with 
    * 4 states: holds no fork, holds fork 1, holds fork 2, holds both fork
    * 4 actions: do nothing, pick fork 1, pick fork 2, eat
    Picking items has a (positive) cost and can lead to droping another item.
    Eating has a negative cost.
    '''
    return StateMachine(
        transition_function=[
            # Do nothing
            SMTransition("NoFork" , "DoNothing", 0, [("NoFork", 1)]) ,
            SMTransition("Fork1" , "DoNothing", 0, [("NoFork", 0.1), ("Fork1", 0.9)]) ,
            SMTransition("Fork2" , "DoNothing", 0, [("NoFork", 0.1), ("Fork2", 0.9)]) ,
            SMTransition("Fork12" , "DoNothing", 0, [("Fork1", 0.05), ("Fork2", 0.05), ("Fork12", 0.9)]) ,

            # pick 1
            SMTransition("NoFork" , "Pick1", 5, [("Fork1", 1)]) ,
            SMTransition("Fork1" , "Pick1", 5, [("Fork1", 1)]) ,
            SMTransition("Fork2" , "Pick1", 5, [("Fork1", 0.1), ("Fork12", 0.9)]) ,
            SMTransition("Fork12" , "Pick1", 5, [("Fork1", 0.1), ("Fork12", 0.9)]),

            # pick 2 (different values than pick 1)
            SMTransition("NoFork" , "Pick2", 20, [("Fork2", 1)]) ,
            SMTransition("Fork2" , "Pick2", 20, [("Fork2", 1)]) ,
            SMTransition("Fork1" , "Pick2", 20, [("Fork2", 0.1), ("Fork12", 0.9)]) ,
            SMTransition("Fork12" , "Pick2", 20, [("Fork2", 0.1), ("Fork12", 0.9)]),

            # eat (only possible if you have both forks)
            SMTransition("Fork12" , "Eat", -30, [("NoFork", 1)])
        ], 
        initial_state="NoFork"
    )
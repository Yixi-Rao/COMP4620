if __name__ == '__main__':
    import map
    m = map.basic_map()
    mdp = map.DungeonMDP(m)

    import modelling

    peon = m.for_hire('start')[0]
    mdp = modelling.modify_action_reward(mdp, map.HireAction(peon[1],peon[0]), +500)

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
    h = simulate(mdp, pol, 50)
    for line in h.pretty_repr():
        print(line)

# eof
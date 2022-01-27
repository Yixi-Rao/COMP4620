import unittest

class Test(unittest.TestCase):

    def test(self):
        from map import basic_map, DungeonMDP


        map = basic_map()
        mdp = DungeonMDP(map)

        import statemachine
        smmdp, statedict, actiondict = statemachine.state_machine_from_mdp(mdp)

        from connectedcomp import compute_connected_components
        ccgraph = compute_connected_components(smmdp)

        self.assertEqual(ccgraph.nb_components(),76)
        self.assertEqual(len(ccgraph.roots()),1)

def main():
    unittest.main()

if __name__ == "__main__":
    main()

# eof
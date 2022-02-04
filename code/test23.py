import unittest

class Test(unittest.TestCase):

    def test(self):
        import map
        dungeon = map.basic_map()
        for_hire = dungeon.inns_['start']
        peon = for_hire[0]
        soldier = for_hire[1]
        mdp = map.DungeonMDP(dungeon)
        state = map.DungeonState(state=mdp.initial_state(),add=soldier[1])
        state = map.DungeonState(state=state,add=peon[1])

        # testing this action:
        action = map.NoAction()

        next = action.next_states(state,dungeon)

        self.assertEqual(len(next),1)

        self.assertEqual(next[0][1],1)
        self.assertEqual(next[0][2],0)
        next_state = next[0][0]
        self.assertEqual(next_state, state)

def main():
    unittest.main()

if __name__ == "__main__":
    main()

# eof
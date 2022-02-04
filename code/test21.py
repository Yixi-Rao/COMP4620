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

        # testing this action:
        action = map.HireAction(peon[1],peon[0])

        next = action.next_states(state,dungeon)

        self.assertEqual(len(next),1)
        self.assertEqual(next[0][1],1.0)
        self.assertEqual(next[0][2],-10)

        next_state = next[0][0]

        self.assertEqual(next_state.location_, 'start')
        self.assertEqual(next_state.visited_places_, {'start'})
        party = next_state.party_
        self.assertEqual(len(party.adventurers_), 2)
        self.assertEqual(party.adventurers_[0], soldier[1])
        self.assertEqual(party.adventurers_[1], peon[1])

def main():
    unittest.main()

if __name__ == "__main__":
    main()

# eof
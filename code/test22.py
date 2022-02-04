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
        action = map.MoveAction('room1', 1)

        next = action.next_states(state,dungeon)

        self.assertEqual(len(next),2)

        index = 0
        # don't know how to explicitly test 
        # that either next[0][1] or next[1][1] almost equals .8
        if next[0][1] < .5:
            index = 1

        # Checking the state after a failed move
        self.assertAlmostEqual(next[index][1],.8)
        self.assertEqual(next[index][2],0)
        next_state = next[index][0]
        self.assertEqual(next_state.location_, 'start')
        self.assertEqual(next_state.visited_places_, {'start'})
        party = next_state.party_
        self.assertEqual(len(party.adventurers_), 1)
        self.assertEqual(party.adventurers_[0], soldier[1])

        # Checking the state after a successful move
        index = 1-index
        self.assertAlmostEqual(next[index][1],.2)
        self.assertEqual(next[index][2],0)
        next_state = next[index][0]
        self.assertEqual(next_state.location_, 'room1')
        self.assertEqual(next_state.visited_places_, {'start','room1'})
        party = next_state.party_
        self.assertEqual(len(party.adventurers_), 2)
        self.assertEqual(party.adventurers_[0], soldier[1])
        self.assertEqual(party.adventurers_[1], peon[1])


def main():
    unittest.main()

if __name__ == "__main__":
    main()

# eof
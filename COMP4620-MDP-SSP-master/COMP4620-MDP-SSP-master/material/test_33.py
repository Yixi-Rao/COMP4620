import unittest
from student_example2 import TrafficLightDomain, TrafficLightState, TrafficLightAction, SingleLightState
from skdecide import TransitionValue

class Test(unittest.TestCase):

    def test(self):
        dom = TrafficLightDomain()

        state = TrafficLightState(cars_queueing_north=3, cars_queueing_east=2, north_light=SingleLightState.RECENT_RED, east_light=SingleLightState.RED)
        actions = dom.get_applicable_actions(state)
        self.assertEqual(len(actions.get_elements()), 1, msg="Wrong number of actions applicable in this state")
        self.assertTrue(TrafficLightAction.DO_NOT_SWITCH in actions.get_elements())

        state = TrafficLightState(cars_queueing_north=3, cars_queueing_east=2, north_light=SingleLightState.RED, east_light=SingleLightState.GREEN)
        actions = dom.get_applicable_actions(state)
        self.assertEqual(len(actions.get_elements()), 2, msg="Wrong number of actions applicable in this state")
        self.assertTrue(TrafficLightAction.DO_NOT_SWITCH in actions.get_elements())
        self.assertTrue(TrafficLightAction.SWITCH in actions.get_elements())

        


def main():
    unittest.main()

if __name__ == "__main__":
    main()

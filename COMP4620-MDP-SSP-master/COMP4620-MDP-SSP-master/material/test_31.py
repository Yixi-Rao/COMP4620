import unittest
from student_example2 import TrafficLightDomain, TrafficLightState, TrafficLightAction, SingleLightState
from skdecide import TransitionValue

class Test(unittest.TestCase):

    def test(self):
        dom = TrafficLightDomain()

        state = TrafficLightState(cars_queueing_north=3, cars_queueing_east=2, north_light=SingleLightState.RECENT_RED, east_light=SingleLightState.RED)
        next_state = TrafficLightState(cars_queueing_north=3, cars_queueing_east=3, north_light=SingleLightState.RED, east_light=SingleLightState.GREEN)
        action = TrafficLightAction.DO_NOT_SWITCH
        self.assertEqual(dom.get_transition_value(state, action, next_state), TransitionValue(cost=6))
        


def main():
    unittest.main()

if __name__ == "__main__":
    main()

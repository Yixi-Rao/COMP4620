import unittest
from student_example2 import TrafficLightDomain, TrafficLightState, TrafficLightAction, SingleLightState
from skdecide import TransitionValue

class Test(unittest.TestCase):

    def test(self):
        dom = TrafficLightDomain()

        state = TrafficLightState(cars_queueing_north=3, cars_queueing_east=2, north_light=SingleLightState.RECENT_RED, east_light=SingleLightState.RED)
        self.assertTrue(state in dom.get_observation_space().get_elements())

        state = TrafficLightState(cars_queueing_north=3, cars_queueing_east=2, north_light=SingleLightState.RED, east_light=SingleLightState.GREEN)
        self.assertTrue(state in dom.get_observation_space().get_elements())

        


def main():
    unittest.main()

if __name__ == "__main__":
    main()

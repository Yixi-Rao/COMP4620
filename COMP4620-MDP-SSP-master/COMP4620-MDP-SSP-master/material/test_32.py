import unittest
from student_example2 import TrafficLightDomain, TrafficLightState, TrafficLightAction, SingleLightState
from skdecide import TransitionValue

class Test(unittest.TestCase):

    def test(self):
        dom = TrafficLightDomain()

        state = TrafficLightState(cars_queueing_north=3, cars_queueing_east=2, north_light=SingleLightState.RECENT_RED, east_light=SingleLightState.RED)
        action = TrafficLightAction.DO_NOT_SWITCH
        next_states = dom.get_next_state_distribution(state, action)

        # check that the sum of probabilities is one
        sum: float = 0
        for _, prob in next_states.get_values():
            self.assertGreater(prob, 0, "Probabilities need to be strictly greater than 0")
            sum = sum + prob
        self.assertAlmostEqual(sum, 1, delta=.001, msg="Probabilities should sum up to 1")

        # Verifies the individual probabilities
        expected_result = {
            TrafficLightState(cars_queueing_north=3, cars_queueing_east=1, north_light=SingleLightState.RED, east_light=SingleLightState.GREEN): 0.56, 
            TrafficLightState(cars_queueing_north=3, cars_queueing_east=2, north_light=SingleLightState.RED, east_light=SingleLightState.GREEN): 0.14,
            TrafficLightState(cars_queueing_north=4, cars_queueing_east=1, north_light=SingleLightState.RED, east_light=SingleLightState.GREEN): 0.24, 
            TrafficLightState(cars_queueing_north=4, cars_queueing_east=2, north_light=SingleLightState.RED, east_light=SingleLightState.GREEN): 0.06
        }

        for next_state, prob in next_states.get_values():
            self.assertAlmostEqual(prob, expected_result[next_state], delta=0.001, msg="Wrong probability")
        


def main():
    unittest.main()

if __name__ == "__main__":
    main()

import unittest
from value import ValueFunction, compute_value_function_of_policy
from policy import Policy
from little_robot import default_robot, GridState

class Test(unittest.TestCase):

    def test(self):
        rob = default_robot()
        policy: Policy = Policy(domain=rob, default_action=rob.action('right'))
        values: ValueFunction = compute_value_function_of_policy(pol=policy, gamma=0.8,epsilon=0.0001)
        
        self.assertAlmostEqual(values[GridState(0,0)], 3.7, delta=0.1)
        self.assertAlmostEqual(values[GridState(3,4)], 5, delta=0.1)
        self.assertAlmostEqual(values[GridState(4,2)], 0, delta=0.1)
        

def main():
    unittest.main()

if __name__ == "__main__":
    main()

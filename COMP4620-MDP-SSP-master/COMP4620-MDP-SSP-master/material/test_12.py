import unittest
from value import ValueFunction
from policy import Policy
from little_robot import default_robot, GridState

class Test(unittest.TestCase):

    def test(self):
        rob = default_robot()
        values = ValueFunction(domain=rob, default_value=1)
        values[GridState(1,2)] = 2
        policy: Policy = Policy(domain=rob, default_action=rob.action('right'))
        bvalues,error = values.compute_single_policy_backup(policy=policy, gamma=0.8)
        self.assertEqual(bvalues[GridState(0,2)], 2.2, msg="Error in the new value function")
        self.assertEqual(bvalues[GridState(0,1)], 1.8, msg="Error in the new value function")
        self.assertEqual(bvalues[GridState(4,2)], 0, msg="Terminal states should have a value of 0")
        self.assertAlmostEqual(error, 1.2, delta=0.001, msg="Error in error returned by the method")
        self.assertEqual(values[GridState(0,2)], 1, msg="Do not modify the original value function!")

def main():
    unittest.main()

if __name__ == "__main__":
    main()

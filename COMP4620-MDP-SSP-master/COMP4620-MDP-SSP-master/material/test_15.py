import unittest
from value import ValueFunction
from little_robot import default_robot, GridState

class Test(unittest.TestCase):

    def test(self):
        rob = default_robot()
        values = ValueFunction(domain=rob, default_value=3)
        values[GridState(1,2)] = 1

        self.assertEqual(values.greedy_action(GridState(0,2), gamma=0.8), (rob.action(name="right"), 2.6))
        

def main():
    unittest.main()

if __name__ == "__main__":
    main()

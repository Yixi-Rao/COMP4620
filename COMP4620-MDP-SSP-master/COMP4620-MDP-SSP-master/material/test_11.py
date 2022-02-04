import unittest
from value import ValueFunction
from little_robot import default_robot, GridState

class Test(unittest.TestCase):

    def test(self):
        rob = default_robot()
        values = ValueFunction(domain=rob, default_value=1)
        values[GridState(1,2)] = 2
        self.assertEqual(values.q_value(state=GridState(0,2), action=rob.action(name="right"), gamma=0.8), 2.2)
        


def main():
    unittest.main()

if __name__ == "__main__":
    main()

import unittest
from value import ValueFunction
from little_robot import default_robot, GridState

class Test(unittest.TestCase):

    def test(self):
        rob = default_robot()
        values = ValueFunction(domain=rob, default_value=3)
        values[GridState(1,2)] = 1
        bvalues, error = values.compute_bellmann_backup(gamma=.8)

        self.assertEqual(values[GridState(0,0)], 3)
        self.assertAlmostEqual(bvalues[GridState(0,0)], 3.4, delta=.01)
        self.assertAlmostEqual(bvalues[GridState(0,2)], 2.6, delta=.01)
        self.assertAlmostEqual(bvalues[GridState(4,2)], 0, delta=.01)
        self.assertEqual(error, 3)
        

def main():
    unittest.main()

if __name__ == "__main__":
    main()

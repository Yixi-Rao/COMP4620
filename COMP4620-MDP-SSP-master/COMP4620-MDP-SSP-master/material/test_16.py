import unittest
from vi import ValueIteration
from little_robot import default_robot, GridState

class Test(unittest.TestCase):

    def test(self):
        rob = default_robot()
        vi = ValueIteration(domain=rob, gamma=0.8)
        vi.backup()

        self.assertAlmostEqual(vi.value(GridState(4,2)), 0, delta=0.1)
        self.assertAlmostEqual(vi.value(GridState(3,2)), 1.4, delta=0.1)
        self.assertAlmostEqual(vi.value(GridState(0,2)), 3.5868, delta=0.1)
        

def main():
    unittest.main()

if __name__ == "__main__":
    main()
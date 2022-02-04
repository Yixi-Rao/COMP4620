import unittest
from pi import PolicyIteration
from policy import Policy
from little_robot import default_robot, GridState

class Test(unittest.TestCase):

    def test(self):
        rob = default_robot()
        pi = PolicyIteration(domain=rob, epsilon=0.1, max_iterations=1000, gamma=0.8)

        pi.refine_policy()
        pi.refine_policy()
        pol: Policy = pi.get_policy()
        
        self.assertEqual(pol[GridState(4,1)], rob.action("up"))
        self.assertEqual(pol[GridState(3,2)], rob.action("right"))
        

def main():
    unittest.main()

if __name__ == "__main__":
    main()

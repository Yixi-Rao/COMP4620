import unittest
from example1 import example_1
from rtdp import RTDP

class Test(unittest.TestCase):

    def test(self):
        domain = example_1()
        rtdp = RTDP(domain, 0.9)
        rtdp.run_n_simulations(50, 500)
        policy = rtdp.policy()

        self.assertEqual(policy[domain.state("NoFork")], domain.action("Pick1"))
        self.assertEqual(policy[domain.state("Fork1")], domain.action("Pick2"))
        self.assertEqual(policy[domain.state("Fork2")], domain.action("Pick1"))
        self.assertEqual(policy[domain.state("Fork12")], domain.action("Eat"))
        

def main():
    unittest.main()

if __name__ == "__main__":
    main()

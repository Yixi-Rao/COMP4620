from typing import Optional, Dict, Tuple

from interface import Assignment1Domain, State, Action

from value import ValueFunction, compute_value_function_of_policy
from policy import Policy

class PolicyIteration:
  '''
    PolicyIteration is the class that is used to perform the Policy Iteration algorithm.
    It contains the domain, the current policy, and other misc information.
  '''
  _domain: Assignment1Domain
  _policy: Policy
  _gamma: float
  _epsilon: float
  _max_iterations: int

  def __init__(self, domain: Assignment1Domain, epsilon: Optional[float] = 0.01, max_iterations: Optional[float] = 1000, gamma: Optional[float] = 0.9):
    self._domain = domain
    self._policy = Policy(domain)
    self._gamma = gamma
    self._epsilon = epsilon
    self._max_iterations = max_iterations

  def get_policy(self) -> Policy:
      '''
        Returns the current policy.
      '''
      return self._policy

  def refine_policy(self) -> None:
      '''
        Performs one iteration of the policy iteration algorithm.  
      '''
      # DONE
      value_function = compute_value_function_of_policy(self.get_policy(),self._gamma)
      self._policy = value_function.greedy_policy(self._gamma)

  def policy_iteration(self) -> None:
      '''
        Performs the policy iteration algorithm.
      '''
      for _i in range(self._max_iterations):
          old_policy = self._policy
          self.refine_policy()
          new_policy = self._policy
          if old_policy == new_policy:
              return


if __name__ == '__main__':
    import example1
    domain = example1.example_1()

    pi = PolicyIteration(domain, 0.01, 1000, 0.9)
    pi.get_policy().print()

    pi.refine_policy()
    pi.get_policy().print()

    pi.refine_policy()
    pi.get_policy().print()

    pi.policy_iteration()
    pi.get_policy().print()

'''
+++++++
Policy:
State NoFork -> DoNothing
State Fork1 -> DoNothing
State Fork2 -> DoNothing
State Fork12 -> DoNothing
+++++++
Policy:
State NoFork -> DoNothing
State Fork1 -> DoNothing
State Fork2 -> DoNothing
State Fork12 -> Eat
+++++++
Policy:
State NoFork -> DoNothing
State Fork1 -> Pick2
State Fork2 -> Pick1
State Fork12 -> Eat
+++++++
Policy:
State NoFork -> Pick1
State Fork1 -> Pick2
State Fork2 -> Pick1
State Fork12 -> Eat

'''
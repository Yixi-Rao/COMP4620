from typing import List, Tuple

from rewardwrapper import RewardWrapper
from sarsa import Sarsa
from qlearning import QLearning
from domain import RLEnvironment
from q import Q, TemporalDifference
from cheatingcricket import cheating_cricket_team_2
import sys

def write_rewards(filename: str, datum: Tuple[List[float], str]) -> None:
    with open(filename, 'w') as file:
        file.write("{}\n".format(datum[1]))
        for value in datum[0]:
            file.write('{}\n'.format(value))

def read_rewards(filename: str) -> Tuple[List[float], str]:
    name: str
    list: List[float] = []
    with open(filename, 'r') as file:
        name = file.readline().rstrip()
        for line in file:
            list.append(float(line))
    return list, name

def basic_qlearning(domain: RLEnvironment, alpha: float, gamma: float, epsilon: float, length: int) -> Tuple[List[float],str]:
    wrap: RewardWrapper = RewardWrapper(domain)
    q: Q = TemporalDifference(alpha=alpha)
    ms: QLearning = QLearning(wrap, epsilon=epsilon, gamma=gamma, q=q)
    ms.reset()
    for _i in range(length):
        if _i % int(length / 10) == 0:
            print('+', end='', flush=True)
        elif _i % int(length / 100) == 0:
            print('.', end='', flush=True)
        ms.execute_one_action()
    print()
    return wrap.get_reward_summary(gamma), "Q-Learning with epsilon={}".format(epsilon)

def basic_sarsa(domain: RLEnvironment, alpha:float, gamma: float, epsilon: float, length: int) -> Tuple[List[float],str]:
    wrap: RewardWrapper = RewardWrapper(domain)
    q: Q = TemporalDifference(alpha=alpha)
    ms: Sarsa = Sarsa(wrap, epsilon=epsilon, gamma=gamma, q=q)
    ms.reset()
    for _i in range(length):
        if _i % int(length / 10) == 0:
            print('+', end='', flush=True)
        elif _i % int(length / 100) == 0:
            print('.', end='', flush=True)
        ms.execute_one_action()
    print()
    return wrap.get_reward_summary(gamma), "SARSA with epsilon={}".format(epsilon)

if __name__ == "__main__":
    read: bool = False
    write: bool = False
    prefix: str = "./"

    if len(sys.argv) > 1:
        if sys.argv[1] == 'r':
            read = True
        if sys.argv[1] == 'w':
            write = True
    if len(sys.argv) > 2:
        prefix = sys.argv[2]
    
    domain: RLEnvironment = cheating_cricket_team_2()
    alpha: float = .05
    gamma = .99
    epsilon = .05
    
    data: List[Tuple[List[float],str]] = []
    DEFAULT_DURATION = 500000

    datum: Tuple[List[float],str] = ([],"Zero")
    for _i in range(DEFAULT_DURATION):
        datum[0].append(0)
    data.append(datum)

    filename = prefix + "q2_1"
    if read: 
        datum = read_rewards(filename)
    else:
        datum = basic_sarsa(domain, alpha=alpha, gamma=gamma, epsilon=epsilon, length=DEFAULT_DURATION)
        if write:
            write_rewards(filename, datum)
    data.append(datum)

    filename = prefix + "q2_2"
    if read: 
        datum = read_rewards(filename)
    else:
        datum = basic_qlearning(domain, alpha=alpha, gamma=gamma, epsilon=epsilon, length=DEFAULT_DURATION)
        if write:
            write_rewards(filename, datum)
    data.append(datum)

    print("Average discounted reward:")
    print("---------------+------------+------------+")
    print("Algorithm:     | SARSA      | Q-Learning |")
    print("---------------+------------+------------+")
    for i in range(10):
        sum1 = 0
        sum2 = 0
        steps = int(len(data[1][0])/10)
        for j in range(steps):
            sum1 += data[1][0][ (i*steps) + j ]
            sum2 += data[2][0][ (i*steps) + j ]
        print("      {:2} 10th: | {:10.4f} | {:10.4f} |".format((i+1), sum1/steps, sum2/steps))
    print("---------------+------------+------------+")

    from plot import plot_rewards
    plot_rewards(data)
    
'''
  Explain here why SARSA performs better than Q-learning during the learning.
  QL is the off-policy algorithm, which updates the Q value based on the best reward of the next state-action pair, so QL directly learns the optimal policy,
  while SARSA is on-policy, which updates the Q value based on what the agent had tried, so SARAS will learn a  SARSA learns a near optimal policy. The SARSA will 
  produce a more conservative policy since it allows for possible penalties from exploratory moves, while QL will ignore them. As a result, during the learning, SARSA will create a 
  less risky policy and it is stable, which performs better than QL since QL will have risk of making mistakes during the learning process

'''

# eof
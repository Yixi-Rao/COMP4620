from typing import List, Tuple

import sys

from rewardwrapper import RewardWrapper
from qlearning import QLearning
from domain import RLEnvironment
from q import Q, TemporalDifference
from cricket import cricket_team_2

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
    ms: QLearning = QLearning(domain=wrap, epsilon=epsilon, gamma=gamma, q=q)
    ms.reset()
    for _i in range(length):
        if _i % int(length / 10) == 0:
            print('+', end='', flush=True)
        elif _i % int(length / 100) == 0:
            print('.', end='', flush=True)
        ms.execute_one_action()
    print()
    return wrap.get_reward_summary(gamma), "Q-Learning with epsilon={}".format(epsilon)

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

    domain: RLEnvironment = cricket_team_2()
    alpha: float = .05
    gamma = .99
    
    data: List[Tuple[List[float],str]] = []
    DEFAULT_DURATION = 100000

    datum: Tuple[List[float],str] = ([],"Zero")
    for _i in range(DEFAULT_DURATION):
        datum[0].append(0)
    data.append(datum)
    
    epsilon = .1
    filename = prefix + "q1_1"
    if read: 
        datum = read_rewards(filename)
    else:
        datum = basic_qlearning(domain, alpha=alpha, gamma=gamma, epsilon=epsilon, length=DEFAULT_DURATION)
        if write:
            write_rewards(filename, datum)
    data.append(datum)

    epsilon = .01
    filename = prefix + "q1_2"
    if read: 
        datum = read_rewards(filename)
    else:
        datum = basic_qlearning(domain, alpha=alpha, gamma=gamma, epsilon=epsilon, length=DEFAULT_DURATION)
        if write:
            write_rewards(filename, datum)
    data.append(datum)

    print("Average discounted reward:")
    print("---------------+------------+------------+")
    print("Epsilon:       | {:10.2f} | {:10.2f} |".format(.1,.01))
    print("---------------+------------+------------+")
    for i in range(10):
        sum1 = 0
        sum2 = 0
        steps = int(DEFAULT_DURATION/10)
        for j in range(steps):
            sum1 += data[1][0][ (i*steps) + j ]
            sum2 += data[2][0][ (i*steps) + j ]
        print("      {:2} 10th: | {:10.4f} | {:10.4f} |".format((i+1), sum1/steps, sum2/steps))
    print("---------------+------------+------------+")

    from plot import plot_rewards
    plot_rewards(data)

'''
  Explain here why Q-learning with epsilon value of 0.01 performs better than Q-learning with epsilon value of 0.1:
  
  epsilon value is the probability that the agent will try random actions, epsilon value of 0.1 is ten times as much as epsilon value of 0.01
  so Q-learning with epsilon value of 0.1 will more likely choose random actions and never use the past knowledge, so it will encounter some case
  where the RL has learnt that it don't need to move to the poor state but it has a 10% of moving randomly to some trivial states, therefore
  at this point, it is moving blindly and uselessly and it is not the purpose of exploration. So larger epsilon value will spend more time for the 
  Q value to converge.
  

'''

# eof
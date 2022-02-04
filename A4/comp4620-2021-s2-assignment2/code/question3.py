from typing import List, Tuple

from rewardwrapper import RewardWrapper
from sarsa import Sarsa
from qlearning import QLearning
from domain import RLEnvironment
from q import Q, TemporalDifference, greedy_action

from cheatingcricket import cheating_cricket_team_3
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

def learn_with_sarsa(domain: RLEnvironment, alpha: float, gamma: float, epsilon: float, length: int) -> Q:
    q: Q = TemporalDifference(alpha=alpha)
    ms: Sarsa = Sarsa(domain, epsilon=epsilon, gamma=gamma, q=q)
    ms.reset()
    for _i in range(length):
        if _i % int(length / 10) == 0:
            print('+', end='', flush=True)
        elif _i % int(length / 100) == 0:
            print('.', end='', flush=True)
        ms.execute_one_action()
    return q

def learn_with_qlearning(domain: RLEnvironment, alpha: float, gamma: float, epsilon: float, length: int) -> Q:
    q: Q = TemporalDifference(alpha=alpha)
    ms: QLearning = QLearning(domain, epsilon=epsilon, gamma=gamma, q=q)
    ms.reset()
    for _i in range(length):
        if _i % int(length / 10) == 0:
            print('+', end='', flush=True)
        elif _i % int(length / 100) == 0:
            print('.', end='', flush=True)
        ms.execute_one_action()
    return q

def use_q(domain: RLEnvironment, q: Q, gamma: float, length: int) -> List[float]:
    wrap: RewardWrapper = RewardWrapper(domain)
    state = wrap.reset()
    for _i in range(length):
        action = greedy_action(q,domain)
        envout = wrap.execute(action)
        state = envout.state
    return wrap.get_reward_summary(gamma)

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
    
    domain: RLEnvironment = cheating_cricket_team_3()
    alpha: float = .1
    gamma = .99
    epsilon = .05
    
    data: List[Tuple[List[float],str]] = []
    TRAINING_DURATION = 400000
    DEFAULT_DURATION = 2000

    datum: Tuple[List[float],str] = ([],"Zero")
    for _i in range(DEFAULT_DURATION):
        datum[0].append(0)
    data.append(datum)

    filename = prefix + "q3_1"
    if read:
        datum = read_rewards(filename)
    else:
        q = learn_with_sarsa(domain, alpha=alpha, gamma=gamma, epsilon=epsilon, length=TRAINING_DURATION)
        print()
        datum = use_q(domain, q, gamma, length=DEFAULT_DURATION), "SARSA"
        if write:
            write_rewards(filename, datum)
    data.append(datum)

    filename = prefix + "q3_2"
    if read:
        datum = read_rewards(filename)
    else:
        q = learn_with_qlearning(domain, alpha=alpha, gamma=gamma, epsilon=epsilon, length=TRAINING_DURATION)
        print()
        datum = use_q(domain, q, gamma, length=DEFAULT_DURATION), "Q-Learning"
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
  Explain here why Q-learning performs better than SARSA after the learning.
  
  Q-learning is off-policy algorithm that means it performs the ε-greedy policy but evaluating and generating optimal policy, so after the training,
  the policy will be switched to the greedy policy(practical purpose) from the ε-greedy policy (training purpose), the optimal policy that is what 
  Q-learning have learned and refined. As a result, it will perform well. For the SARSA, it is assumed that it will keep using the current policy, so the 
  purpose of the SARSA is to train a policy that is optimal under the assumption that the same policy will be used, and this policy will consider some randomness,
  which will influence the policy it produced.Imaged that the SARSA is used after the learning, it switches to a greedy policy, then it will choose the action that is
  safer, less risk, longer, less optimal.So, Q-learning performs better than SARSA after the learning.


'''

# eof

import matplotlib.pyplot as plt
from typing import List, Tuple

def plot_rewards(data: List[Tuple[List[float],str]]):

    for list, name in data:
        plt.plot(list, label=name)

    plt.legend(loc='lower right')
    plt.show()

# eof
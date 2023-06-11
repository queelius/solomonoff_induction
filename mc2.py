import random
from collections import defaultdict

# Define a Markov Chain model with specified order
class MarkovChain:
    def __init__(self, order):
        self.order = order
        self.model = defaultdict(lambda: defaultdict(int))

    def train(self, data):
        for i in range(len(data) - self.order - 1):
            state = data[i:i+self.order]
            next_state = data[(i+1):(i+self.order+1)]
            self.model[state][next_state] += 1

    def generate(self, start_state, length):
        result = start_state
        current_state = start_state
        for i in range(length - self.order - 1):
            print(f'iteration: {i}, current_state: {current_state}')
            next_state = self.pick_next_state(current_state)
            print(f'next_state: {next_state}')
            result += next_state
            print(f'result: {result}')
            current_state = current_state[1:] + next_state
            print(f'current_state #2: {current_state}')
        return result

    def pick_next_state(self, state):
        candidates = list(self.model[state].items())
        total_count = sum(count for _, count in candidates)
        r = random.uniform(0, total_count)
        s = 0
        for candidate, count in candidates:
            s += count
            if s >= r:
                return candidate
        return candidates[-1][0]


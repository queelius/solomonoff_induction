import random

class MarkovChain:
    def __init__(self, order):
        self.order = order

        # {
        #   '1+2=' : {
        #       '3': 10,
        #       '4': 1
        #   }
        # }
        self.model = {}

    def train(self, data):
        print("training on data with order", self.order)
        for i in range(len(data)):
            tokens = data[i]
            print(f'tokens: {tokens}')
            m = len(tokens)
            for j in range(m):
                for k in range(self.order):
                    if j+k <= m:
                        prev_tokens = tokens[j:j+k]
                        next_token = tokens[j+k]
                        print(f'{prev_tokens} => {next_token}')
                        #self.model[prev_tokens][next_token] += 1

    def next_token(self, state):
        candidates = list(self.model[state].items())
        total_count = sum(count for _, count in candidates)
        r = random.uniform(0, total_count)
        s = 0
        for candidate, count in candidates:
            s += count
            if s >= r:
                return candidate
        return candidates[-1][0]

    def generate(self, state, max_tokens = 128, stop_token='.'):
        print(f'starting state: {state}')
        if len(state) >= self.order:
            state = state[len(state) - self.order:]
            print(f'truncated state: {state}')

        output = []
        for i in range(max_tokens):
            token = self.next_token(state)
            if token == stop_token:
                break
            output.append(token)
            state = state + token
            if len(state) >= self.order:
                # truncate the state to the last n tokens
                state = state[len(state) - self.order:]

        return ''.join(output)

    

# new class that inherits from MarkovChain as a bit sequence Markov chain
class BitSequenceMarkovChain(MarkovChain):

    def __init__(self, transition_matrix, states=None):
        self.transition_matrix = np.array(transition_matrix)
        self.states = states if states else list(range(len(transition_matrix)))

    # pdf of a sequence
    def pdf(self, bit_sequence):
        """
        Calculate the probability of a sequence of bits
        """
        p = 1
        # take three bits at a time
        for i in range(len(bit_sequence)-3):
            current_state = bit_sequence[i:i+3]
            next_state = bit_sequence[i+1:i+4]
            # get the index of the current state
            current_state_index = self.states.index(current_state)
            # get the index of the next state
            next_state_index = self.states.index(next_state)
            # multiply the pdf by the transition probability
            p *= self.transition_matrix[current_state, next_state]
        return p

 
1
# Example usage
states = ['000', '001', '010', '011', '100', '101', '110', '111']

# Create a vector of 8 x 2 matrix
indices = np.zeros((8, 2), dtype=int)
for i in range(8):
    indices[i, :] = [2*i % 8, (2*i+1) % 8]

T_max_entropy = np.array([
   # 000  001  010  011  100  101  110  111
    [0.5, 0.5, 0,   0,   0,   0,   0,   0  ], # 000
    [0,   0,   0.5, 0.5, 0,   0,   0,   0  ], # 001
    [0,   0  , 0,   0  , 0.5, 0.5, 0,   0  ], # 010
    [0,   0,   0,   0,   0  , 0,   0.5, 0.5], # 011
    [0.5, 0.5, 0,   0,   0,   0,   0,   0  ], # 100
    [0,   0,   0.5, 0.5, 0,   0,   0,   0  ], # 101
    [0,   0,   0,   0,   0.5, 0.5, 0,   0  ], # 110
    [0,   0,   0,   0,   0,   0,   0.5, 0.5], # 111
])


T_min_entropy = np.array([
   # 000  001  010  011  100  101  110  111
    [0,   1,   0,   0,   0,   0,   0,   0  ], # 000
    [0,   0,   1,   0,   0,   0,   0,   0  ], # 001
    [0,   0,   0,   0  , 0,   1,   0,   0  ], # 010
    [0,   0,   0,   0,   0  , 0,   0,   1  ], # 011
    [1,   0,   0,   0,   0,   0,   0,   0  ], # 100
    [0,   0,   0,   1  , 0,   0,   0,   0  ], # 101
    [0,   0,   0,   0,   1,   0,   0,   0  ], # 110
    [0,   0,   0,   0,   0,   0,   1,   0  ], # 111
])


# create a list of transition matrices
np.set_printoptions(precision=2)
print("Transition matrix for max entropy:")
print(T_max_entropy)
# calculate the entropy rate, KC proxy
ent_rate_max_entropy = entropy_rate(T_max_entropy)
kc_max_entorpy = kc_proxy(ent_rate_max_entropy)
print("Entropy rate DGP:", ent_rate_max_entropy)
print("KC proxy:", kc_max_entorpy)


print("Transition matrix for complete min entropy:")
print(T_min_entropy)
# calculate the entropy rate, KC proxy
ent_rate_min_entropy = entropy_rate(T_min_entropy)
kc_min_entorpy = kc_proxy(ent_rate_min_entropy)
print("Entropy rate DGP:", ent_rate_min_entropy)
print("KC proxy:", kc_min_entorpy)

Ts = [T_max_entropy, T_min_entropy]

for i in range(1, 10):
    # create an 8x8 matrix of zeros
    T = np.zeros((8, 8))
    # for each row, randomly choose two indices and set them to
    # two random positive integers, then normalize the row

    for i in range(8):
        T[i,indices[i,0]] = np.random.randint(1, 100, size=1)
        T[i,indices[i,1]] = np.random.randint(1, 100, size=1)
        T[i] = T[i] / T[i].sum()

    # add the transition matrix to the list
    Ts.append(T)
    
    print("Transition matrix:")
    print(T)
    # calculate the entropy rate, KC proxy, and universal prior
    ent_rate = entropy_rate(T)
    kc = kc_proxy(ent_rate)
    print("Entropy rate:", ent_rate)
    print("KC proxy:", kc)
    print("")


T_dgp = Ts[3]

dgp = BitSequenceMarkovChain(states, T_dgp)
stat_dist = stationary_distribution(T_dgp)
print("Stationary distribution:", stat_dist)

# sample from the stationary distribution to get the
# initial state of the Markov chain
current_state = np.random.choice(states, p=stat_dist)
sequence = current_state
print(current_state, end='')
N = 100

# sample N times for a total observation of N+3 bits

for i in range(N):
    current_state = dgp.sample(current_state,1)[0]
    # print the last character of the current state,
    # which signifies the next bit in the sequence
    # don't print a newline though
    sequence += current_state[-1]
    print(current_state[-1], end='')
    

#print("PDF of sequence:", dgp.pdf(sequence))

#universal_prior = normalize_kc_proxies(kc1)
#print("Universal prior:", universal_prior)

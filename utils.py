import numpy as np
import numpy as np
from scipy.sparse import lil_matrix
import random

def stationary_distribution(transition_matrix):
    """
    Calculate the stationary distribution of a Markov chain given its transition matrix.
    """
    eigvals, eigvecs = np.linalg.eig(transition_matrix.T)
    stationary = eigvecs[:, np.isclose(eigvals, 1)].real.squeeze()
    stationary /= np.sum(stationary)
    return stationary

def entropy_rate(transition_matrix):
    """
    Calculate the entropy rate of a Markov chain given its transition matrix.
    """
    stationary_probs = stationary_distribution(transition_matrix)
    entropy = -np.sum(transition_matrix * np.log2(transition_matrix + 1e-9), axis=1)  # Add small constant to avoid log(0)
    return np.sum(stationary_probs * entropy)

def kc_proxy(entropy_rate, scaling_factor=1, constant=1):
    """
    Map the entropy rate to a proxy for the Kolmogorov complexity (KC).
    """
    return scaling_factor * (entropy_rate + constant)

def normalize_kc_proxies(kc_proxies):
    """
    Normalize the KC proxies to obtain the universal prior.
    """
    total = np.sum(kc_proxies)
    return kc_proxies / total

def generate_transition_matrix(order, deterministic_ratio=0.5):
    num_states = 2**order
    P = lil_matrix((num_states, num_states), dtype=np.float32)

    for state in range(num_states):
        binary_state = format(state, f'0{order}b')
        next_binary_states = [binary_state[1:] + '0', binary_state[1:] + '1']
        next_states = [int(next_binary_state, 2) for next_binary_state in next_binary_states]

        # Assign deterministic transition probabilities
        if random.random() < deterministic_ratio:
            P[state, next_states[0]] = 1.0
        else:
            P[state, next_states[0]] = random.random()
            P[state, next_states[1]] = 1 - P[state, next_states[0]]

    return P

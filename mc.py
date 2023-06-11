import numpy as np
import utils

class MarkovChain:
    def __init__(self, P, states=None):
        self.P = P
        self.states = states if states else list(range(len(P)))

    def sample(self, state, num_samples=1):
        """
        Sample the next state(s) from the Markov chain given the current state.
        """
        state_index = self.states.index(state)
        next_states = np.random.choice(self.states, size=num_samples, p=self.P[state_index])
        return next_states
    
    def entropy_rate(self):
        """
        Calculate the entropy rate of the Markov chain.
        """
        return utils.entropy_rate(self.P)
    
    def kc_proxy(self, scaling_factor=1, constant=1):
        """
        Calculate the KC proxy of the Markov chain.
        """
        return utils.kc_proxy(self.entropy_rate(), scaling_factor, constant)
    
    def stationary_distribution(self):
        """
        Calculate the stationary distribution of the Markov chain.
        """
        return utils.stationary_distribution(self.P)
    
    def __repr__(self):
        return f"MarkovChain({self.P}, {self.states})"
    
    def __str__(self):
        return self.__repr__()

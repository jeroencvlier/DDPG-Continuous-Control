import copy
import numpy as np
import random
class OrnsteinUhlenbeckNoise:
    '''The Ornstein-Uhlenbeck process to apply noise to action state for exploration'''
    def __init__(self,num_agents, action_size,mu = 0.0, theta=0.15, sigma=0.08 , seed = 432):
        '''Initialize parameters and noise process.'''
        self.num_agents = num_agents
        self.action_size = action_size
        self.mu = np.zeros((num_agents, action_size)) * mu
        self.theta = theta
        self.sigma = sigma
        self.seed = random.seed(seed)
        self.reset()

    def reset(self):
        '''Reset the internal state'''
        self.state = copy.copy(self.mu)

    def sample(self):
        '''Update internal state and return noise sample'''
        self.state += self.theta * (self.mu - self.state) + self.sigma * \
                      (np.random.uniform(0,1,[self.num_agents,self.action_size])-0.5)
        return self.state

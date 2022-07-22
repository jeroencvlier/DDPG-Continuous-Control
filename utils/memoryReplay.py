from collections import deque
import torch
import numpy as np
import random
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class MemoryReplay:
    '''Defines the memory replay of stored samples.
    memory_size (int) : maximum size of buffer
    replay_size (int) : size of each training batch
    seed        (int) : random seed
    '''
    def __init__(self, memory_size, replay_size, seed=123):
        self.memory = deque(maxlen=memory_size)  
        self.replay_size = replay_size
        self.seed = random.seed(seed)
    
    def add(self, state, action, reward, next_state, done):
        '''Store samples to memory
        state      ([float]) : The current state space of the givern envirnment
        action         (int) : The stochastic or predicted action for the current state space
        reward         (int) : The reward recieved for that action
        next_state ([float]) : The next state space of the givern envirnment after an action has been taken
        done          (bool) : Whether the envirnment has been completed or not
        '''
        if torch.is_tensor(state): state = state.detach().numpy()
        if torch.is_tensor(action): action = action.detach().numpy()
        if torch.is_tensor(reward): reward = reward.detach().numpy()
        if torch.is_tensor(next_state): next_state = next_state.detach().numpy()
        if torch.is_tensor(state): done = done.detach().numpy()
        
        self.memory.append({"state":state, "action":np.array(action), "reward":reward, "next_state":next_state, "done":done})
    
    def sample(self):
        '''Sample experiences from memory.'''
        experiences = random.sample(self.memory, k=self.replay_size)
        
        states = torch.FloatTensor(np.array([e['state'] for e in experiences])).to(device)
        actions = torch.FloatTensor(np.array([e['action'] for e in experiences])).to(device)
        rewards = torch.FloatTensor(np.array([e['reward'] for e in experiences])).unsqueeze(1).to(device)
        next_states = torch.FloatTensor(np.array([e['next_state'] for e in experiences])).to(device)
        dones = torch.FloatTensor(np.array([float(e['done']) for e in experiences])).unsqueeze(1).to(device)
  
        return (states, actions, rewards, next_states, dones)

    def __len__(self):
        """Return the current size of internal memory."""
        return len(self.memory)

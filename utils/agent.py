# standard modules
import ujson
import random
import numpy as np
from IPython.display import clear_output

# agent libraries
from utils.actorCritic import ActorPolicy, CriticPolicy
from utils.noise import OrnsteinUhlenbeckNoise
from utils.memoryReplay import MemoryReplay

# Plotting Modules
import matplotlib.pyplot as plt

# pytorch
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

class Agent:
    '''Defines the agent that interacts and learns with the environment'''
    def __init__(self,num_agents,state_size,action_size, memory_size = 500000, replay_size = 500, gamma = 0.95, tau=0.01, update_frequency = 20, learn_steps = 25, lr_actor = 0.0001, lr_critic = 0.001, seed = 333, print_every = 5):
        # Preset variables for learning
        self.tau = tau
        self.gamma = gamma
        self.lr_actor = lr_actor
        self.lr_critic = lr_critic
        
        self.memory_size = memory_size
        self.replay_size = replay_size
        self.update_frequency = update_frequency
        self.learn_steps = learn_steps
        self.state_size = state_size
        self.action_size = action_size
        self.num_agents = num_agents
        self.seed = random.seed(seed)
        
        self.msgs = []
        self.print_every = print_every
        
        # initialize critic network Q(s,a|θQ) and actor µ(s|θµ) with weights θQ and θµ
        self.actor = ActorPolicy(state_size,action_size)
        self.critic = CriticPolicy(state_size,action_size)

        # initiate optimizer
        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=self.lr_actor)
        self.critic_optimizer = optim.Adam(self.critic.parameters(), lr=self.lr_critic)

        # Initialize target network Q and µ: θQ'← θQ, θµ'← θµ
        self.actor_target = ActorPolicy(self.state_size,self.action_size)
        self.critic_target = CriticPolicy(self.state_size,self.action_size)

        # copy parameters state dictionary
        self.actor_target.load_state_dict(self.actor.state_dict())
        self.critic_target.load_state_dict(self.critic.state_dict())

        # instantiate memory replay
        self.memory = MemoryReplay(memory_size, replay_size, seed)

        # Initialize time step (for updating every update_frequency steps)
        self.freq_update = 0
        
        # Initate noise
        self.noise = OrnsteinUhlenbeckNoise(num_agents, action_size, seed = seed)
        
    def soft_update(self, target_net,local_net,tau):
        '''Soft update: θ_target = τ * θ_local + (1 - τ) * θ_target
        target_net (pytorch)
        local_net
        tau            (float) : Soft update parameter
        

        '''
        for target_param, local_param in zip(target_net.parameters(), local_net.parameters()):
            target_param.data.copy_(tau*local_param.data + (1.0-tau)*target_param.data)
        return target_net
    
    def act(self, env, brain_name, state, add_noise = True):
        '''Agent takes an action givern the state and returns a reward. 
        When the freq_update parameter is met then the agent will learn
        
        add_noise (Bool) : Adds noise to the action parameter
        '''
        self.actor.eval()
        with torch.no_grad():
            action = self.actor(state).cpu().data.numpy()
        self.actor.train()
        
        if add_noise == True:
            action += self.noise.sample()
            # clip after noise
            action = action.clip(-1,1)    
            
        env_info = env.step(action)[brain_name]
        done = env_info.local_done
        next_state = env_info.vector_observations
        reward = env_info.rewards
        
        # Store replay buffer
        for s_,a_,r_,ns_,d_ in zip(state, action, reward, next_state, done):
            self.memory.add(s_,a_,r_,ns_,d_)
            
        self.freq_update += 1
        if (len(self.memory) >= self.replay_size) and (self.freq_update%self.update_frequency==0):
            self.learn()
                    
        return reward, next_state, done
        
    def learn(self):
        '''Updates the networks after every ith step as defined by the update_frequency parameter'''
        for _ in range(self.learn_steps):
            # sample from replay
            s, a, r, ns, d = self.memory.sample()

            # critic loss optimizer
            na = self.actor_target(ns)
            q_target_next = self.critic_target(ns, na).detach() ## <<< Detach???

            q_target = r + (self.gamma * (1-d) * q_target_next) 
            q = self.critic(s, a)
            critic_loss = F.mse_loss(q, q_target)
            self.critic_optimizer.zero_grad()
            critic_loss.backward()
            # gradient clipping
            nn.utils.clip_grad_norm_(self.critic.parameters(), 1)
            self.critic_optimizer.step()

            # actor loss optimizer
            a = self.actor(s)
            q = self.critic(s, a)
            actor_loss = -q.mean()
            self.actor_optimizer.zero_grad()
            actor_loss.backward()
            self.actor_optimizer.step()

            # soft update
            self.critic_target = self.soft_update(self.critic_target , self.critic, self.tau)
            self.actor_target = self.soft_update(self.actor_target , self.actor, self.tau)
        return
    
    def plotter(self, scores, deque_length = 100, plot_graph = True ,save_plot = False , target_score = 30, solved = False):
        '''Plots the score
        scores           ([float]) : List of all the final scores
        deque_length (Int/[float]) : Length of score deque or score score deque to calculate deque length
        plot_graph          (Bool) : Displays score graph
        save_plot           (Bool) : Saves the plot to a .png file
        target_score         (Int) : Target score for the Network
        solved              (Bool) : Defines if evvironment is solved. If True, final score printed.
        '''    
        if isinstance(deque_length,int) == False:
            deque_length = len(deque_length)
            
        msg = 'Episode {}\tAverage Scores: {:.2f}'.format(len(scores), np.mean(scores[-deque_length:]))
        self.msgs.append(msg)
        
        # clear output and print scores
        clear_output()
        for m in self.msgs: 
            print(m)
            
        if solved == True:
            print('\nEnvironment solved!\tAverage Score: {:.2f}'.format(len(scores)-100, np.mean(scores[-100:])))

        # Score Plot
        plt.figure(figsize=(8,5))
        plt.plot([*range(1,len(scores)+1)],scores,label='Score')

        average_window = []
        for w in range(1,deque_length+1):
            average_window.append(np.mean(scores[:w]))

        plt.plot([*range(1,len(scores)+1)],average_window,color='red',label=f'Average Score')
        plt.plot([*range(1,len(scores)+1)],[target_score for i in range(len(scores))],color='black',label='Target Score')
        plt.title(f'Training Graph for {self.num_agents} agents')
        plt.ylabel('Score')
        plt.xlabel('Episode')
        plt.grid()
        plt.legend()

        # save plot
        if save_plot == True:
            plt.savefig('Images/TainedNetworkScores.png')
        # Display    
        plt.show()
        return 

    def save_checkpoint(self):
        '''Saves the trained model'''
        # Save Model
        torch.save(self.actor.state_dict(), 'TrainedModel/DDPG_Actor.pth')
        torch.save(self.critic.state_dict(), 'TrainedModel/DDPG_Critic.pth')
        # Save Model Network Structures
        ujson.dump({"hidden_layers":self.actor.hidden},open('TrainedModel/DDPG_Actor_Network.json','w'))
        ujson.dump({"hidden_layers":self.critic.hidden},open('TrainedModel/DDPG_Critic_Network.json','w'))

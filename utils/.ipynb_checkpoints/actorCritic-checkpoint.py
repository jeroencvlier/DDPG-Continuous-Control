import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class ActorPolicy(nn.Module):
    def __init__(self,state_size,action_size,hidden=[256,128]):
        super().__init__()
        self.hidden = hidden
        layerlist = []
        layerlist.append(nn.Linear(state_size, hidden[0]))
        layerlist.append(nn.BatchNorm1d(hidden[0]))
        layerlist.append(nn.ReLU(inplace=True))
        layerlist.append(nn.Linear(hidden[0], hidden[1]))
        layerlist.append(nn.ReLU(inplace=True))
        layerlist.append(nn.Linear(hidden[1], action_size))
        layerlist.append(nn.Tanh())
        self.sequence = nn.Sequential(*layerlist)
    
    def forward(self, state):     
        x = np.array(state)
        x = self.sequence(torch.FloatTensor(x).to(device))
        return x
    
class CriticPolicy(nn.Module):
    def __init__(self,state_size,action_size,hidden=[256,128]):
        super().__init__()
        self.hidden = hidden
        input_size = state_size
        outout_size = 1
        layerlist1 = []
        layerlist1.append(nn.Linear(input_size, hidden[0]))
        layerlist1.append(nn.BatchNorm1d(hidden[0]))
        layerlist1.append(nn.ReLU(inplace=True))
        self.sequence1 = nn.Sequential(*layerlist1)
        # insert action space from actor into neural network here
        layerlist2 = []
        layerlist2.append(nn.Linear(hidden[0]+action_size, hidden[1]))
        layerlist2.append(nn.ReLU(inplace=True))
        layerlist2.append(nn.Linear(hidden[1], outout_size))
        self.sequence2 = nn.Sequential(*layerlist2)
    
    def forward(self, state, action):
        x = torch.FloatTensor(state)
        x = self.sequence1(x)
        x = torch.cat((x,action), dim=1)
        x = self.sequence2(x)
        return x

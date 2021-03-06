import numpy as np
import torch
import torchvision
from torch import nn
from torch.autograd import Variable
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from torch.autograd import Variable
import torch.nn.functional as F
from RestNetBlocks import ResNetLayer, ResNetBottleNeckBlock
from Parameters import Parameters
"""
class ConvBlock(nn.Module):
    def __init__(self):
        super(ConvBlock, self).__init__()
        self.conv = nn.Conv2d(1, kernel_size = (3, 3), padding='same')
        self.act = nn.ReLU()

    def forward(self, x):
        return self.act(self.conv(x)+x)
"""

class DiscreteActorCritic(nn.Module):
    
    def __init__(self, lr, input_dims, nb_blocks):
        super(ActorCritic, self).__init__()
        self.nb_blocks = nb_blocks

        self.input_dims = input_dims #input_dims is the number of cells in the f_map input, cell_nb**2
        self.Para = Parameters()
        
        blocks = []
         
        hid_sz = 15
        blocks.append(
                nn.Conv3d(1, hid_sz, (3, 3, 3), padding=1)
            )
        blocks.append(
                nn.Conv3d(hid_sz, hid_sz, (3, 3, 3), padding=1)
            )
        blocks.append(
                nn.Conv3d(hid_sz, 1, (3, 3, 3), padding=1)
            )
        self.Bs = nn.ModuleList(blocks)

        #self._3to2d = nn.Conv2d(self.Para.f_map_depth, 1, (1,1))
        self.po = ... #nn.Conv2d(1, 1, (3, 3), padding=1)
        self.val = nn.Linear(self.input_dims, 1)

        self.optimizer = torch.optim.Adam(self.parameters(), lr=lr)
        
        

    def forward(self, f_map):
        x = f_map.reshape([1, 1, self.Para.f_map_depth, self.nb_blocks, self.nb_blocks])
        #print(f"x shape as input : {x.shape}")
        for ix, l in enumerate(self.Bs):
            x = l(x)
            #print(f"x shape after block {ix} : {x.shape}")
        x = self._3to2d(x.view([1, self.Para.f_map_depth, self.nb_blocks, self.nb_blocks]))
        sigma = F.sigmoid(self.sig(x))
        mu = F.sigmoid(self.mu(x))
        #print(f"shapes sigma {sigma.shape}, mu {mu.shape}, x0 {x.shape}, x1 {x.view([1, self.input_dims]).shape}")
        val = self.val(x.view([1, self.input_dims]))
        #print(f"mu {mu} \nsigma {sigma}")
        return (mu, sigma), val 


class ActorCritic(nn.Module):
    
    def __init__(self, lr, input_dims, nb_blocks):
        super(ActorCritic, self).__init__()
        self.nb_blocks = nb_blocks

        self.input_dims = input_dims #input_dims is the number of cells in the f_map input, cell_nb**2
        self.Para = Parameters()
        
        blocks = []
         
        hid_sz = 15
        blocks.append(
                nn.Conv3d(1, hid_sz, (3, 3, 3), padding=1)
            )
        blocks.append(
                nn.Conv3d(hid_sz, hid_sz, (3, 3, 3), padding=1)
            )
        blocks.append(
                nn.Conv3d(hid_sz, 1, (3, 3, 3), padding=1)
            )
        self.Bs = nn.ModuleList(blocks)

        self._3to2d = nn.Conv2d(self.Para.f_map_depth, 1, (1,1))
        self.sig = nn.Conv2d(1, 1, (3, 3), padding=1)
        self.mu = nn.Conv2d(1, 1, (3, 3), padding=1)
        self.val = nn.Linear(self.input_dims, 1)

        self.optimizer = torch.optim.Adam(self.parameters(), lr=lr)
        
        

    def forward(self, f_map):
        x = f_map.reshape([1, 1, self.Para.f_map_depth, self.nb_blocks, self.nb_blocks])
        #print(f"x shape as input : {x.shape}")
        for ix, l in enumerate(self.Bs):
            x = l(x)
            #print(f"x shape after block {ix} : {x.shape}")
        x = self._3to2d(x.view([1, self.Para.f_map_depth, self.nb_blocks, self.nb_blocks]))
        sigma = F.sigmoid(self.sig(x))
        mu = F.sigmoid(self.mu(x))
        #print(f"shapes sigma {sigma.shape}, mu {mu.shape}, x0 {x.shape}, x1 {x.view([1, self.input_dims]).shape}")
        val = self.val(x.view([1, self.input_dims]))
        #print(f"mu {mu} \nsigma {sigma}")
        return (mu, sigma), val 



class Dataset(Dataset):
    'Characterizes a dataset for PyTorch'

    def __init__(self, data, labels):
        'Initialization'

        self.labels = labels
        self.data = data

    def __len__(self):
        'Denotes the total number of samples'
        return len(self.data)

    def __getitem__(self, index):
        'Generates one sample of data'
        # Select sample

        # Load data and get label
        X = self.data.iloc[[index]].values
        y = self.labels.iloc[[index]].values
        return X, y

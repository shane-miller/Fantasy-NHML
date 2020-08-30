import torch.nn.functional as F
import torch.utils.data as data
import torch.optim as optim
import torch.cuda as cuda
import torch.nn as nn
import torch

from sklearn.model_selection import train_test_split
from tqdm import tqdm
import numpy as np

import importlib
import time

import argparse


##### Argument Parsing ######
# Get values from the command line.
parser = argparse.ArgumentParser(description='Fantasy NHML')

parser.add_argument('--epochs',        type=int,   default=50,       help='Number of epochs')
parser.add_argument('--batch_size',    type=int,   default=100,      help='Batch Size')
parser.add_argument('--lr',            type=float, default=0.01,     help='Initial learning rate')
parser.add_argument('--momentum',      type=float, default=0.4,      help='Momentum for network')
parser.add_argument('--weight_decay',  type=float, default=0.25,     help='Weight decay for network')
parser.add_argument('--name',          type=str,   default="result", help='Name to name all the exported files of the network')
parser.add_argument('--normalize',     type=bool,  default=False,    help='Whether to use normalized data')
parser.add_argument('--lr_decay',      type=float, default=1.0,      help='LR decay')
parser.add_argument('--lr_step_size',  type=float, default=10,       help='LR decay step size')

args = parser.parse_args()

weight_decay = args.weight_decay
lr_step_size = args.lr_step_size
batch_size = args.batch_size
normalize = args.normalize
momentum = args.momentum
lr_decay = args.lr_decay
epochs = args.epochs
lr = args.lr


##### Confirm Cuda Is Available #####
print("Cuda Available:", cuda.is_available(), '\n')


##### Load Data #####
current_file_path = pathlib.Path(__file__).parent.absolute()
path = current_file_path.parents[0] / 'Data' / 'Centers'

data = np.load(path / 'player_data.npy', allow_pickle=True)
points = np.load(path / 'fantasy_points_data.npy', allow_pickle=True)


##### Dataset Definition #####
class PlayerDataset(data.Dataset):
    def __init__(self, stats, points):
        self.stats = stats
        self.points = points

    def __len__(self):
        return len(self.stats)

    def __getitem__(self, index):
        stat_set = self.stats[index]
        fantasy_points = self.points[index]

        return stat_set, fantasy_points


##### Dataset Initialization #####
data_train, data_test, points_train, points_test = train_test_split(data, points, test_size=0.3)
data_train, data_val, points_train, points_val = train_test_split(data_train, points_train, test_size=0.285)

train_all = PlayerDataset(data_train, points_train)
test_all = PlayerDataset(data_train, points_train)
val_all = PlayerDataset(data_val, points_val)

train_loader = data.DataLoader(train_all, batch_size=64, shuffle=True)
test_loader = data.DataLoader(test_all, batch_size=64, shuffle=True)
val_loader = data.DataLoader(val_all, batch_size=64, shuffle=True)


##### Neural Network Definition #####
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        self.fc1 = nn.Linear(190, 256)
        self.fc2 = nn.Linear(256, 64)
        self.fc3 = nn.Linear(64, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)




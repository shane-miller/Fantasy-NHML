import torch.nn.functional as F
import torch.utils.data as data
import torch.optim as optim
import torch.cuda as cuda
import torch.nn as nn
import torch

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
parser.add_argument('--dataset_split', type=float, default=0.80,     help='Percentage split of dataset')
parser.add_argument('--lr',            type=float, default=0.01,     help='Initial learning rate')
parser.add_argument('--momentum',      type=float, default=0.4,      help='Momentum for network')
parser.add_argument('--weight_decay',  type=float, default=0.25,     help='Weight decay for network')
parser.add_argument('--name',          type=str,   default="result", help='Name to name all the exported files of the network')
parser.add_argument('--normalize',     type=bool,  default=False,    help='Whether to use normalized data')
parser.add_argument('--lr_decay',      type=float, default=1.0,      help='LR decay')
parser.add_argument('--lr_step_size',  type=float, default=10,       help='LR decay step size')

args = parser.parse_args()

split_percent = args.dataset_split
weight_decay = args.weight_decay
lr_step_size = args.lr_step_size
batch_size = args.batch_size
normalize = args.normalize
use_seed = args.use_seed
momentum = args.momentum
lr_decay = args.lr_decay
epochs = args.epochs
seed = args.seed
name = args.name
lr = args.lr

##### Confirm Cuda Is Available #####
print("Cuda Available:", cuda.is_available(), '\n')


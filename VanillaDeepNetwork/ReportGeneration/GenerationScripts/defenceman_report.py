import torch.nn.functional as F
import torch.utils.data as data
import torch.cuda as cuda
import torch.nn as nn
import torch

import numpy as np
import pathlib
import math
import os


current_file_path = pathlib.Path(__file__).parent.absolute()
path = current_file_path.parents[0].parents[0].parents[0] / 'Data' / 'PlayerData'

stats = np.load(path / 'most_recent_season_data.npy', allow_pickle=True)
stats = stats[2]
names = np.load(path / 'most_recent_season_data_names.npy', allow_pickle=True)
names = names[2]


##### Neural Network Definition #####
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        self.fc1 = nn.Linear(190, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 64)
        self.fc4 = nn.Linear(64, 32)
        self.fc5 = nn.Linear(32, 16)
        self.fc6 = nn.Linear(16, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))
        x = F.relu(self.fc5(x))
        x = self.fc6(x)

        return x


##### Initialize Network #####
net = Net()

if cuda.is_available():
    net = net.cuda()

state_dict = torch.load(current_file_path.parents[0].parents[0] / 'ModelWeights' / 'Defenceman_Weights.pth')
net.load_state_dict(state_dict)


##### Get Data For Each Player #####
predictions = []
net.eval()
for i, player in enumerate(stats, 0):
    player = torch.FloatTensor(player)
    if cuda.is_available():
        player = player.cuda()

    output = net(player)

    predictions.append((names[i][0], output.data.cpu().numpy()[0]))

file = None
try:
    file = open(current_file_path.parents[0] / 'Reports' / 'defenceman_report.txt', 'x')
except:
    os.remove(current_file_path.parents[0] / 'Reports' / 'defenceman_report.txt')
    file = open(current_file_path.parents[0] / 'Reports' / 'defenceman_report.txt', 'x')

max_name_len = max(len(player[0]) for player in predictions)
name_str = 'Player Name'
file.write(f'{name_str:>{max_name_len}}' + ' | ' + 'Predicted Fantasy Points' + '\n\n')

predictions.sort(key = lambda x: -x[1])
for player in predictions:
    file.write(f'{player[0]:>{max_name_len}}' + ' | ' + str(math.ceil(player[1])) + '\n')

file.close()


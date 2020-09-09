import torch.nn.functional as F
import torch.utils.data as data
import torch.optim as optim
import torch.cuda as cuda
import torch.nn as nn
import torch

from sklearn.model_selection import train_test_split
import numpy as np
import pathlib
import time


##### Confirm Cuda Is Available #####
print('Cuda Available:', cuda.is_available(), '\n')


##### Load Data #####
current_file_path = pathlib.Path(__file__).parent.absolute()
path = current_file_path.parents[0].parents[0] / 'Data' / 'PlayerData' / 'Goalies'

stats = np.load(path / 'player_data.npy', allow_pickle=True)
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
data_train, data_test, points_train, points_test = train_test_split(stats, points, test_size=0.3)
data_train, data_val, points_train, points_val = train_test_split(data_train, points_train, test_size=0.285)

train_all = PlayerDataset(data_train, points_train)
test_all = PlayerDataset(data_train, points_train)
val_all = PlayerDataset(data_val, points_val)

train_loader = data.DataLoader(train_all, batch_size=100, shuffle=True)
test_loader = data.DataLoader(test_all, batch_size=100, shuffle=True)
val_loader = data.DataLoader(val_all, batch_size=100, shuffle=True)


##### Neural Network Definition #####
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        self.fc1 = nn.Linear(38, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 16)
        self.fc4 = nn.Linear(16, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)

        return x


##### Initialize Network #####
net = Net()

if cuda.is_available():
    net = net.cuda()

criterion = nn.MSELoss()
optimizer = optim.SGD(net.parameters(), lr=0.000000005, momentum=0.00001, weight_decay=0)


##### Training Loop #####
t0 = time.time()

print('Beginning Training:')
for epoch in range(1000):
    net.train()
    running_loss_train = []
    for i, data in enumerate(train_loader, 0):
        stats, points = data

        stats = stats.float()
        points = points.float()

        if cuda.is_available():
            stats = stats.cuda()
            points = points.cuda()

        optimizer.zero_grad()

        outputs = net(stats)
        outputs = torch.reshape(outputs, (-1,))

        loss = criterion(outputs, points)
        loss.backward()

        optimizer.step()

        running_loss_train.append(loss.item())

    avg_loss = np.mean(np.array([running_loss_train]))


    net.eval()
    running_loss_eval = []
    difference_array = []

    for i, data in enumerate(val_loader, 0):
        stats, points = data

        stats = stats.float()
        points = points.float()

        if cuda.is_available():
            stats = stats.cuda()
            points = points.cuda()

        outputs = net(stats)
        outputs = torch.reshape(outputs, (-1,))

        loss = criterion(outputs, points)
        running_loss_eval.append(loss.item())

        for j in range(0, len(outputs)):
            prediction = outputs[j]
            ground_truth = points[j]

            difference_array.append(np.absolute(ground_truth.cpu().detach().numpy() - prediction.cpu().detach().numpy()))

    eval_avg_loss = np.mean(np.array([running_loss_eval]))
    val_accuracy = np.average(difference_array)

    if epoch % 10 == 0:
        print('Epoch:', epoch,
              '\n         | Avg Loss:', avg_loss,
              '\n         | Eval Avg Loss:', eval_avg_loss,
              '\n         | Eval Avg Difference:', val_accuracy)

    if cuda.is_available():
        cuda.empty_cache()


##### Test Data Evaluation #####
net.eval()

running_loss_test = []
difference_array = []

for i, data in enumerate(val_loader, 0):
    stats, points = data

    stats = stats.float()
    points = points.float()

    if cuda.is_available():
        stats = stats.cuda()
        points = points.cuda()

    outputs = net(stats)
    outputs = torch.reshape(outputs, (-1,))

    loss = criterion(outputs, points)
    running_loss_test.append(loss.item())

    for j in range(0, len(outputs)):
        prediction = outputs[j]
        ground_truth = points[j]

        difference_array.append(np.absolute(ground_truth.cpu().detach().numpy() - prediction.cpu().detach().numpy()))

test_avg_loss = np.mean(np.array([running_loss_test]))
test_accuracy = np.average(difference_array)


##### Results #####
print('Test Loss =', test_avg_loss)
print('Test Avg Difference =', test_accuracy)
print('Time taken =', (time.time() - t0))


##### Save Weights #####
torch.save(net.state_dict(), current_file_path.parents[0] / 'ModelWeights' / 'Goalie_Weights.pth')

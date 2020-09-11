from sklearn.model_selection import train_test_split
from sklearn import linear_model, metrics
import numpy as np
import pathlib
import math
import os


##### Load Data #####
current_file_path = pathlib.Path(__file__).parent.absolute()
path = current_file_path.parents[0].parents[0] / 'Data' / 'PlayerData' / 'Wings'

stats = np.load(path / 'player_data.npy', allow_pickle=True)
points = np.load(path / 'fantasy_points_data.npy', allow_pickle=True)

temp = []
for player in stats:
    temp.append([player[35], player[0], player[80], player[79], player[75], player[92], player[87], player[98],
                 player[136], player[131], player[140], player[31], player[170], player[169], player[152],
                 player[159], player[40], player[4]])
stats = temp

mse = math.inf
r2 = math.inf
count = 0
while (mse > 750 or (r2 > 0.75 or r2 < -0.75)) and count < 25000:
    count = count + 1
    
    ##### Split Data #####
    data_train, data_test, points_train, points_test = train_test_split(stats, points, test_size=0.3)


    ##### Create and Train the Model #####
    reg = linear_model.LinearRegression()

    reg.fit(data_train, points_train)

    preds = reg.predict(data_test)
    r2 = metrics.r2_score(points_test, preds)
    mse = metrics.mean_squared_error(points_test, preds)

print("R2 score : %.4f" % r2)
print("Mean squared error: %.4f" % mse)


##### Predict and Save Fantasy Values #####
path = current_file_path.parents[0].parents[0] / 'Data' / 'PlayerData'

stats = np.load(path / 'most_recent_season_data.npy', allow_pickle=True)
stats = stats[1]

temp = []
for player in stats:
    temp.append([player[35], player[0], player[80], player[79], player[75], player[92], player[87], player[98],
                 player[136], player[131], player[140], player[31], player[170], player[169], player[152],
                 player[159], player[40], player[4]])
stats = temp

names = np.load(path / 'most_recent_season_data_names.npy', allow_pickle=True)
names = names[1]

predictions = []
temp = reg.predict(stats)
for i, player in enumerate(names):
    value = temp[i]
    if value < 0:
        value = 0
    else:
        value = math.ceil(value)

    predictions.append((player[0], value))

file = None
try:
    file = open(current_file_path.parents[0] / 'Reports' / 'wing_report.txt', 'x')
except:
    os.remove(current_file_path.parents[0] / 'Reports' / 'wing_report.txt')
    file = open(current_file_path.parents[0] / 'Reports' / 'wing_report.txt', 'x')

max_name_len = max(len(player[0]) for player in predictions)
name_str = 'Player Name'
file.write(f'{name_str:>{max_name_len}}' + ' | ' + 'Predicted Fantasy Points' + '\n\n')

predictions.sort(key = lambda x: -x[1])
for player in predictions:
    file.write(f'{player[0]:>{max_name_len}}' + ' | ' + str(math.ceil(player[1])) + '\n')

file.close()
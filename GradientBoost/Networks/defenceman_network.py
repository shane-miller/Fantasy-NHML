from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import metrics
import numpy as np
import pathlib
import math
import os


##### Load Data #####
current_file_path = pathlib.Path(__file__).parent.absolute()
path = current_file_path.parents[0].parents[0] / 'Data' / 'PlayerData' / 'Defencemen'

stats = np.load(path / 'player_data.npy', allow_pickle=True)
points = np.load(path / 'fantasy_points_data.npy', allow_pickle=True)


mse = 0
r2 = 0
count = 0
while r2 < 0.6 and count < 50:
    count = count + 1

    ##### Split Data #####
    data_train, data_test, points_train, points_test = train_test_split(stats, points, test_size=0.3)

    ##### Create and Train the Model #####
    reg = GradientBoostingRegressor(learning_rate=0.075, n_estimators=200, max_depth=4)
    reg.fit(data_train, points_train)

    preds = reg.predict(data_test)
    r2 = metrics.r2_score(points_test, preds)
    mse = metrics.mean_squared_error(points_test, preds)

print("R2 Score : %.4f" % r2)
print("Root Mean Squared Error: %.4f" % np.sqrt(mse))


##### Predict and Save Fantasy Values #####
path = current_file_path.parents[0].parents[0] / 'Data' / 'PlayerData'

stats = np.load(path / 'most_recent_season_data.npy', allow_pickle=True)
stats = stats[2]

names = np.load(path / 'most_recent_season_data_names.npy', allow_pickle=True)
names = names[2]

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

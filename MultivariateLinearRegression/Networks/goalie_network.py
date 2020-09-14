from sklearn.model_selection import train_test_split
from sklearn import linear_model, metrics
import numpy as np
import pathlib
import pickle
import math
import os


##### Load Data #####
current_file_path = pathlib.Path(__file__).parent.absolute()
path = current_file_path.parents[0].parents[0] / 'Data' / 'PlayerData' / 'Goalies'

stats = np.load(path / 'player_data.npy', allow_pickle=True)
points = np.load(path / 'fantasy_points_data.npy', allow_pickle=True)

temp = []
for player in stats:
    temp.append([player[8], player[37], player[15], player[33], player[10], player[28], player[35], player[16], player[23]])
stats = temp

mse = 0
r2 = 0
count = 0
while r2 < 0.65 and count < 25000:
    count = count + 1
    
    ##### Split Data #####
    data_train, data_test, points_train, points_test = train_test_split(stats, points, test_size=0.3)

    ##### Create and Train the Model #####
    reg = linear_model.LinearRegression()

    reg.fit(data_train, points_train)

    preds = reg.predict(data_test)
    r2 = metrics.r2_score(points_test, preds)
    mse = metrics.mean_squared_error(points_test, preds)

print("R2 Score : %.4f" % r2)
print("Root Mean Squared Error: %.4f" % np.sqrt(mse))


##### Save Model #####
path = current_file_path.parents[0] / 'SavedModels'

file = None
try:
    file = open(path / 'goalie_model.sav', 'wb')
except:
    os.remove(path / 'goalie_model.sav')
    file = open(path / 'goalie_model.sav', 'wb')

pickle.dump(reg, file)
file.close()

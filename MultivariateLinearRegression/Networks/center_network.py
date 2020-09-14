from sklearn.model_selection import train_test_split
from sklearn import linear_model, metrics
import numpy as np
import pathlib
import pickle
import math
import os


##### Load Data #####
current_file_path = pathlib.Path(__file__).parent.absolute()
path = current_file_path.parents[0].parents[0] / 'Data' / 'PlayerData' / 'Centers'

stats = np.load(path / 'player_data.npy', allow_pickle=True)
points = np.load(path / 'fantasy_points_data.npy', allow_pickle=True)

temp = []
for player in stats:
    temp.append([player[35], player[0], player[80], player[79], player[75], player[92], player[87], player[98],
                 player[136], player[131], player[140], player[31], player[170], player[169], player[152],
                 player[159], player[40], player[4]])
stats = temp

mse = 0
r2 = 0
count = 0
while r2 < 0.825 and count < 25000:
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
    file = open(path / 'center_model.sav', 'wb')
except:
    os.remove(path / 'center_model.sav')
    file = open(path / 'center_model.sav', 'wb')

pickle.dump(reg, file)
file.close()

from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn import metrics
from tqdm import tqdm
import numpy as np
import pathlib
import pickle
import math
import os


def main():
    ##### Load Data #####
    current_file_path = pathlib.Path(__file__).parent.absolute()
    path = current_file_path.parents[0].parents[0] / 'Data' / 'PlayerData' / 'Goalies'

    stats = np.load(path / 'player_data.npy', allow_pickle=True)
    points = np.load(path / 'fantasy_points_data.npy', allow_pickle=True)

    temp = []
    for player in stats:
        temp.append([player[8], player[37], player[15], player[33], player[10], player[28], player[35], player[16], player[23]])
    stats = temp

    mse = -math.inf
    r2 = -math.inf
    best_reg = None
    for i in tqdm(range(5000), desc='Generating Goalie Model'):
        ##### Split Data #####
        data_train, data_test, points_train, points_test = train_test_split(stats, points, test_size=0.3)

        ##### Create and Train the Model #####
        reg = ElasticNet(max_iter=1000000)
        reg.fit(data_train, points_train)

        preds = reg.predict(data_test)
        if metrics.r2_score(points_test, preds) > r2:
            best_reg = reg
            r2 = metrics.r2_score(points_test, preds)
            mse = metrics.mean_squared_error(points_test, preds)

    print("\tR2 Score : %.4f" % r2)
    print("\tRoot Mean Squared Error: %.4f" % np.sqrt(mse))


    ##### Save Model #####
    path = current_file_path.parents[0] / 'SavedModels'

    file = None
    try:
        file = open(path / 'goalie_model.sav', 'wb')
    except:
        os.remove(path / 'goalie_model.sav')
        file = open(path / 'goalie_model.sav', 'wb')

    pickle.dump(best_reg, file)
    file.close()


if __name__ == "__main__":
    main()

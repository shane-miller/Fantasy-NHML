from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
import numpy as np
import pathlib
import pickle

def main():
    print('Fitting Goalies:')

    ##### Load Data #####
    current_file_path = pathlib.Path(__file__).parent.absolute()
    path = current_file_path.parents[0].parents[0] / 'Data' / 'PlayerData' / 'Goalies'

    stats = np.load(path / 'player_data.npy', allow_pickle=True)
    points = np.load(path / 'fantasy_points_data.npy', allow_pickle=True)

    ##### Define Parameters for Grid Search #####
    parameters = {'learning_rate' : [0.01, 0.05, 0.075, 0.1, 0.125, 0.15, 0.25],
                  'n_estimators' : [50, 100, 150, 200, 250],
                  'tol' : [0.00001, 0.0001, 0.001],
                  'max_depth' : [None, 4, 8]}

    ##### Create and Train the Model Finding Best Parameters Using Grid Search #####
    reg = GradientBoostingRegressor()

    grid = GridSearchCV(estimator=reg, param_grid=parameters, scoring='r2', n_jobs=5, verbose=1)
    grid.fit(stats, points)

    print('Best R2 Score:', grid.best_score_)

    best_reg = grid.best_estimator_

    ##### Save Model #####
    path = current_file_path.parents[0] / 'SavedModels'

    file = open(path / 'goalie_model.sav', 'wb')

    pickle.dump(best_reg, file)
    file.close()

    print()


if __name__ == "__main__":
    main()

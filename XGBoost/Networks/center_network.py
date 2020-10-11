from sklearn.model_selection import GridSearchCV
from xgboost import XGBRegressor
import numpy as np
import pathlib
import pickle

def main():
    print('Fitting Centers:')

    ##### Load Data #####
    current_file_path = pathlib.Path(__file__).parent.absolute()
    path = current_file_path.parents[0].parents[0] / 'Data' / 'PlayerData' / 'Centers'

    stats = np.load(path / 'player_data.npy', allow_pickle=True)
    points = np.load(path / 'fantasy_points_data.npy', allow_pickle=True)

    ##### Define Parameters for Grid Search #####
    parameters = {'n_estimators' : [50, 100, 150, 200, 250],
                  'learning_rate' : [0.1, 0.25, 0.5, 0.75, 0.9],
                  'max_depth' : [3, 4, 5],
                  'objective' : ['reg:squarederror']}

    ##### Create and Train the Model Finding Best Parameters Using Grid Search #####
    reg = XGBRegressor()

    grid = GridSearchCV(estimator=reg, param_grid=parameters, scoring='r2', n_jobs=5, verbose=1)
    grid.fit(stats, points)

    print('Best R2 Score:', grid.best_score_)

    best_reg = grid.best_estimator_

    ##### Save Model #####
    path = current_file_path.parents[0] / 'SavedModels'

    file = open(path / 'center_model.sav', 'wb')

    pickle.dump(best_reg, file)
    file.close()

    print()
    

if __name__ == "__main__":
    main()

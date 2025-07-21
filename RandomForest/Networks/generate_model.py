from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import randint
import numpy as np
import pathlib
import pickle

def generate_model(position_str):
    print('Fitting ' + position_str.capitalize() + ':')

    ##### Load Data #####
    current_file_path = pathlib.Path(__file__).parent.absolute()
    path = current_file_path.parents[0].parents[0] / 'Data' / 'PlayerData' / position_str.capitalize()

    stats = np.load(path / 'player_data.npy', allow_pickle=True)
    points = np.load(path / 'fantasy_points_data.npy', allow_pickle=True)

    ##### Define Parameters for Grid Search #####
    parameters = {'n_estimators' : randint(low=25, high=350),
                  'criterion' : ['squared_error', 'absolute_error', 'friedman_mse'],
                  'max_depth' : randint(low=1, high=10)}

    ##### Create and Train the Model Finding Best Parameters Using Randomized Search #####
    reg = RandomForestRegressor()

    search = RandomizedSearchCV(estimator=reg, param_distributions=parameters, n_iter=50, scoring='r2', n_jobs=-1, verbose=1)
    search.fit(stats, points)

    print('Best R2 Score:', search.best_score_)

    best_reg = search.best_estimator_

    ##### Save Model #####
    path = current_file_path.parents[0] / 'SavedModels'

    file = open(path / (position_str + '_model.sav'), 'wb')

    pickle.dump(best_reg, file)
    file.close()

    print()

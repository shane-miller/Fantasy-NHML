from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from scipy.stats import uniform, randint
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
    parameters = {'base_estimator' : [DecisionTreeRegressor(max_depth=2), DecisionTreeRegressor(max_depth=3), DecisionTreeRegressor(max_depth=4), DecisionTreeRegressor(max_depth=5)],
                  'n_estimators' : randint(low=25, high=350),
                  'learning_rate' : uniform(loc=0.1, scale=1.4),
                  'loss' : ['linear', 'square', 'exponential']}

    ##### Create and Train the Model Finding Best Parameters Using Grid Search #####
    reg = AdaBoostRegressor()

    search = RandomizedSearchCV(estimator=reg, param_distributions=parameters, n_iter=150, scoring='r2', n_jobs=-1, verbose=1)
    search.fit(stats, points)

    print('Best R2 Score:', search.best_score_)

    best_reg = search.best_estimator_

    ##### Save Model #####
    path = current_file_path.parents[0] / 'SavedModels'

    file = open(path / (position_str + '_model.sav'), 'wb')

    pickle.dump(best_reg, file)
    file.close()

    print()

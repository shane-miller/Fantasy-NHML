from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import ElasticNet
from scipy.stats import uniform
import numpy as np
import pathlib
import pickle

def generate_model(position_str):
    print('Fitting ' + position_str.capitalize() +':')

    ##### Load Data #####
    current_file_path = pathlib.Path(__file__).parent.absolute()
    path = current_file_path.parents[0].parents[0] / 'Data' / 'PlayerData' / position_str.capitalize()

    stats = np.load(path / 'player_data.npy', allow_pickle=True)
    points = np.load(path / 'fantasy_points_data.npy', allow_pickle=True)

    ##### Define Parameters for Grid Search #####
    max_iter = 10000
    if(position_str == 'goalies') :
        max_iter = 1000000

    parameters = {'alpha' : uniform(loc=0.5, scale=1),
                  'l1_ratio' : uniform(loc=0.25, scale=0.5),
                  'normalize' : [False, True],
                  'max_iter' : [max_iter],
                  'tol' : uniform(loc=0.0001, scale=0.0099),
                  'selection' : ['cyclic', 'random']}

    ##### Create and Train the Model Finding Best Parameters Using Grid Search #####
    reg = ElasticNet()

    search = RandomizedSearchCV(estimator=reg, param_distributions=parameters, n_iter=200, scoring='r2', n_jobs=5, verbose=1)
    search.fit(stats, points)

    print('Best R2 Score:', search.best_score_)

    best_reg = search.best_estimator_

    ##### Save Model #####
    path = current_file_path.parents[0] / 'SavedModels'

    file = open(path / (position_str + '_model.sav'), 'wb')

    pickle.dump(best_reg, file)
    file.close()

    print()

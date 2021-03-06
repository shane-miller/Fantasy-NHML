from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
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
    parameters = {'normalize' : [False, True]}

    ##### Create and Train the Model #####
    reg = LinearRegression()

    grid = GridSearchCV(estimator=reg, param_grid=parameters, scoring='r2', n_jobs=-1, verbose=1)
    grid.fit(stats, points)

    print('Best R2 Score:', grid.best_score_)

    best_reg = grid.best_estimator_
    
    ##### Save Model #####
    path = current_file_path.parents[0] / 'SavedModels'

    file = open(path / (position_str + '_model.sav'), 'wb')

    pickle.dump(best_reg, file)
    file.close()

    print()

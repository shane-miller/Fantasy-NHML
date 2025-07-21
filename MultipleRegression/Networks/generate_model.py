from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
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


    ##### Create and Train the Model Using a Pipeline #####
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('reg', LinearRegression())
    ])
    pipeline.fit(stats, points)

    ##### Save Model #####
    path = current_file_path.parents[0] / 'SavedModels'
    file = open(path / (position_str + '_model.sav'), 'wb')
    pickle.dump(pipeline, file)
    file.close()
    print()

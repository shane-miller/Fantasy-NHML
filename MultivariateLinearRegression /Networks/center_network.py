from sklearn.model_selection import train_test_split
from sklearn import linear_model, metrics
import numpy as np

##### Load Data #####
current_file_path = pathlib.Path(__file__).parent.absolute()
path = current_file_path.parents[0].parents[0] / 'Data' / 'PlayerData' / 'Centers'

stats = np.load(path / 'player_data.npy', allow_pickle=True)
points = np.load(path / 'fantasy_points_data.npy', allow_pickle=True)


##### Split Data #####
data_train, data_test, points_train, points_test = train_test_split(stats, points, test_size=0.3)


##### Create and Train the Model #####
reg = linear_model.LinearRegression()

reg.fit(data_train, points_train)

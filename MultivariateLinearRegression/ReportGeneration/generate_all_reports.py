from sklearn import linear_model
import numpy as np
import pathlib
import pickle
import math
import os

##### SKATERS #####
def generate_skater_reports(position_str):
    index = None
    if position_str == 'center':
        index = 0
    elif position_str == 'wing':
        index = 1
    else:
        index = 2

    ##### Load Model #####
    current_file_path = pathlib.Path(__file__).parent.absolute()
    path = current_file_path.parents[0] / 'SavedModels'

    file = None
    try:
        file = open(path / (position_str + '_model.sav'), 'rb')
    except:
        raise Exception('Missing ' + position_str + '_model.sav')

    reg = pickle.load(file)


    ##### Predict and Save Fantasy Values #####
    path = current_file_path.parents[0].parents[0] / 'Data' / 'PlayerData'

    stats = np.load(path / 'most_recent_season_data.npy', allow_pickle=True)
    stats = stats[index]

    temp = []
    for player in stats:
        temp.append([player[35], player[0], player[80], player[79], player[75], player[92], player[87], player[98],
                     player[136], player[131], player[140], player[31], player[170], player[169], player[152],
                     player[159], player[40], player[4]])
    stats = temp

    names = np.load(path / 'most_recent_season_data_names.npy', allow_pickle=True)
    names = names[index]

    predictions = []
    temp = reg.predict(stats)
    for i, player in enumerate(names):
        value = temp[i]
        if value < 0:
            value = 0
        else:
            value = math.ceil(value)

        predictions.append((player[0], value))

    file = None
    filename = position_str + '_report.txt'
    try:
        file = open(current_file_path.parents[0] / 'Reports' / filename, 'x')
    except:
        os.remove(current_file_path.parents[0] / 'Reports' / filename)
        file = open(current_file_path.parents[0] / 'Reports' / filename, 'x')

    max_name_len = max(len(player[0]) for player in predictions)
    name_str = 'Player Name'
    file.write(f'{name_str:>{max_name_len}}' + ' | ' + 'Predicted Fantasy Points' + '\n\n')

    predictions.sort(key = lambda x: -x[1])
    for player in predictions:
        file.write(f'{player[0]:>{max_name_len}}' + ' | ' + str(math.ceil(player[1])) + '\n')

    file.close()


##### GOALIES #####
def generate_goalie_report():
    ##### Load Model #####
    current_file_path = pathlib.Path(__file__).parent.absolute()
    path = current_file_path.parents[0] / 'SavedModels'

    file = None
    try:
        file = open(path / 'goalie_model.sav', 'rb')
    except:
        raise Exception('Missing goalie_model.sav')

    reg = pickle.load(file)


    ##### Predict and Save Fantasy Values #####
    path = current_file_path.parents[0].parents[0] / 'Data' / 'PlayerData'

    stats = np.load(path / 'most_recent_season_data.npy', allow_pickle=True)
    stats = stats[3]

    temp = []
    for player in stats:
        temp.append([player[8], player[37], player[15], player[33], player[10], player[28], player[35], player[16], player[23]])
    stats = temp

    names = np.load(path / 'most_recent_season_data_names.npy', allow_pickle=True)
    names = names[3]

    predictions = []
    temp = reg.predict(stats)
    for i, player in enumerate(names):
        value = temp[i]
        if value < 0:
            value = 0
        else:
            value = math.ceil(value)

        predictions.append((player[0], value))

    file = None
    try:
        file = open(current_file_path.parents[0] / 'Reports' / 'goalie_report.txt', 'x')
    except:
        os.remove(current_file_path.parents[0] / 'Reports' / 'goalie_report.txt')
        file = open(current_file_path.parents[0] / 'Reports' / 'goalie_report.txt', 'x')

    max_name_len = max(len(player[0]) for player in predictions)
    name_str = 'Player Name'
    file.write(f'{name_str:>{max_name_len}}' + ' | ' + 'Predicted Fantasy Points' + '\n\n')

    predictions.sort(key = lambda x: -x[1])
    for player in predictions:
        file.write(f'{player[0]:>{max_name_len}}' + ' | ' + str(math.ceil(player[1])) + '\n')

    file.close()



def main():
    generate_skater_reports('center')
    generate_skater_reports('wing')
    generate_skater_reports('defenceman')
    generate_goalie_report()


if __name__ == "__main__":
    main()
    
import numpy as np
import pathlib
import pickle
import math

def generate_reports(position_str):
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
    path = current_file_path.parents[0].parents[0] / 'Data' / 'PlayerData' / position_str.capitalize()

    stats = np.load(path / 'most_recent_season_data.npy', allow_pickle=True)
    names = np.load(path / 'most_recent_season_data_names.npy', allow_pickle=True)

    predictions = []
    temp = reg.predict(stats)
    for i, player in enumerate(names):
        value = temp[i]
        if value < 0:
            value = 0
        else:
            value = math.ceil(value)

        predictions.append((player[0], value))

    file = open(current_file_path.parents[0] / 'Reports' / (position_str + '_report.txt'), 'w')

    max_name_len = max(len(player[0]) for player in predictions)
    name_str = 'Player Name'
    file.write(f'{name_str:>{max_name_len}}' + ' | ' + 'Predicted Fantasy Points' + '\n\n')

    predictions.sort(key = lambda x: -x[1])
    for player in predictions:
        file.write(f'{player[0]:>{max_name_len}}' + ' | ' + str(math.ceil(player[1])) + '\n')

    file.close()


def main():
    generate_reports('centers')
    generate_reports('wings')
    generate_reports('defencemen')
    generate_reports('goalies')


if __name__ == "__main__":
    main()
    
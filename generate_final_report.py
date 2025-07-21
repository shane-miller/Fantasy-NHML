import numpy as np
import argparse
import pathlib
import pickle
import math

def process_model(model_str, positions):
    ### Load Models ###
    current_file_path = pathlib.Path(__file__).parent.absolute()
    path = current_file_path / model_str / 'SavedModels'

    # Map position string to model file and data folder
    position_map = {
        'Center': ('centers_model.sav', 'Centers'),
        'Wing': ('wings_model.sav', 'Wings'),
        'Defenceman': ('defencemen_model.sav', 'Defencemen'),
        'Goalie': ('goalies_model.sav', 'Goalies'),
        'Forward': [('centers_model.sav', 'Centers'), ('wings_model.sav', 'Wings')],
        'Skater': [('centers_model.sav', 'Centers'), ('wings_model.sav', 'Wings'), ('defencemen_model.sav', 'Defencemen')]
    }


    predictions = []
    current_file_path = pathlib.Path(__file__).parent.absolute()
    base_path = current_file_path / 'Data' / 'PlayerData'

    # Handle multi-group positions (Forward, Skater)
    if isinstance(position_map[positions], list):
        for model_file, folder in position_map[positions]:
            reg = pickle.load(open(path / model_file, 'rb'))
            stats = np.load(base_path / folder / 'most_recent_season_data.npy', allow_pickle=True)
            names = np.load(base_path / folder / 'most_recent_season_data_names.npy', allow_pickle=True)
            curr_stats = np.asarray(stats)
            temp = reg.predict(curr_stats)
            for j, player in enumerate(names):
                value = temp[j]
                if value < 0:
                    value = 0
                else:
                    value = math.ceil(value)
                predictions.append((player[0], value))
    else:
        model_file, folder = position_map[positions]
        reg = pickle.load(open(path / model_file, 'rb'))
        stats = np.load(base_path / folder / 'most_recent_season_data.npy', allow_pickle=True)
        names = np.load(base_path / folder / 'most_recent_season_data_names.npy', allow_pickle=True)
        curr_stats = np.asarray(stats)
        temp = reg.predict(curr_stats)
        for j, player in enumerate(names):
            value = temp[j]
            if value < 0:
                value = 0
            else:
                value = math.ceil(value)
            predictions.append((player[0], value))
    return predictions


def generate_report(models, file, position_str):
    predictions_list = []
    if models[0]:
        predictions_list.append(process_model('RandomForest', position_str))
    if models[1]:
        predictions_list.append(process_model('AdaBoost', position_str))
    if models[2]:
        predictions_list.append(process_model('XGBoost', position_str))

    final_predictions = []
    for i in range(len(predictions_list[0])):
        total = 0
        for j in range(len(predictions_list)):
            total = total + predictions_list[j][i][1]

        total = math.ceil(total / len(predictions_list))
        final_predictions.append((predictions_list[0][i][0], total))

    max_name_len = max(len(player[0]) for player in final_predictions)
    name_str = 'Player Name'
    file.write('\n\n' + f'{position_str:>{(max_name_len + 1)}}' + ' ' + 'Predictions' + '\n\n')
    file.write(f'{name_str:>{max_name_len}}' + ' | ' + 'Predicted Fantasy Points' + '\n\n')

    final_predictions.sort(key = lambda x: -x[1])
    for player in final_predictions:
        file.write(f'{player[0]:>{max_name_len}}' + ' | ' + str(math.ceil(player[1])) + '\n')


def main():
    ##### PARSER #####
    parser = argparse.ArgumentParser(description = 'Set models used for predictions and report format.')

    parser.add_argument('--rf',  action = 'store_true', help = 'Add tag if you want to use RandomForest for predictions.')
    parser.add_argument('--ab',  action = 'store_true', help = 'Add tag if you want to use AdaBoost for predictions.')
    parser.add_argument('--xgb', action = 'store_true', help = 'Add tag if you want to use XGBoost for predictions.')
    parser.add_argument('--format', type = str, choices = ['sg', 'fdg', 'cwdg'], default = 'fdg', help = 'sg for skater/goalie, fdg for forward/defence/goalie, cwdg for center/wing/defence/goalie')

    args = parser.parse_args()

    models = [args.rf, args.ab, args.xgb]
    report_format = args.format

    positions = None
    if report_format == 'sg':
        positions = ['Skater', 'Goalie']
    elif report_format == 'fdg':
        positions = ['Forward', 'Defenceman', 'Goalie']
    else:
        positions = ['Center', 'Wing', 'Defenceman', 'Goalie']

    if not any(models):
        models = [True, True, True, True, True, True, True]

    ##### PATH #####
    current_file_path = pathlib.Path(__file__).parent.absolute()

    file = open(current_file_path / 'final_report.txt', 'w')

    for position in positions:
        generate_report(models, file, position)

    file.close()


if __name__ == "__main__":
    main()

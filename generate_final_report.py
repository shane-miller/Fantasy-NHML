import numpy as np
import argparse
import pathlib
import pickle
import math

def process_model(model_str, index):
    ### Load Models ###
    current_file_path = pathlib.Path(__file__).parent.absolute()
    path = current_file_path / model_str / 'SavedModels'

    center_reg = None
    if 0 in index:
        file = None
        try:
            file = open(path / 'center_model.sav', 'rb')
        except:
            raise Exception('Missing ' + model_str + '\'s center_model.sav')

        center_reg = pickle.load(file)

    wing_reg = None
    if 1 in index:
        file = None
        try:
            file = open(path / 'wing_model.sav', 'rb')
        except:
            raise Exception('Missing ' + model_str + '\'s wing_model.sav')

        wing_reg = pickle.load(file)

    def_reg = None
    if 2 in index:
        file = None
        try:
            file = open(path / 'defenceman_model.sav', 'rb')
        except:
            raise Exception('Missing ' + model_str + '\'s defenceman_model.sav')

        def_reg = pickle.load(file)

    goalie_reg = None
    if 3 in index:
        file = None
        try:
            file = open(path / 'goalie_model.sav', 'rb')
        except:
            raise Exception('Missing ' + model_str + '\'s goalie_model.sav')

        goalie_reg = pickle.load(file)


    ### Predict and Save Fantasy Values ###
    predictions = []

    current_file_path = pathlib.Path(__file__).parent.absolute()
    path = current_file_path / 'Data' / 'PlayerData'

    stats = np.load(path / 'most_recent_season_data.npy', allow_pickle=True)
    names = np.load(path / 'most_recent_season_data_names.npy', allow_pickle=True)
    for i in index:
        curr_stats = stats[i]
        curr_stats = np.asarray(curr_stats)

        curr_names = names[i]

        reg = None
        if i == 0:
            reg = center_reg
        elif i == 1:
            reg = wing_reg
        elif i == 2:
            reg = def_reg
        else:
            reg = goalie_reg

        temp = reg.predict(curr_stats)
        for j, player in enumerate(curr_names):
            value = temp[j]
            if value < 0:
                value = 0
            else:
                value = math.ceil(value)

            predictions.append((player[0], value))

    return predictions


def generate_report(models, file, position_str):
    index = None
    if position_str == 'Center':
        index = [0]
    elif position_str == 'Wing':
        index = [1]
    elif position_str == 'Defenceman':
        index = [2]
    elif position_str == 'Goalie':
        index = [3]
    elif position_str == 'Forward':
        index = [0, 1]
    else:
        index = [0, 1, 2]

    predictions_list = []
    if models[0]:
        predictions_list.append(process_model('MultivariateLinearRegression', index))
    if models[1]:
        predictions_list.append(process_model('PassiveAggressiveRegression', index))
    if models[2]:
        predictions_list.append(process_model('ElasticNet', index))
    if models[3]:
        predictions_list.append(process_model('RandomForest', index))
    if models[4]:
        predictions_list.append(process_model('AdaBoost', index))
    if models[5]:
        predictions_list.append(process_model('GradientBoost', index))
    if models[6]:
        predictions_list.append(process_model('XGBoost', index))

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

    parser.add_argument('--mlr', action = 'store_true', help = 'Add tag if you want to use MultivariateLinearRegression for predictions.')
    parser.add_argument('--par', action = 'store_true', help = 'Add tag if you want to use PassiveAggressiveRegression for predictions.')
    parser.add_argument('--en',  action = 'store_true', help = 'Add tag if you want to use ElasticNet for predictions.')
    parser.add_argument('--rf',  action = 'store_true', help = 'Add tag if you want to use RandomForest for predictions.')
    parser.add_argument('--ab',  action = 'store_true', help = 'Add tag if you want to use AdaBoost for predictions.')
    parser.add_argument('--gb',  action = 'store_true', help = 'Add tag if you want to use GradientBoost for predictions.')
    parser.add_argument('--xgb', action = 'store_true', help = 'Add tag if you want to use XGBoost for predictions.')
    parser.add_argument('--format', type = str, choices = ['sg', 'fdg', 'cwdg'], default = 'fdg', help = 'sg for skater/goalie, fdg for forward/defence/goalie, cwdg for center/wing/defence/goalie')

    args = parser.parse_args()

    models = [args.mlr, args.par, args.en, args.rf, args.ab, args.gb, args.xgb]
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

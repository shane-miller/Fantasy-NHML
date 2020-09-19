import argparse
import pathlib

def process_model(model_str, index):
    #returns tuple with all position indices appended together
    #returns after predictions were made
    pass


def generate_report(models, file, position_str):
    index = None
    if position_str == 'Center':
        index = [0]
    elif position_str == 'Wing':
        index = [1]
    elif position_str == 'Defencemen':
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
    file.write(f'{position_str:>{(max_name_len + 2)}}' + ' ' + 'Predictions' + '\n\n')
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
    parser.add_argument('--format', type = str, choices = ['sg', 'fdg', 'cwdg'], default = 'fdg', help = 'sg for skater/goalie, fdg for foward/defence/goalie, cwdg for center/wing/defence/goalie')

    args = parser.parse_args()

    models = [args.mlr, args.par, args.en, args.rf, args.ab, args.gb, args.xgb]
    report_format = args.format

    positions = None
    if report_format == 'sg':
        positions = ['Skater', 'Goalie']
    elif report_format == 'fdg':
        positions = ['Foward', 'Defencemen', 'Goalie']
    else:
        positions = ['Center', 'Wing', 'Defencemen', 'Goalie']

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

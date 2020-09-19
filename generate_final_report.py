import argparse
import pathlib


def generate_report(models, file, position_str):
    index = None
    if position_str == 'Centers':
        index = [0]
    elif position_str == 'Wings':
        index = [1]
    elif position_str == 'Defencemen':
        index = [2]
    elif position_str == 'Goalies':
        index = [3]
    elif position_str == 'Fowards':
        index = [0, 1]
    else:
        index = [0, 1, 2]


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

    models = [args.mlr, args.par, args.en, args.rf, args.ab, args.gb, args.xgb, args.format]

    positions = None
    if report_format == 'sg':
        positions = ['Skaters', 'Goalies']
    elif report_format == 'fdg':
        positions = ['Foward', 'Defencemen', 'Goalies']
    else:
        positions = ['Centers', 'Wings', 'Defencemen', 'Goalies']

    if not models.any():
        models = [True, True, True, True, True, True, True]

    ##### PATH #####
    current_file_path = pathlib.Path(__file__).parent.absolute()

    file = open(current_file_path / 'final_report.txt', 'w'

    for position in positions:
        generate_report(models, file, position)

    file.close()


if __name__ == "__main__":
    main()

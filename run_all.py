from RandomForest import run_all as rf
from AdaBoost import run_all as ab
from XGBoost import run_all as xgb
import argparse


def main():
    ##### PARSER #####
    parser = argparse.ArgumentParser(description = 'Use these tags if you don\'t want every model to run.')

    parser.add_argument('--rf',  action = 'store_true', help = 'Add tag if you want to run RandomForest')
    parser.add_argument('--ab',  action = 'store_true', help = 'Add tag if you want to run AdaBoost')
    parser.add_argument('--xgb', action = 'store_true', help = 'Add tag if you want to run XGBoost')

    args = parser.parse_args()

    run_rf  = args.rf
    run_ab  = args.ab
    run_xgb = args.xgb


    ##### Run All Networks #####
    if not (run_rf or run_ab or run_xgb):
        run_rf = run_ab = run_xgb = True

    if run_rf:
        print()
        rf.main()

    if run_ab:
        print()
        ab.main()

    if run_xgb:
        print()
        xgb.main()

    print()


if __name__ == "__main__":
    main()

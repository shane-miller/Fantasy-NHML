from MultipleRegression import run_all as mr
from GradientBoost import run_all as gb
from RandomForest import run_all as rf
from ElasticNet import run_all as en
from AdaBoost import run_all as ab
from XGBoost import run_all as xgb
import argparse


def main():
    ##### PARSER #####
    parser = argparse.ArgumentParser(description = 'Use these tags if you don\'t want every model to run.')

    parser.add_argument('--mr', action = 'store_true', help = 'Add tag if you want to run MultipleRegression')
    parser.add_argument('--en',  action = 'store_true', help = 'Add tag if you want to run ElasticNet')
    parser.add_argument('--rf',  action = 'store_true', help = 'Add tag if you want to run RandomForest')
    parser.add_argument('--ab',  action = 'store_true', help = 'Add tag if you want to run AdaBoost')
    parser.add_argument('--gb',  action = 'store_true', help = 'Add tag if you want to run GradientBoost')
    parser.add_argument('--xgb', action = 'store_true', help = 'Add tag if you want to run XGBoost')

    args = parser.parse_args()

    run_mr = args.mr
    run_en  = args.en
    run_rf  = args.rf
    run_ab  = args.ab
    run_gb  = args.gb
    run_xgb = args.xgb


    ##### Run All Networks #####
    if not (run_mr or run_en or run_rf or run_ab or run_gb or run_xgb):
        run_mr = run_en = run_rf = run_ab = run_gb = run_xgb = True

    if run_mr:
        print()
        mr.main()

    if run_en:
        print()
        en.main()

    if run_rf:
        print()
        rf.main()

    if run_ab:
        print()
        ab.main()

    if run_gb:
        print()
        gb.main()

    if run_xgb:
        print()
        xgb.main()

    print()


if __name__ == "__main__":
    main()

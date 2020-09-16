from MultivariateLinearRegression import run_all as mlr
from PassiveAggressiveRegression import run_all as par
from GradientBoost import run_all as gb
from RandomForest import run_all as rf
from ElasticNet import run_all as en
from AdaBoost import run_all as ab
from XGBoost import run_all as xgb
from shutil import rmtree
import argparse
import pathlib


def main():
    ##### PARSER #####
    parser = argparse.ArgumentParser(description = 'Use these if you don\'t want every model to run.')

    parser.add_argument('--mlr', type = bool, default = False, help = 'Add if you want to run MultivariateLinearRegression')
    parser.add_argument('--par', type = bool, default = False, help = 'Add if you want to run PassiveAggressiveRegression')
    parser.add_argument('--en',  type = bool, default = False, help = 'Add if you want to run ElasticNet')
    parser.add_argument('--rf',  type = bool, default = False, help = 'Add if you want to run RandomForest')
    parser.add_argument('--ab',  type = bool, default = False, help = 'Add if you want to run AdaBoost')
    parser.add_argument('--gb',  type = bool, default = False, help = 'Add if you want to run GradientBoost')
    parser.add_argument('--xgb', type = bool, default = False, help = 'Add if you want to run XGBoost')

    args = parser.parse_args()

    run_mlr = args.mlr
    run_par = args.par
    run_en  = args.en
    run_rf  = args.rf
    run_ab  = args.ab
    run_gb  = args.gb
    run_xgb = args.xgb


    ##### Run All Networks #####
    if not (run_mlr or run_par or run_en or run_rf or run_ab or run_gb or run_xgb):
        run_mlr = True
        run_par = True
        run_en  = True
        run_rf  = True
        run_ab  = True
        run_gb  = True
        run_xgb = True

    if run_mlr:
        print()
        mlr.main()

    if run_par:
        print()
        par.main()

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


    ##### Remove __pycache__ Folders #####
    current_file_path = pathlib.Path(__file__).parent.absolute()

    path = current_file_path / 'MultivariateLinearRegression' / '__pycache__'
    rmtree(path)

    path = current_file_path / 'PassiveAggressiveRegression' / '__pycache__'
    rmtree(path)
    
    path = current_file_path / 'ElasticNet' / '__pycache__'
    rmtree(path)

    path = current_file_path / 'RandomForest' / '__pycache__'
    rmtree(path)

    path = current_file_path / 'GradientBoost' / '__pycache__'
    rmtree(path)

    path = current_file_path / 'AdaBoost' / '__pycache__'
    rmtree(path)

    path = current_file_path / 'XGBoost' / '__pycache__'
    rmtree(path)


if __name__ == "__main__":
    main()

from MultivariateLinearRegression import run_all as mlr
from GradientBoost import run_all as gb
from AdaBoost import run_all as ab
from RandomForest import run_all as rf
from XGBoost import run_all as xgb
from shutil import rmtree
import pathlib

def main():
    ##### Run All Networks #####
    print()
    mlr.main()
    print()
    rf.main()
    print()
    ab.main()
    print()
    gb.main()
    print()
    xgb.main()
    print()

    ##### Remove __pycache__ Folders #####
    current_file_path = pathlib.Path(__file__).parent.absolute()

    path = current_file_path / 'MultivariateLinearRegression' / '__pycache__'
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

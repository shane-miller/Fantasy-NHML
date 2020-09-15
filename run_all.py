from MultivariateLinearRegression import run_all as mlr
from RandomForest import run_all as rf
from GradientBoost import run_all as gb
from shutil import rmtree
import pathlib

def main():
    ##### Run All Networks #####
    print()
    mlr.main()
    print()
    rf.main()
    print()
    gb.main()
    print()

    ##### Remove __pycache__ Folders #####
    current_file_path = pathlib.Path(__file__).parent.absolute()

    path = current_file_path / 'MultivariateLinearRegression' / '__pycache__'
    rmtree(path)

    path = current_file_path / 'RandomForest' / '__pycache__'
    rmtree(path)

    path = current_file_path / 'GradientBoost' / '__pycache__'
    rmtree(path)


if __name__ == "__main__":
    main()

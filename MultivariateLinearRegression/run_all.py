from MultivariateLinearRegression.Networks import generate_model as mlr
from MultivariateLinearRegression.ReportGeneration import generate_all_reports
from shutil import rmtree
import pathlib

def main():
    print('----- Processing Multivariate Linear Regression -----')
    ##### Generate Models #####
    mlr.generate_model('centers')
    mlr.generate_model('wings')
    mlr.generate_model('defencemen')
    mlr.generate_model('goalies')

    ##### Generate Reports #####
    generate_all_reports.main()


    ##### Remove __pycache__ Folders #####
    current_file_path = pathlib.Path(__file__).parent.absolute()

    path = current_file_path / 'Networks' / '__pycache__'
    rmtree(path)

    path = current_file_path / 'ReportGeneration' / '__pycache__'
    rmtree(path)


if __name__ == "__main__":
    main()

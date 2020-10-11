from XGBoost.Networks import generate_model as xgb
from XGBoost.ReportGeneration import generate_all_reports
from shutil import rmtree
import pathlib

def main():
    print('----- Processing XGBoost Regression -----')
    ##### Generate Models #####
    xgb.generate_model('centers')
    xgb.generate_model('wings')
    xgb.generate_model('defencemen')
    xgb.generate_model('goalies')


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

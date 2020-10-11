from AdaBoost.Networks import generate_model as ada
from AdaBoost.ReportGeneration import generate_all_reports
from shutil import rmtree
import pathlib

def main():
    print('----- Processing AdaBoost Regression -----')
    ##### Generate Models #####
    ada.generate_model('centers')
    ada.generate_model('wings')
    ada.generate_model('defencemen')
    ada.generate_model('goalies')


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

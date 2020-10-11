from RandomForest.Networks import generate_model as rf
from RandomForest.ReportGeneration import generate_all_reports
from shutil import rmtree
import pathlib

def main():
    print('----- Processing Random Forest Regression -----')
    ##### Generate Models #####
    rf.generate_model('centers')
    rf.generate_model('wings')
    rf.generate_model('defencemen')
    rf.generate_model('goalies')


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
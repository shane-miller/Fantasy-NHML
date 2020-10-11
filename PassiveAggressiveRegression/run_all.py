from PassiveAggressiveRegression.Networks import generate_model as par
from PassiveAggressiveRegression.ReportGeneration import generate_all_reports
from shutil import rmtree
import pathlib

def main():
    print('----- Processing Passive Aggressive Regression -----')
    ##### Generate Models #####
    par.generate_model('centers')
    par.generate_model('wings')
    par.generate_model('defencemen')
    par.generate_model('goalies')


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
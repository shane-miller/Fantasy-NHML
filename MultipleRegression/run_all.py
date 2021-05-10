from MultipleRegression.Networks import generate_model as mr
from MultipleRegression.ReportGeneration import generate_all_reports
from shutil import rmtree
import pathlib

def main():
    print('----- Processing Multiple Regression -----')
    ##### Generate Models #####
    mr.generate_model('centers')
    mr.generate_model('wings')
    mr.generate_model('defencemen')
    mr.generate_model('goalies')

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

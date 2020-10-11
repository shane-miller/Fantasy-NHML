from GradientBoost.Networks import generate_model as gb
from GradientBoost.ReportGeneration import generate_all_reports
from shutil import rmtree
import pathlib

def main():
    print('----- Processing Gradient Boost Regression -----')
    ##### Generate Models #####
    gb.generate_model('centers')
    gb.generate_model('wings')
    gb.generate_model('defencemen')
    gb.generate_model('goalies')


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

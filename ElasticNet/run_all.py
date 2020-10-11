from ElasticNet.Networks import generate_model as en
from ElasticNet.ReportGeneration import generate_all_reports
from shutil import rmtree
import pathlib

def main():
    print('----- Processing Elastic Net Regression -----')
    ##### Generate Models #####
    en.generate_model('centers')
    en.generate_model('wings')
    en.generate_model('defencemen')
    en.generate_model('goalies')


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
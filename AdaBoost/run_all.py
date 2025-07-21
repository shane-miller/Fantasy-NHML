from AdaBoost.Networks import generate_model as ada
from AdaBoost.ReportGeneration import generate_all_reports

def main():
    print('----- Processing AdaBoost Regression -----')
    ##### Generate Models #####
    ada.generate_model('centers')
    ada.generate_model('wings')
    ada.generate_model('defencemen')
    ada.generate_model('goalies')


    ##### Generate Reports #####
    generate_all_reports.main()


if __name__ == "__main__":
    main()

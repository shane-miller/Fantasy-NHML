from RandomForest.Networks import generate_model as rf
from RandomForest.ReportGeneration import generate_all_reports

def main():
    print('----- Processing Random Forest Regression -----')
    ##### Generate Models #####
    rf.generate_model('centers')
    rf.generate_model('wings')
    rf.generate_model('defencemen')
    rf.generate_model('goalies')


    ##### Generate Reports #####
    generate_all_reports.main()


if __name__ == "__main__":
    main()
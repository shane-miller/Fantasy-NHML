from XGBoost.Networks import generate_model as xgb
from XGBoost.ReportGeneration import generate_all_reports

def main():
    print('----- Processing XGBoost Regression -----')
    ##### Generate Models #####
    xgb.generate_model('centers')
    xgb.generate_model('wings')
    xgb.generate_model('defencemen')
    xgb.generate_model('goalies')


    ##### Generate Reports #####
    generate_all_reports.main()


if __name__ == "__main__":
    main()

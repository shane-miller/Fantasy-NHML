from MultipleRegression.Networks import generate_model as mr
from MultipleRegression.ReportGeneration import generate_all_reports

def main():
    print('----- Processing Multiple Regression -----')
    ##### Generate Models #####
    mr.generate_model('centers')
    mr.generate_model('wings')
    mr.generate_model('defencemen')
    mr.generate_model('goalies')

    ##### Generate Reports #####
    generate_all_reports.main()


if __name__ == "__main__":
    main()

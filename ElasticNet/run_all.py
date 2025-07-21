from ElasticNet.Networks import generate_model as en
from ElasticNet.ReportGeneration import generate_all_reports

def main():
    print('----- Processing Elastic Net Regression -----')
    ##### Generate Models #####
    en.generate_model('centers')
    en.generate_model('wings')
    en.generate_model('defencemen')
    en.generate_model('goalies')


    ##### Generate Reports #####
    generate_all_reports.main()


if __name__ == "__main__":
    main()
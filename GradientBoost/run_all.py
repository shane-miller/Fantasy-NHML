from GradientBoost.Networks import generate_model as gb
from GradientBoost.ReportGeneration import generate_all_reports

def main():
    print('----- Processing Gradient Boost Regression -----')
    ##### Generate Models #####
    gb.generate_model('centers')
    gb.generate_model('wings')
    gb.generate_model('defencemen')
    gb.generate_model('goalies')


    ##### Generate Reports #####
    generate_all_reports.main()


if __name__ == "__main__":
    main()

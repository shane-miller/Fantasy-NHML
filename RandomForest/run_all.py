from Networks import center_network
from Networks import wing_network
from Networks import defenceman_network
from Networks import goalie_network
from ReportGeneration import generate_all_reports
from shutil import rmtree
import pathlib

print('----- Processing Random Forest Regression -----')
##### Generate Models #####
center_network.main()
wing_network.main()
defenceman_network.main()
goalie_network.main()


##### Generate Reports #####
generate_all_reports.main()


##### Remove __pycache__ Folders #####
current_file_path = pathlib.Path(__file__).parent.absolute()

path = current_file_path / 'Networks' / '__pycache__'
rmtree(path)

path = current_file_path / 'ReportGeneration' / '__pycache__'
rmtree(path)

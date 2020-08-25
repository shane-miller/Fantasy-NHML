from datetime import datetime
from tqdm import tqdm
import numpy as np
import requests
import argparse
import pathlib
import json


### PARSER ###
# Get fantasy point multiplier values from the command line.
parser = argparse.ArgumentParser(description = 'Fantasy Settings')

parser.add_argument('--g',    type = int, default = 0, help = 'Goals Multiplier')
parser.add_argument('--a',    type = int, default = 0, help = 'Assists Multiplier')
parser.add_argument('--pts',  type = int, default = 0, help = 'Points Multiplier')
parser.add_argument('--pm',   type = int, default = 0, help = '+/- Multiplyer')
parser.add_argument('--pim',  type = int, default = 0, help = 'Penalty Minutes Multiplier')
parser.add_argument('--ppg',  type = int, default = 0, help = 'Power Play Goals Multiplier')
parser.add_argument('--ppa',  type = int, default = 0, help = 'Power Play Assists Multiplier')
parser.add_argument('--ppp',  type = int, default = 0, help = 'Power Play Points Multiplier')
parser.add_argument('--shg',  type = int, default = 0, help = 'Short Handed Goal Multiplier')
parser.add_argument('--sha',  type = int, default = 0, help = 'Short Handed Assist Multiplier')
parser.add_argument('--shp',  type = int, default = 0, help = 'Short Handed Point Multiplier')
parser.add_argument('--gwg',  type = int, default = 0, help = 'Game Winning Goal Multiplier')
parser.add_argument('--fow',  type = int, default = 0, help = 'Faceoffs Won Multiplier')
parser.add_argument('--fol',  type = int, default = 0, help = 'Faceoffs Lost Multiplier')
parser.add_argument('--shft', type = int, default = 0, help = 'Shifts Multiplier')
parser.add_argument('--sog',  type = int, default = 0, help = 'Shots on Goal Multiplier')
parser.add_argument('--hit',  type = int, default = 0, help = 'Hits Multiplier')
parser.add_argument('--blk',  type = int, default = 0, help = 'Blocked Shots Multiplier')
parser.add_argument('--defp', type = int, default = 0, help = 'Defensemen Points Multiplier')
parser.add_argument('--gs',   type = int, default = 0, help = 'Games Started Multiplier')
parser.add_argument('--w',    type = int, default = 0, help = 'Wins Multiplier')
parser.add_argument('--l',    type = int, default = 0, help = 'Losses Multiplier')
parser.add_argument('--sa',   type = int, default = 0, help = 'Shots Against Multiplier')
parser.add_argument('--ga',   type = int, default = 0, help = 'Goals Against Multiplier')
parser.add_argument('--sv',   type = int, default = 0, help = 'Saves Multiplier')
parser.add_argument('--so',   type = int, default = 0, help = 'Shutouts Multiplier')
parser.add_argument('--otl',  type = int, default = 0, help = 'Overtime Losses Multiplier')

args = parser.parse_args()

g_multiplier    = args.g
a_multiplier    = args.a
pts_multiplier  = args.pts
pm_multiplier   = args.pm
pim_multiplier  = args.pim
ppg_multiplier  = args.ppg
ppa_multiplier  = args.ppa
ppp_multiplier  = args.ppp
shg_multiplier  = args.shg
sha_multiplier  = args.sha
shp_multiplier  = args.shp
gwg_multiplier  = args.gwg
fow_multiplier  = args.fow
fol_multiplier  = args.fol
shft_multiplier = args.shft
sog_multiplier  = args.sog
hit_multiplier  = args.hit
blk_multiplier  = args.blk
defp_multiplier = args.defp
gs_multiplier   = args.gs
w_multiplier    = args.w
l_multiplier    = args.l
sa_multiplier   = args.sa
ga_multiplier   = args.ga
sv_multiplier   = args.sv
so_multiplier   = args.so
otl_multiplier  = args.otl


### CONSTANT STRINGS ###
skater_summary = 'summary'
skater_fo_percentage = 'faceoffpercentages'
skater_fo_wl = 'faceoffwins'
skater_gfga = 'goalsForAgainst'
skater_misc = 'realtime'
skater_penalties = 'penalties'
skater_pk = 'penaltykill'
skater_pp = 'powerplay'
skater_puck_possession = 'puckPossessions'
skater_sat_count = 'summaryshooting'
skater_sat_percentages = 'percentages'
skater_scoring_per_60 = 'scoringRates'
skater_scoring_per_game = 'scoringpergame'
skater_toi = 'timeonice'

goalie_summary = 'summary'
goalie_advanced = 'advanced'
goalie_saves_by_strength = 'savesByStrength'

left_wing_tag = ['L', 'Left Wings']
right_wing_tag = ['R', 'Right Wings']
center_tag = ['C', 'Centers']
defenceman_tag = ['D', 'Defencemen']
goalie_tag = ['G', 'Goalies']

num_years = 10

year_upper_bound = f'{datetime.now().year - 1}{datetime.now().year}'
year_lower_bound = f'{datetime.now().year - num_years}{datetime.now().year - (num_years - 1)}'

base_skater_url = 'https://api.nhle.com/stats/rest/en/skater/{}?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22lastName%22,%22direction%22:%22ASC_CI%22%7D,%7B%22property%22:%22skaterFullName%22,%22direction%22:%22ASC_CI%22%7D,%7B%22property%22:%22seasonId%22,%22direction%22:%22DESC%22%7D%5D&start={}&limit=100&factCayenneExp=gamesPlayed%3E=25&cayenneExp=active%3D1%20and%20gameTypeId=2%20and%20positionCode%3D%22{}%22%20and%20seasonId%3C={}%20and%20seasonId%3E={}'
base_goalie_url = 'https://api.nhle.com/stats/rest/en/goalie/{}?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22lastName%22,%22direction%22:%22ASC_CI%22%7D,%7B%22property%22:%22goalieFullName%22,%22direction%22:%22ASC_CI%22%7D,%7B%22property%22:%22seasonId%22,%22direction%22:%22DESC%22%7D%5D&start={}&limit=100&factCayenneExp=gamesPlayed%3E=15&cayenneExp=active%3D1%20and%20gameTypeId=2%20and%20seasonId%3C={}%20and%20seasonId%3E={}'

# skater_report_list is commented out because NHL api crashes on sat_count when sorting alphabetically by name. Will fix when they fix.
#skater_report_list = [skater_toi, skater_scoring_per_game, skater_scoring_per_60, skater_sat_percentages, skater_sat_count, skater_puck_possession, skater_pp, skater_pk, skater_penalties, skater_misc, skater_gfga, skater_fo_wl, skater_fo_percentage, skater_summary]
skater_report_list = [skater_toi, skater_scoring_per_game, skater_scoring_per_60, skater_sat_percentages, skater_puck_possession, skater_pp, skater_pk, skater_penalties, skater_misc, skater_gfga, skater_fo_wl, skater_fo_percentage, skater_summary]
goalie_report_list = [goalie_saves_by_strength, goalie_advanced, goalie_summary]


# Function that queries the nhle api the required number of times and joins the data into one json record
def api_helper(base_url, tag, report_list, year_upper_bound, year_lower_bound):
	temp = {}
	if(tag == goalie_tag):
		temp = requests.get(base_url.format(report_list[0], 0, year_upper_bound, year_lower_bound)).json()
	else:
		temp = requests.get(base_url.format(report_list[0], 0, tag[0], year_upper_bound, year_lower_bound)).json()
	total_length = int(temp.get('total'))
	records = {'total': total_length}

	print('Processing ' + tag[1] + ':')
	for i in report_list:
		temp = {}
		for j in tqdm(range(0, total_length + 1, 100), desc='Batch Querying for Report Type ' + i):
			temp2 = {}
			if(tag == goalie_tag):
				temp2 = requests.get(base_url.format(i, j, year_upper_bound, year_lower_bound)).json()
			else:
				temp2 = requests.get(base_url.format(i, j, tag[0], year_upper_bound, year_lower_bound)).json()
			if(temp.get('data') == None):
				temp.update({'data': temp2.get('data')})
			else:
				temp.update({'data': temp.get('data') + temp2.get('data')})

		for k in range(total_length):
			if(records.get('data') == None):
				records.update({'data': temp.get('data')})
			else:
				records.get('data')[k].update(temp.get('data')[k])

	if(tag == goalie_tag):
		for player in records.get('data'):
			player.pop('ties')
			player.pop('shootsCatches')
			player.pop('teamAbbrevs')
	else:
		for player in records.get('data'):
			player.pop('positionCode')
			player.pop('shootsCatches')
			player.pop('teamAbbrevs')

	return records


# Calculates the total number of fantasy points a player had in a given season based on the values returned from the arg parser
def calculate_fantasy_points(players, tag, seasonId):
	fantasy_points_list = []
	for player in players:
		fantasy_total = 0

		key_names = []
		if(tag == 'goalie'):
			key_names = [['gamesStarted', gs_multiplier], ['wins', w_multiplier], ['losses', l_multiplier], ['shotsAgainst', sa_multiplier],
						 ['goalsAgainst', ga_multiplier], ['saves', sv_multiplier], ['shutouts', so_multiplier], ['otLosses', otl_multiplier]]
		else:
			key_names = [['goals', g_multiplier], ['assists', a_multiplier], ['points', pts_multiplier], ['plusMinus', pm_multiplier],
						 ['penaltyMinutes', pim_multiplier], ['ppGoals', ppg_multiplier], ['ppAssists', ppa_multiplier], ['ppPoints', ppp_multiplier],
						 ['shGoals', shg_multiplier], ['shAssists', sha_multiplier], ['shPoints', shp_multiplier], ['gameWinningGoals', gwg_multiplier],
						 ['totalFaceoffWins', fow_multiplier], ['totalFaceoffLosses', fol_multiplier], ['shifts', shft_multiplier], ['shots', sog_multiplier],
						 ['hits', hit_multiplier], ['blockedShots', blk_multiplier]]

		if(tag == 'defenceman'):
			key_names.append(['points', defp_multiplier])

		for key in key_names:
			fantasy_total = fantasy_total + (player.get(key[0]) * key[1])

		if(tag != 'goalie'):
			# See readme for explanation on this equation
			a = fantasy_total
			b = int(player.get('gamesPlayed'))
			fantasy_total = ((2*a*b) + 246*a)/(5*b)

		fantasy_points_list.append(fantasy_total)

	current_file_path = pathlib.Path(__file__).parent.absolute()
	path = current_file_path.parents[0] / 'Data'

	if(tag == 'center'):
		path = path / 'Centers'
	elif(tag == 'wing'):
		path = path / 'Wings'
	elif(tag == 'defenceman'):
		path = path / 'Defencemen'
	elif(tag == 'goalie'):
		path = path / 'Goalies'

	path = path / f'{seasonId}_fantasy_points'

	np.save(path, fantasy_points_list)


# Filters a list of players by a given year
def filter_list_by_year(player_list, year):
	filtered_list = [player for player in player_list if player.get('seasonId') == int(year)]
	filtered_list.sort(key=lambda x: x.get('playerId'))

	return filtered_list


# Saves the data for for the given year and tag into an np file into the correct folder
def save_yearly_data(player_list, tag, seasonId):
	final_list = []
	for player in player_list:
		temp_list = []

		if(tag == 'goalie'):
			temp_list.append(player.pop('goalieFullName'))
		else:
			temp_list.append(player.pop('skaterFullName'))
		
		temp_list.append(player.pop('lastName'))
		temp_list.append(player.pop('playerId'))
		temp_list.append(player.pop('seasonId'))
		
		player_stats_list = [(k,v) for k,v in player.items()]
		player_stats_list.sort(key=lambda x: x[0])
		
		for stat in player_stats_list:
			temp_list.append(stat[1])
		
		final_list.append(temp_list)

	current_file_path = pathlib.Path(__file__).parent.absolute()
	path = current_file_path.parents[0] / 'Data'

	if(tag == 'center'):
		path = path / 'Centers'
	elif(tag == 'wing'):
		path = path / 'Wings'
	elif(tag == 'defenceman'):
		path = path / 'Defencemen'
	elif(tag == 'goalie'):
		path = path /'Goalies'

	path = path / f'{seasonId}_data'
	np.save(path, final_list)


# Prints out the json for a players stats given in a dictionary
def print_stats(player):
	print(json.dumps(player, sort_keys = False, indent = 4))


def main():
	### DATA SCRAPING ###
	# Download data from the API the NHL uses for nhl.com/stats
	center_records = api_helper(base_skater_url, center_tag, skater_report_list, year_upper_bound, year_lower_bound)
	left_wing_records = api_helper(base_skater_url, left_wing_tag, skater_report_list, year_upper_bound, year_lower_bound)
	right_wing_records = api_helper(base_skater_url, right_wing_tag, skater_report_list, year_upper_bound, year_lower_bound)
	defenceman_records = api_helper(base_skater_url, defenceman_tag, skater_report_list, year_upper_bound, year_lower_bound)
	goalie_records = api_helper(base_goalie_url, goalie_tag, goalie_report_list, year_upper_bound, year_lower_bound)

	# Join Wing Lists Together
	wing_records = {
		'data': left_wing_records.get('data') + right_wing_records.get('data'),
		'total': left_wing_records.get('total') + right_wing_records.get('total')
	}

	# Printing example
	#print_stats(center_records.get('data')[0])
	
	records_list = [[center_records, 'center'], [wing_records, 'wing'], [defenceman_records, 'defenceman'], [goalie_records, 'goalie']]
	for records in records_list:
		for year in range(num_years, 0, -1):
			seasonId = f'{datetime.now().year - year}{datetime.now().year - (year - 1)}'
			filtered_list = filter_list_by_year(records[0].get('data'), seasonId)
			save_yearly_data(filtered_list, records[1], seasonId)
			if(year != num_years):
				calculate_fantasy_points(filtered_list, records[1], seasonId)


if __name__ == "__main__":
    main()

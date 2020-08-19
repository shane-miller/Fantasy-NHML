import numpy as np
import requests
import argparse
import json
from datetime import datetime

### PARSER ###
# Get fantasy point multiplier values from the command line.
parser = argparse.ArgumentParser(description = 'Fantasy Settings')

parser.add_argument('--g',    type = int, default = 0, help = 'Goals Multiplier') # 3
parser.add_argument('--a',    type = int, default = 0, help = 'Assists Multiplier') # 2
parser.add_argument('--pts',  type = int, default = 0, help = 'Points Multiplier')
parser.add_argument('--pm',   type = int, default = 0, help = '+/- Multiplyer')
parser.add_argument('--pim',  type = int, default = 0, help = 'Penalty Minutes Multiplier')
parser.add_argument('--ppg',  type = int, default = 0, help = 'Power Play Goals Multiplier')
parser.add_argument('--ppa',  type = int, default = 0, help = 'Power Play Assists Multiplier')
parser.add_argument('--ppp',  type = int, default = 0, help = 'Power Play Points Multiplier') # 1
parser.add_argument('--shg',  type = int, default = 0, help = 'Short Handed Goal Multiplier')
parser.add_argument('--sha',  type = int, default = 0, help = 'Short Handed Assist Multiplier')
parser.add_argument('--shp',  type = int, default = 0, help = 'Short Handed Point Multiplier') # 2
parser.add_argument('--gwg',  type = int, default = 0, help = 'Game Winning Goal Multiplier')
parser.add_argument('--fow',  type = int, default = 0, help = 'Faceoffs Won Multiplier')
parser.add_argument('--fol',  type = int, default = 0, help = 'Faceoffs Lost Multiplier')
parser.add_argument('--shft', type = int, default = 0, help = 'Shifts Multiplier')
parser.add_argument('--hat',  type = int, default = 0, help = 'Hat Tricks Multiplier')
parser.add_argument('--sog',  type = int, default = 0, help = 'Shots on Goal Multiplier')
parser.add_argument('--hit',  type = int, default = 0, help = 'Hits Multiplier')
parser.add_argument('--blk',  type = int, default = 0, help = 'Blocked Shots Multiplier')
parser.add_argument('--defp', type = int, default = 0, help = 'Defensemen Points Multiplier')
parser.add_argument('--gs',   type = int, default = 0, help = 'Games Started Multiplier')
parser.add_argument('--w',    type = int, default = 0, help = 'Wins Multiplier') # 5
parser.add_argument('--l',    type = int, default = 0, help = 'Losses Multiplier')
parser.add_argument('--sa',   type = int, default = 0, help = 'Shots Against Multiplier')
parser.add_argument('--ga',   type = int, default = 0, help = 'Goals Against Multiplier')
parser.add_argument('--ega',  type = int, default = 0, help = 'Empty Net Goals Against Multiplier')
parser.add_argument('--sv',   type = int, default = 0, help = 'Saves Multiplier')
parser.add_argument('--so',   type = int, default = 0, help = 'Shutouts Multiplier') # 3
parser.add_argument('--otl',  type = int, default = 0, help = 'Overtime Losses Multiplier') # 2

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
hat_multiplier  = args.hat
sog_multiplier  = args.sog
hit_multiplier  = args.hit
blk_multiplier  = args.blk
defp_multiplier = args.defp
gs_multiplier   = args.gs
w_multiplier    = args.w
l_multiplier    = args.l
sa_multiplier   = args.sa
ga_multiplier   = args.ga
ega_multiplier  = args.ega
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

left_wing_tag = 'L'
right_wing_tag = 'R'
center_tag = 'C'
defenceman_tag = 'D'

year_upper_bound = f'{datetime.now().year - 1}{datetime.now().year}'
year_lower_bound = f'{datetime.now().year - 5}{datetime.now().year - 4}'

start_position = 0


### DATA SCRAPING ###
# Download data from the API the NHL uses for nhl.com/stats
base_skater_url = 'https://api.nhle.com/stats/rest/en/skater/{}?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22lastName%22,%22direction%22:%22ASC_CI%22%7D,%7B%22property%22:%22skaterFullName%22,%22direction%22:%22ASC_CI%22%7D,%7B%22property%22:%22seasonId%22,%22direction%22:%22DESC%22%7D%5D&start={}&limit=100&factCayenneExp=gamesPlayed%3E=25&cayenneExp=active%3D1%20and%20gameTypeId=2%20and%20positionCode%3D%22{}%22%20and%20seasonId%3C={}%20and%20seasonId%3E={}'
base_goalie_url = 'https://api.nhle.com/stats/rest/en/goalie/{}?isAggregate=false&isGame=false&sort=%5B%7B%22property%22:%22lastName%22,%22direction%22:%22ASC_CI%22%7D,%7B%22property%22:%22skaterFullName%22,%22direction%22:%22ASC_CI%22%7D,%7B%22property%22:%22seasonId%22,%22direction%22:%22DESC%22%7D%5D&start={}&limit=100&factCayenneExp=gamesPlayed%3E=15&cayenneExp=active%3D1%20and%20gameTypeId=2%20and%20seasonId%3C={}%20and%20seasonId%3E={}'



temp = requests.get(base_skater_url.format(skater_summary, start_position, center_tag, year_upper_bound, year_lower_bound)).json()
total_length = int(temp.get('total'))
#center_report_list is commented out because NHL api crashes on sat_count when sorting alphabetically by name. Will fix when they fix.
#center_report_list = [skater_summary, skater_fo_percentage, skater_fo_wl, skater_gfga, skater_misc, skater_penalties, skater_pk, skater_pp, skater_puck_possession, skater_sat_count, skater_sat_percentages, skater_scoring_per_60, skater_scoring_per_game, skater_toi]
center_report_list = [skater_summary, skater_fo_percentage, skater_fo_wl, skater_gfga, skater_misc, skater_penalties, skater_pk, skater_pp, skater_puck_possession, skater_sat_percentages, skater_scoring_per_60, skater_scoring_per_game, skater_toi]
center_records = {'total': total_length}
for i in reversed(center_report_list):
	temp = {}
	for j in range(start_position, int(total_length/100)*100 + 99, 100):
		temp2 = requests.get(base_skater_url.format(i, j, center_tag, year_upper_bound, year_lower_bound)).json()
		if(temp.get('data') == None):
			temp.update({'data': temp2.get('data')})
		else:
			temp.update({'data': temp.get('data') + temp2.get('data')})

	for k in range(total_length):
		if(center_records.get('data') == None):
			center_records.update({'data': temp.get('data')})
		else:
			center_records.get('data')[k].update(temp.get('data')[k])

print(json.dumps(center_records.get('data')[0], sort_keys = True, indent = 4))


# todo: do the same for defensement and goals
# todo: save a .npy file for each forward, defense, and goalie and save the files to the correct folders in /data

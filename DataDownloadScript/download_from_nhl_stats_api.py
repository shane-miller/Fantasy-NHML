import numpy as np
import requests
import argparse
import json

### PARSER ###
# Get fantasy point multiplier values from the command line.
parser = argparse.ArgumentParser(description = 'Fantasy Settings')

parser.add_argument('--g',    type = int, default = 3, help = 'Goals Multiplier')
parser.add_argument('--a',    type = int, default = 2, help = 'Assists Multiplier')
parser.add_argument('--pts',  type = int, default = 0, help = 'Points Multiplier')
parser.add_argument('--pm',   type = int, default = 0, help = '+/- Multiplyer')
parser.add_argument('--pim',  type = int, default = 0, help = 'Penalty Minutes Multiplier')
parser.add_argument('--ppg',  type = int, default = 0, help = 'Power Play Goals Multiplier')
parser.add_argument('--ppa',  type = int, default = 0, help = 'Power Play Assists Multiplier')
parser.add_argument('--ppp',  type = int, default = 1, help = 'Power Play Points Multiplier')
parser.add_argument('--shg',  type = int, default = 0, help = 'Short Handed Goal Multiplier')
parser.add_argument('--sha',  type = int, default = 0, help = 'Short Handed Assist Multiplier')
parser.add_argument('--shp',  type = int, default = 2, help = 'Short Handed Point Multiplier')
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
parser.add_argument('--w',    type = int, default = 5, help = 'Wins Multiplier')
parser.add_argument('--l',    type = int, default = 0, help = 'Losses Multiplier')
parser.add_argument('--sa',   type = int, default = 0, help = 'Shots Against Multiplier')
parser.add_argument('--ga',   type = int, default = 0, help = 'Goals Against Multiplier')
parser.add_argument('--ega',  type = int, default = 0, help = 'Empty Net Goals Multiplier')
parser.add_argument('--sv',   type = int, default = 0, help = 'Saves Multiplier')
parser.add_argument('--so',   type = int, default = 3, help = 'Shutouts Multiplier')
parser.add_argument('--otl',  type = int, default = 2, help = 'Overtime Losses Multiplier')

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


### DATA SCRAPING ###
# Download data from the API the NHL uses for nhl.com/stats
url_forwards = 'https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=[%7B%22property%22:%22lastName%22,%22direction%22:%22ASC_CI%22%7D,%7B%22property%22:%22skaterFullName%22,%22direction%22:%22ASC_CI%22%7D]&start=100&limit=101&factCayenneExp=gamesPlayed%3E=30&cayenneExp=(positionCode=%22L%22%20or%20positionCode=%22R%22%20or%20positionCode=%22C%22)%20and%20active=1%20and%20gameTypeId=2%20and%20seasonId%3C=20192020%20and%20seasonId%3E=20152016'

forward_records = requests.get(url_forwards).json()

# todo: increment the start in the url each time by 100 so we don't get the same 100 players every time
# todo: add url for defensement and forwards
# todo: set date range to be last 5 years by getting the previous year rather than hard-coding it

for i in range(int(records['total']/100)+1):
    players = records['data']
    # todo: concatenate the json data together in a numpy array

# todo: save a .npy file for each forward, defense, and goalie and save the files to the correct folders in /data

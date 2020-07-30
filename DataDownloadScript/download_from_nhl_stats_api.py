import numpy as np
import requests
import json

url_forwards = 'https://api.nhle.com/stats/rest/en/skater/summary?isAggregate=false&isGame=false&sort=[%7B%22property%22:%22lastName%22,%22direction%22:%22ASC_CI%22%7D,%7B%22property%22:%22skaterFullName%22,%22direction%22:%22ASC_CI%22%7D]&start=100&limit=101&factCayenneExp=gamesPlayed%3E=30&cayenneExp=(positionCode=%22L%22%20or%20positionCode=%22R%22%20or%20positionCode=%22C%22)%20and%20active=1%20and%20gameTypeId=2%20and%20seasonId%3C=20192020%20and%20seasonId%3E=20102011'

forward_records = requests.get(url_forwards).json()

# todo: increment the start in the url each time by 100 so we don't get the same 100 players every time
# todo: add url for defensement and forwards
# todo: set date range to be last 10 years by getting the previous year rather than hard-coding it

for i in range(int(records['total']/100)+1):
    players = records['data']
    # todo: concatenate the json data together in a numpy array

# todo: save a .npy file for each forward, defense, and goalie and save the files to the correct folders in /data
